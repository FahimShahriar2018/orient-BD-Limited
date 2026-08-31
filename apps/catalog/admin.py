from django.contrib import admin
from .models import Category, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'brand', 'category', 'price',
                    'discount_price', 'count_in_stock', 'is_featured', 'is_deal_of_day']
    list_filter = ['category', 'brand', 'is_featured', 'is_deal_of_day']
    search_fields = ['name', 'sku', 'brand']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_editable = ['price', 'discount_price', 'count_in_stock', 'is_featured', 'is_deal_of_day']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['product__name', 'user__email']
