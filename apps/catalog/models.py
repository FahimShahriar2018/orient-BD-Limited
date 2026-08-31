from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Product category with optional parent for subcategory hierarchy."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='children'
    )
    icon = models.CharField(max_length=60, blank=True, help_text='Bootstrap icon class e.g. bi-laptop')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_list') + f'?category={self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_product_count(self):
        return self.products.filter(count_in_stock__gt=0).count()


class Brand(models.Model):
    """Official hardware and solutions brand / partner."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=120)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    logo_url = models.URLField(max_length=1000, blank=True, help_text='Online logo image URL')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:brand_detail', kwargs={'slug': self.slug})

    @property
    def letter(self):
        return self.name[0].upper() if self.name else '#'

    @property
    def logo_display_url(self):
        if self.logo_url:
            return self.logo_url
        if self.logo:
            try:
                return self.logo.url
            except Exception:
                pass
        return '/static/images/placeholder-brand.png'


class Product(models.Model):
    """Hardware product with full specs, pricing and stock tracking."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=280)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    count_in_stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    short_specs = models.JSONField(default=list, blank=True,
                                   help_text='List of quick-spec bullet strings')
    technical_specs = models.JSONField(default=dict, blank=True,
                                       help_text='Dict of spec_key: spec_value pairs')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    num_reviews = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_deal_of_day = models.BooleanField(default=False)
    is_call_for_price = models.BooleanField(default=False, help_text='Mark True for enterprise hardware where price is on quotation')
    is_upcoming = models.BooleanField(default=False, help_text='Preview item coming soon')
    warranty = models.CharField(max_length=150, default='1 Year Official Brand Warranty')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        """Return discounted price if set, otherwise regular price."""
        if self.discount_price and self.discount_price > 0:
            return self.discount_price
        return self.price

    @property
    def discount_percentage(self):
        """Return integer % saved (0 if no discount)."""
        if self.discount_price and self.discount_price > 0 and self.price > 0:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.count_in_stock > 0

    @property
    def primary_image(self):
        img = self.images.order_by('display_order').first()
        return img if img else None

    @property
    def primary_image_url(self):
        img = self.images.order_by('display_order').first()
        if img:
            return img.url
        return '/static/images/placeholder-product.png'


class ProductImage(models.Model):
    """Multiple images per product, supporting local uploads or online URLs."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, help_text='Online image URL')
    alt_text = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f'{self.product.name} — image {self.display_order}'

    @property
    def url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        return '/static/images/placeholder-product.png'


class Review(models.Model):
    """Customer review for a product (one per user per product)."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — {self.product.name} ({self.rating}★)'
