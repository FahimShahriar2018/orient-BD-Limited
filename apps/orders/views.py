from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from apps.cart.cart import Cart
from apps.catalog.models import Product
from .models import Order, OrderItem, Coupon, SHIPPING_PRICES
from .forms import CheckoutForm, PublicOrderTrackForm
from .utils import generate_tracking_number


def checkout_view(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please sign in or create an account to complete your purchase.')
        return redirect(f"{reverse('accounts:login')}?next={reverse('orders:checkout')}")

    cart = Cart(request)
    if cart.is_empty():
        messages.warning(request, 'Your shopping basket is empty.')
        return redirect('cart:cart_detail')

    subtotal = cart.get_subtotal()
    discount = cart.discount_amount
    initial_shipping = Decimal('0.00') if subtotal >= Decimal('50000.00') else Decimal('100.00')

    initial_data = {
        'shipping_method': 'inside_dhaka',
        'payment_method': 'cod',
        'full_name': request.user.get_full_name() or request.user.username,
        'phone': request.user.phone,
        'email': request.user.email,
        'division': request.user.address_division,
        'district': request.user.address_district,
        'street_address': request.user.address_street,
        'postal_code': request.user.address_postal,
    }

    form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'discount': discount,
        'shipping_price': initial_shipping,
        'total': subtotal - discount + initial_shipping,
    }
    return render(request, 'orders/checkout.html', context)


@transaction.atomic
def place_order_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in or create an account to place an order.')
        return redirect(f"{reverse('accounts:login')}?next={reverse('orders:checkout')}")

    if request.method != 'POST':
        return redirect('orders:checkout')

    cart = Cart(request)
    if cart.is_empty():
        messages.error(request, 'Your cart is empty.')
        return redirect('catalog:product_list')

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please check all required fields in the delivery form.')
        subtotal = cart.get_subtotal()
        discount = cart.discount_amount
        return render(request, 'orders/checkout.html', {
            'form': form,
            'cart': cart,
            'subtotal': subtotal,
            'discount': discount,
            'shipping_price': Decimal('100.00'),
            'total': subtotal - discount + Decimal('100.00'),
        })

    cd = form.cleaned_data
    subtotal = cart.get_subtotal()
    discount = cart.discount_amount

    method = cd['shipping_method']
    shipping_price = Decimal(str(SHIPPING_PRICES.get(method, 0)))
    if method == 'inside_dhaka' and subtotal >= Decimal('50000.00'):
        shipping_price = Decimal('0.00')

    total_price = subtotal - discount + shipping_price

    cart_items_data = list(cart)
    for item in cart_items_data:
        product = Product.objects.select_for_update().get(id=item['product'].id)
        if product.count_in_stock < item['qty']:
            messages.error(request, f'Sorry, "{product.name}" only has {product.count_in_stock} items remaining in stock.')
            return redirect('cart:cart_detail')
        product.count_in_stock -= item['qty']
        product.save()

    shipping_address = {
        'fullName': cd['full_name'],
        'phone': cd['phone'],
        'email': cd['email'],
        'division': cd['division'],
        'district': cd['district'],
        'street': cd['street_address'],
        'postalCode': cd.get('postal_code', ''),
        'notes': cd.get('delivery_notes', ''),
    }

    if cd['payment_method'] == 'card':
        card_raw = cd.get('card_number', '').replace(' ', '').replace('-', '')
        masked_card = f'**** **** **** {card_raw[-4:]}' if len(card_raw) >= 4 else 'Card Payment'
        payment_result = {
            'status': 'Authorized (Online Banking / Card)',
            'cardHolder': cd.get('card_name', ''),
            'maskedCard': masked_card,
            'cardBank': cd.get('card_bank', '') or 'Online Card/Bank',
            'timestamp': timezone.now().isoformat(),
        }
    elif cd['payment_method'] in ['bkash', 'nagad']:
        payment_result = {
            'status': f"Submitted ({cd['payment_method'].upper()})",
            'transactionId': cd.get('trx_id', '').strip().upper(),
            'senderNumber': cd.get('sender_number', '').strip(),
            'timestamp': timezone.now().isoformat(),
        }
    else:
        payment_result = {
            'status': 'Cash on Delivery (Pay at Doorstep)',
            'timestamp': timezone.now().isoformat(),
        }

    coupon_obj = None
    if cart.coupon_code:
        coupon_obj = Coupon.objects.filter(code__iexact=cart.coupon_code).first()

    initial_timeline = [
        {
            'status': 'Pending',
            'note': 'Order received and logged in Orient system. Awaiting warehouse confirmation.',
            'timestamp': timezone.now().isoformat(),
        }
    ]

    tracking_number = generate_tracking_number()
    while Order.objects.filter(tracking_number=tracking_number).exists():
        tracking_number = generate_tracking_number()

    order = Order.objects.create(
        user=request.user,
        tracking_number=tracking_number,
        shipping_address=shipping_address,
        shipping_method=method,
        shipping_price=shipping_price,
        payment_method=cd['payment_method'],
        payment_result=payment_result,
        items_price=subtotal,
        discount_amount=discount,
        total_price=total_price,
        order_status='Pending',
        status_timeline=initial_timeline,
        coupon=coupon_obj,
    )

    for item in cart_items_data:
        product = item['product']
        OrderItem.objects.create(
            order=order,
            product=product,
            name=product.name,
            image_url=product.primary_image_url,
            price=item['price'],
            qty=item['qty'],
        )

    cart.clear()

    messages.success(request, f'Your order has been placed successfully! Tracking Number: {order.tracking_number}')
    return redirect('orders:order_confirmation', tracking_number=order.tracking_number)


def order_confirmation_view(request, tracking_number):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), tracking_number=tracking_number)
    return render(request, 'orders/confirmation.html', {'order': order})


def public_track_order_view(request):
    order = None
    tracking_number = (request.POST.get('tracking_number') or request.GET.get('tracking_number', '')).strip().upper()
    phone = (request.POST.get('phone') or request.GET.get('phone', '')).strip()

    form = PublicOrderTrackForm(initial={'tracking_number': tracking_number, 'phone': phone})

    if tracking_number:
        found_order = Order.objects.prefetch_related('items__product').filter(tracking_number=tracking_number).first()
        if found_order:
            if phone:
                order_phone = str(found_order.shipping_address.get('phone', ''))
                order_digits = ''.join(filter(str.isdigit, order_phone))
                input_digits = ''.join(filter(str.isdigit, phone))
                # Match last 10 digits for Bangladeshi mobile numbers (01XXXXXXXXX / 8801XXXXXXXXX)
                if input_digits and (input_digits[-10:] in order_digits or order_digits[-10:] in input_digits):
                    order = found_order
                else:
                    order = None
                    messages.error(request, 'The provided mobile phone number does not match the registered order contact.')
            else:
                order = found_order
        else:
            messages.error(request, f'No order found with tracking number "{tracking_number}". Please verify your tracking code.')

    return render(request, 'orders/track_order.html', {
        'form': form,
        'order': order,
        'tracking_number': tracking_number,
        'phone': phone,
    })


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, tracking_number):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), tracking_number=tracking_number)
    if order.user != request.user and not request.user.is_staff and request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('orders:order_history')

    return render(request, 'orders/order_detail.html', {'order': order})


def print_invoice_view(request, tracking_number):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), tracking_number=tracking_number)
    return render(request, 'orders/invoice.html', {'order': order})
