from django.db import models
from django.utils import timezone


ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
]

SHIPPING_METHOD_CHOICES = [
    ('inside_dhaka', 'Inside Dhaka Standard (৳100)'),
    ('outside_dhaka', 'Outside Dhaka Courier (৳200)'),
    ('express', 'Express Same-Day (৳300)'),
    ('pickup', 'Showroom Pickup (Free)'),
]

PAYMENT_METHOD_CHOICES = [
    ('cod', 'Cash on Delivery'),
    ('bkash', 'bKash Mobile Banking'),
    ('nagad', 'Nagad Mobile Banking'),
    ('card', 'Online Bank / Card'),
]

SHIPPING_PRICES = {
    'inside_dhaka': 100,
    'outside_dhaka': 200,
    'express': 300,
    'pickup': 0,
}


class Coupon(models.Model):
    """Promotional discount coupon codes."""

    DISCOUNT_TYPE_CHOICES = [
        ('percent', 'Percentage (%)'),
        ('flat', 'Flat Amount (৳)'),
    ]

    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()

    class Meta:
        ordering = ['-valid_to']

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to

    def apply(self, subtotal):
        """Return discount amount for the given subtotal."""
        if not self.is_valid() or subtotal < self.min_order_value:
            return 0
        if self.discount_type == 'percent':
            return round(subtotal * self.discount_value / 100, 2)
        return min(self.discount_value, subtotal)


class Order(models.Model):
    """Customer order with full shipping, payment, and fulfillment data."""

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders'
    )
    tracking_number = models.CharField(max_length=50, unique=True, db_index=True)
    shipping_address = models.JSONField()  # dict: fullName, phone, email, street, division, district, postal
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHOD_CHOICES)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_result = models.JSONField(default=dict, blank=True)
    # Prices
    items_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    # Status
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='Pending'
    )
    status_timeline = models.JSONField(default=list, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    # Timestamps
    paid_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.tracking_number

    def get_status_index(self):
        stages = ['Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered']
        try:
            return stages.index(self.order_status)
        except ValueError:
            return -1

    def advance_status(self, note=''):
        """Move the order to the next stage in the pipeline."""
        stages = ['Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered']
        idx = self.get_status_index()
        if idx < len(stages) - 1:
            new_status = stages[idx + 1]
            self.order_status = new_status
            timeline_entry = {
                'status': new_status,
                'note': note,
                'timestamp': timezone.now().isoformat(),
            }
            timeline = self.status_timeline or []
            timeline.append(timeline_entry)
            self.status_timeline = timeline
            if new_status == 'Delivered':
                self.delivered_at = timezone.now()
            self.save()
        return self.order_status


class OrderItem(models.Model):
    """Line item in an order (snapshot of product at time of purchase)."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.qty}× {self.name}'

    @property
    def line_total(self):
        return self.price * self.qty
