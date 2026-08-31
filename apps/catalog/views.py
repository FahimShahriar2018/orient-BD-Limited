from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review, Brand
from .forms import ReviewForm


def product_list_view(request):
    queryset = Product.objects.all().select_related('category').prefetch_related('images')

    # Search Query
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    # Category Filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug and category_slug != 'all':
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            queryset = queryset.filter(
                Q(category=selected_category) | Q(category__parent=selected_category)
            )

    # Brand Filter
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        queryset = queryset.filter(brand__in=selected_brands)

    # Price Range
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price.isdigit():
        queryset = queryset.filter(price__gte=int(min_price))
    if max_price.isdigit():
        queryset = queryset.filter(price__lte=int(max_price))

    # In-Stock Only
    in_stock_only = request.GET.get('in_stock', '').strip()
    if in_stock_only == '1':
        queryset = queryset.filter(count_in_stock__gt=0)

    # Deal / Featured / Upcoming
    if request.GET.get('deal') == '1':
        queryset = queryset.filter(is_deal_of_day=True)
    if request.GET.get('featured') == '1':
        queryset = queryset.filter(is_featured=True)
    if request.GET.get('upcoming') == '1':
        queryset = queryset.filter(is_upcoming=True)

    # Rating
    min_rating = request.GET.get('rating', '').strip()
    if min_rating.isdigit():
        queryset = queryset.filter(rating__gte=int(min_rating))

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'rating':
        queryset = queryset.order_by('-rating', '-num_reviews')
    elif sort_by == 'popular':
        queryset = queryset.order_by('-num_reviews')
    else:
        queryset = queryset.order_by('-created_at')

    all_categories = Category.objects.filter(parent=None).prefetch_related('children')
    available_brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'total_count': paginator.count,
        'all_categories': all_categories,
        'selected_category': selected_category,
        'available_brands': available_brands,
        'selected_brands': selected_brands,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_only': in_stock_only,
        'min_rating': min_rating,
        'sort_by': sort_by,
        'query_params': query_params.urlencode(),
    }
    return render(request, 'catalog/product_list.html', context)


def brand_list_view(request):
    """Official brand partner directory with A-Z filtering."""
    brands = Brand.objects.all().order_by('name')
    letters = sorted(list(set(b.name[0].upper() for b in brands if b.name)))
    selected_letter = request.GET.get('letter', 'all').upper()

    if selected_letter != 'ALL' and selected_letter in letters:
        filtered_brands = brands.filter(name__istartswith=selected_letter)
    else:
        filtered_brands = brands
        selected_letter = 'ALL'

    context = {
        'brands': filtered_brands,
        'all_brands': brands,
        'letters': letters,
        'selected_letter': selected_letter,
        'total_brands': brands.count(),
    }
    return render(request, 'catalog/brand_list.html', context)


def brand_detail_view(request, slug):
    """View all products by a specific brand."""
    brand_obj = get_object_or_404(Brand, slug=slug)
    products_qs = Product.objects.filter(
        Q(brand__iexact=brand_obj.name) | Q(name__icontains=brand_obj.name)
    ).select_related('category').prefetch_related('images').order_by('-created_at')

    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'brand': brand_obj,
        'products': page_obj,
        'page_obj': page_obj,
        'total_count': paginator.count,
    }
    return render(request, 'catalog/brand_detail.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images', 'reviews__user'),
        slug=slug
    )

    # Check if a matching Brand object exists
    brand_obj = Brand.objects.filter(name__iexact=product.brand).first()

    reviews = product.reviews.all()
    total_reviews = reviews.count()
    star_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in reviews:
        if r.rating in star_distribution:
            star_distribution[r.rating] += 1

    star_percentages = {}
    for star, count in star_distribution.items():
        star_percentages[star] = round((count / total_reviews * 100), 1) if total_reviews > 0 else 0

    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()

    review_form = ReviewForm()

    related_products = Product.objects.filter(
        category=product.category,
        count_in_stock__gt=0
    ).exclude(id=product.id).prefetch_related('images')[:4]

    canonical_url = request.build_absolute_uri(product.get_absolute_url())

    context = {
        'product': product,
        'brand_obj': brand_obj,
        'images': product.images.all(),
        'reviews': reviews,
        'total_reviews': total_reviews,
        'star_distribution': star_distribution,
        'star_percentages': star_percentages,
        'user_has_reviewed': user_has_reviewed,
        'review_form': review_form,
        'related_products': related_products,
        'canonical_url': canonical_url,
    }
    return render(request, 'catalog/product_detail.html', context)


@login_required
def submit_review_view(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        existing = Review.objects.filter(product=product, user=request.user).first()
        if existing:
            messages.warning(request, 'You have already submitted a review for this hardware product.')
            return redirect(product.get_absolute_url())

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            agg = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'), count=Count('id'))
            product.rating = round(agg['avg_rating'] or 0, 1)
            product.num_reviews = agg['count'] or 0
            product.save()

            messages.success(request, 'Thank you! Your verified product review has been published.')
        else:
            messages.error(request, 'Please correct the errors in the review form.')

    return redirect(product.get_absolute_url())
