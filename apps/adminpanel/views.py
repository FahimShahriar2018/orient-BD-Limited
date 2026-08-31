from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import json

from .decorators import admin_required
from .forms import ProductAdminForm
from apps.catalog.models import Product, Category, ProductImage
from apps.orders.models import Order
from apps.accounts.models import User


@admin_required
def dashboard_view(request):
    total_sales = Order.objects.exclude(order_status='Cancelled').aggregate(total=Sum('total_price'))['total'] or 0
    total_orders = Order.objects.count()
    active_skus = Product.objects.filter(count_in_stock__gt=0).count()
    total_customers = User.objects.filter(role='customer').count()

    recent_orders = Order.objects.order_by('-created_at')[:6]

    today = timezone.now().date()
    days_labels = []
    revenue_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        days_labels.append(day.strftime('%b %d'))
        day_sum = Order.objects.filter(
            created_at__date=day
        ).exclude(order_status='Cancelled').aggregate(s=Sum('total_price'))['s'] or 0
        revenue_data.append(float(day_sum))

    status_counts = {
        'Pending': Order.objects.filter(order_status='Pending').count(),
        'Confirmed': Order.objects.filter(order_status='Confirmed').count(),
        'Processing': Order.objects.filter(order_status='Processing').count(),
        'Shipped': Order.objects.filter(order_status='Shipped').count(),
        'Delivered': Order.objects.filter(order_status='Delivered').count(),
    }

    low_stock_products = Product.objects.filter(count_in_stock__lt=5).order_by('count_in_stock')[:5]

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'active_skus': active_skus,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'days_labels_json': json.dumps(days_labels),
        'revenue_data_json': json.dumps(revenue_data),
        'status_counts_json': json.dumps(status_counts),
    }
    return render(request, 'adminpanel/dashboard.html', context)


@admin_required
def product_list_view(request):
    queryset = Product.objects.select_related('category').prefetch_related('images').order_by('-created_at')

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) | Q(sku__icontains=q) | Q(brand__icontains=q)
        )

    cat_slug = request.GET.get('category', '').strip()
    if cat_slug:
        queryset = queryset.filter(category__slug=cat_slug)

    stock_filter = request.GET.get('stock', '').strip()
    if stock_filter == 'low':
        queryset = queryset.filter(count_in_stock__lt=5, count_in_stock__gt=0)
    elif stock_filter == 'out':
        queryset = queryset.filter(count_in_stock=0)

    paginator = Paginator(queryset, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.all()

    return render(request, 'adminpanel/products.html', {
        'page_obj': page_obj,
        'categories': categories,
        'q': q,
        'cat_slug': cat_slug,
        'stock_filter': stock_filter,
    })


@admin_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            raw_bullets = form.cleaned_data.get('short_specs_raw', '')
            product.short_specs = [b.strip() for b in raw_bullets.split('\n') if b.strip()]

            spec_keys = request.POST.getlist('spec_keys[]')
            spec_values = request.POST.getlist('spec_values[]')
            specs_dict = {}
            for k, v in zip(spec_keys, spec_values):
                if k.strip() and v.strip():
                    specs_dict[k.strip()] = v.strip()
            product.technical_specs = specs_dict
            product.save()

            if 'primary_image' in request.FILES:
                ProductImage.objects.create(
                    product=product,
                    image=request.FILES['primary_image'],
                    display_order=0
                )
            elif form.cleaned_data.get('image_url'):
                ProductImage.objects.create(
                    product=product,
                    image_url=form.cleaned_data['image_url'],
                    display_order=0
                )

            messages.success(request, f'Product "{product.name}" created successfully with SKU {product.sku}.')
            return redirect('adminpanel:products')
    else:
        form = ProductAdminForm()

    return render(request, 'adminpanel/product_form.html', {
        'form': form,
        'action_title': 'Add New Hardware SKU',
        'existing_specs': {},
    })


@admin_required
def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

            raw_bullets = form.cleaned_data.get('short_specs_raw', '')
            product.short_specs = [b.strip() for b in raw_bullets.split('\n') if b.strip()]

            spec_keys = request.POST.getlist('spec_keys[]')
            spec_values = request.POST.getlist('spec_values[]')
            specs_dict = {}
            for k, v in zip(spec_keys, spec_values):
                if k.strip() and v.strip():
                    specs_dict[k.strip()] = v.strip()
            product.technical_specs = specs_dict
            product.save()

            if 'primary_image' in request.FILES:
                ProductImage.objects.create(
                    product=product,
                    image=request.FILES['primary_image'],
                    display_order=0
                )
            elif form.cleaned_data.get('image_url'):
                ProductImage.objects.create(
                    product=product,
                    image_url=form.cleaned_data['image_url'],
                    display_order=0
                )

            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('adminpanel:products')
    else:
        initial_bullets = '\n'.join(product.short_specs or [])
        form = ProductAdminForm(instance=product, initial={'short_specs_raw': initial_bullets})

    return render(request, 'adminpanel/product_form.html', {
        'form': form,
        'product': product,
        'action_title': f'Edit Product: {product.name}',
        'existing_specs': product.technical_specs or {},
    })


@admin_required
def product_delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" has been deleted from inventory.')
    return redirect('adminpanel:products')


@admin_required
def order_list_view(request):
    queryset = Order.objects.prefetch_related('items').order_by('-created_at')

    status = request.GET.get('status', '').strip()
    if status and status != 'all':
        queryset = queryset.filter(order_status=status)

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(tracking_number__icontains=q) |
            Q(shipping_address__phone__icontains=q) |
            Q(shipping_address__fullName__icontains=q)
        )

    paginator = Paginator(queryset, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'adminpanel/orders.html', {
        'page_obj': page_obj,
        'current_status': status,
        'q': q,
    })


@admin_required
def order_detail_view(request, tracking_number):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), tracking_number=tracking_number)
    return render(request, 'adminpanel/order_detail.html', {'order': order})


@admin_required
def order_advance_status_view(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number)
    if request.method == 'POST':
        custom_status = request.POST.get('target_status')
        note = request.POST.get('note', '').strip()

        if custom_status:
            order.order_status = custom_status
            timeline = order.status_timeline or []
            timeline.append({
                'status': custom_status,
                'note': note or f'Status updated to {custom_status} by admin {request.user.username}',
                'timestamp': timezone.now().isoformat(),
            })
            order.status_timeline = timeline
            if custom_status == 'Delivered':
                order.delivered_at = timezone.now()
            order.save()
            messages.success(request, f'Order {order.tracking_number} status set to {custom_status}.')
        else:
            new_status = order.advance_status(note=note or f'Advanced by admin {request.user.username}')
            messages.success(request, f'Order {order.tracking_number} advanced to {new_status}.')

    return redirect('adminpanel:order_detail', tracking_number=order.tracking_number)


@admin_required
def customer_list_view(request):
    customers = User.objects.annotate(
        order_count=Count('orders')
    ).order_by('-date_joined')

    q = request.GET.get('q', '').strip()
    if q:
        customers = customers.filter(
            Q(username__icontains=q) | Q(email__icontains=q) |
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(phone__icontains=q)
        )

    paginator = Paginator(customers, 20)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'adminpanel/customers.html', {
        'page_obj': page_obj,
        'q': q,
    })
