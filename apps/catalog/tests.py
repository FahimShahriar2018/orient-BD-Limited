from django.test import TestCase
from decimal import Decimal
from apps.catalog.models import Category, Product
from apps.orders.models import Coupon, Order
from apps.orders.utils import generate_tracking_number


class CatalogModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Processors', slug='processors')
        self.product = Product.objects.create(
            name='AMD Ryzen 7 7800X3D',
            sku='CPU-AMD-7800X3D',
            brand='AMD',
            category=self.category,
            price=Decimal('50000.00'),
            discount_price=Decimal('45000.00'),
            count_in_stock=10,
            description='Top tier gaming CPU'
        )

    def test_effective_price_with_discount(self):
        self.assertEqual(self.product.effective_price, Decimal('45000.00'))

    def test_discount_percentage_calculation(self):
        self.assertEqual(self.product.discount_percentage, 10)

    def test_in_stock_property(self):
        self.assertTrue(self.product.is_in_stock)


class OrderModelTests(TestCase):
    def test_tracking_number_generation_format(self):
        code = generate_tracking_number()
        self.assertTrue(code.startswith('ORIENT-'))
        self.assertEqual(len(code.split('-')), 3)

    def test_coupon_discount_calculation(self):
        from django.utils import timezone
        from datetime import timedelta
        coupon = Coupon.objects.create(
            code='TEST10',
            discount_type='percent',
            discount_value=Decimal('10.00'),
            min_order_value=Decimal('1000.00'),
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1),
            is_active=True
        )
        discount = coupon.apply(Decimal('5000.00'))
        self.assertEqual(discount, Decimal('500.00'))
