from django.contrib import admin
from .models import Coupon, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['line_total']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'min_order_value', 'is_active', 'valid_to']
    list_filter = ['is_active', 'discount_type']
    search_fields = ['code']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'order_status', 'payment_method', 'total_price', 'created_at']
    list_filter = ['order_status', 'payment_method', 'shipping_method']
    search_fields = ['tracking_number']
    readonly_fields = ['tracking_number', 'created_at']
    inlines = [OrderItemInline]
