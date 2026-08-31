from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from apps.catalog.models import Category, Product, Brand
from apps.service.models import Branch
from apps.cart.cart import Cart
from apps.orders.bd_geodata import get_districts


def home_view(request):
    categories = Category.objects.filter(parent=None).prefetch_related('products')
    deal_products = Product.objects.filter(is_deal_of_day=True, count_in_stock__gt=0)[:4]
    featured_products = Product.objects.filter(is_featured=True, count_in_stock__gt=0)[:8]
    new_arrivals = Product.objects.filter(is_upcoming=False, count_in_stock__gt=0).order_by('-created_at')[:10]
    upcoming_products = Product.objects.filter(is_upcoming=True).order_by('-created_at')[:10]
    top_selling = Product.objects.filter(count_in_stock__gt=0).order_by('-num_reviews', '-rating')[:8]
    brands = Brand.objects.all().order_by('name')

    now = timezone.now()
    end_of_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    countdown_target = end_of_day.isoformat()

    context = {
        'departments': categories,
        'deal_products': deal_products,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'upcoming_products': upcoming_products,
        'top_selling': top_selling,
        'brands': brands,
        'countdown_target': countdown_target,
    }
    return render(request, 'home/index.html', context)


def search_api(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(brand__icontains=query) |
        Q(sku__icontains=query) |
        Q(category__name__icontains=query)
    ).select_related('category').prefetch_related('images')

    if category_slug and category_slug != 'all':
        products = products.filter(
            Q(category__slug=category_slug) | Q(category__parent__slug=category_slug)
        )

    results = []
    for p in products[:8]:
        results.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'brand': p.brand,
            'category': p.category.name,
            'price': float(p.price),
            'discount_price': float(p.discount_price) if p.discount_price else 0,
            'image_url': p.primary_image_url,
            'in_stock': p.count_in_stock > 0,
            'url': p.get_absolute_url(),
        })

    return JsonResponse({'results': results})


def districts_api(request):
    division = request.GET.get('division', '').strip()
    districts = get_districts(division)
    return JsonResponse({'districts': districts})


def cart_drawer_api(request):
    cart = Cart(request)
    items = []
    for item in cart:
        product = item['product']
        items.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'url': product.get_absolute_url(),
            'price': float(item['price']),
            'qty': item['qty'],
            'total': float(item['total']),
            'image_url': product.primary_image_url,
        })

    subtotal = float(cart.get_subtotal())
    discount = float(cart.discount_amount)
    total = float(cart.get_total())
    free_shipping_threshold = 50000.0
    free_shipping_progress = min(100.0, (subtotal / free_shipping_threshold) * 100) if free_shipping_threshold > 0 else 100.0
    amount_needed_for_free_shipping = max(0.0, free_shipping_threshold - subtotal)

    return JsonResponse({
        'items': items,
        'count': cart.get_item_count(),
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'free_shipping_threshold': free_shipping_threshold,
        'free_shipping_progress': round(free_shipping_progress, 1),
        'amount_needed_for_free_shipping': amount_needed_for_free_shipping,
    })
