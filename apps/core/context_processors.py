"""
Context processors: inject cart count, categories, and wishlist count
into every template automatically.
"""
from apps.cart.cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': cart.get_item_count(),
    }


def categories_context(request):
    from apps.catalog.models import Category
    nav_categories = Category.objects.filter(parent=None).prefetch_related('children')
    return {'nav_categories': nav_categories}


def wishlist_context(request):
    wishlist = request.session.get('wishlist', [])
    return {'wishlist_count': len(wishlist)}
