from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
from apps.catalog.models import Product
from apps.orders.models import Coupon
from .cart import Cart
from .wishlist import Wishlist


def cart_detail(request):
    cart = Cart(request)
    subtotal = cart.get_subtotal()
    free_shipping_threshold = Decimal('50000.00')
    progress = min(Decimal('100.00'), (subtotal / free_shipping_threshold) * 100) if free_shipping_threshold > 0 else Decimal('100.00')
    amount_needed = max(Decimal('0.00'), free_shipping_threshold - subtotal)

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'discount': cart.discount_amount,
        'total': cart.get_total(),
        'free_shipping_threshold': free_shipping_threshold,
        'free_shipping_progress': float(progress),
        'amount_needed_for_free_shipping': amount_needed,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    qty = int(request.POST.get('qty', 1))

    product = get_object_or_404(Product, id=product_id)

    if product.count_in_stock < qty:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.META.get('HTTP_ACCEPT', ''):
            return JsonResponse({'success': False, 'message': 'Insufficient inventory in stock.'})
        messages.error(request, 'Requested quantity exceeds available stock.')
        return redirect(product.get_absolute_url())

    cart.add(product=product, qty=qty)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.META.get('HTTP_ACCEPT', ''):
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" added to shopping basket!',
            'cart_count': cart.get_item_count(),
            'subtotal': float(cart.get_subtotal()),
        })

    messages.success(request, f'Added {product.name} to your basket.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    qty = int(request.POST.get('qty', 1))

    cart.update(product_id=product_id, qty=qty)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.META.get('HTTP_ACCEPT', ''):
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'subtotal': float(cart.get_subtotal()),
            'total': float(cart.get_total()),
        })

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    cart.remove(product_id=product_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.META.get('HTTP_ACCEPT', ''):
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'subtotal': float(cart.get_subtotal()),
            'total': float(cart.get_total()),
        })

    messages.info(request, 'Item removed from your cart.')
    return redirect('cart:cart_detail')


@require_POST
def apply_coupon_view(request):
    code = request.POST.get('code', '').strip().upper()
    cart = Cart(request)
    subtotal = cart.get_subtotal()

    if not code:
        messages.warning(request, 'Please enter a valid coupon code.')
        return redirect('cart:cart_detail')

    success, msg, discount = cart.apply_coupon(code, subtotal)
    if success:
        messages.success(request, msg)
    else:
        messages.error(request, msg)

    return redirect('cart:cart_detail')


def remove_coupon_view(request):
    cart = Cart(request)
    cart.remove_coupon()
    messages.info(request, 'Coupon removed.')
    return redirect('cart:cart_detail')


def wishlist_view(request):
    wishlist = Wishlist(request)
    products = wishlist.get_products().prefetch_related('images')
    return render(request, 'cart/wishlist.html', {'products': products})


@require_POST
def wishlist_toggle(request):
    product_id = request.POST.get('product_id')
    wishlist = Wishlist(request)
    added = wishlist.toggle(product_id)

    return JsonResponse({
        'success': True,
        'action': 'added' if added else 'removed',
        'wishlist_count': wishlist.count(),
    })


@require_POST
def wishlist_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    wishlist = Wishlist(request)

    if product.is_in_stock:
        cart.add(product, qty=1)
        wishlist.remove(product.id)
        messages.success(request, f'"{product.name}" migrated to your shopping cart!')
    else:
        messages.error(request, f'"{product.name}" is currently out of stock.')

    return redirect('cart:wishlist_view')


def buy_now(request, product_id):
    """Add product directly to cart and redirect immediately to checkout (1-click Order Now)."""
    product = get_object_or_404(Product, id=product_id)
    try:
        qty = int(request.POST.get('qty', request.GET.get('qty', 1)))
    except (ValueError, TypeError):
        qty = 1

    if product.is_call_for_price:
        messages.info(request, f'"{product.name}" is an enterprise quotation item. Please call our hotline at 09642222224.')
        return redirect(product.get_absolute_url())

    if product.count_in_stock < qty:
        messages.error(request, 'Requested quantity exceeds available stock.')
        return redirect(product.get_absolute_url())

    cart = Cart(request)
    cart.add(product=product, qty=qty)
    return redirect('orders:checkout')

