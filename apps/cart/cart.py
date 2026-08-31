"""
Session-based shopping cart.
Stores cart data in request.session['cart'] as:
    { '<product_id>': { 'qty': N, 'price': '<str decimal>' } }
"""
from decimal import Decimal
from apps.catalog.models import Product

CART_SESSION_KEY = 'cart'
COUPON_SESSION_KEY = 'coupon'
DISCOUNT_SESSION_KEY = 'discount'


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_KEY, {})
        self.coupon_code = self.session.get(COUPON_SESSION_KEY)
        self.discount_amount = Decimal(str(self.session.get(DISCOUNT_SESSION_KEY, '0')))

    def add(self, product, qty=1, update_qty=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {
                'qty': 0,
                'price': str(product.effective_price),
            }
        if update_qty:
            self.cart[pid]['qty'] = max(1, qty)
        else:
            self.cart[pid]['qty'] += qty
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def update(self, product_id, qty):
        pid = str(product_id)
        if pid in self.cart:
            if qty <= 0:
                self.remove(pid)
            else:
                self.cart[pid]['qty'] = qty
                self.save()

    def clear(self):
        for key in [CART_SESSION_KEY, COUPON_SESSION_KEY, DISCOUNT_SESSION_KEY]:
            self.session.pop(key, None)
        self.session.modified = True

    def save(self):
        self.session.modified = True

    def apply_coupon(self, code, subtotal):
        """Validate and apply a coupon. Returns (success, message, discount_amount)."""
        from apps.orders.models import Coupon
        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return False, 'Invalid coupon code.', Decimal('0')
        if not coupon.is_valid():
            return False, 'Coupon has expired or is inactive.', Decimal('0')
        if subtotal < coupon.min_order_value:
            return False, f'Minimum order ৳{int(coupon.min_order_value):,} required.', Decimal('0')
        discount = Decimal(str(coupon.apply(subtotal)))
        self.session[COUPON_SESSION_KEY] = coupon.code
        self.session[DISCOUNT_SESSION_KEY] = str(discount)
        self.discount_amount = discount
        self.save()
        return True, f'Coupon applied! You save ৳{int(discount):,}.', discount

    def remove_coupon(self):
        self.session.pop(COUPON_SESSION_KEY, None)
        self.session.pop(DISCOUNT_SESSION_KEY, None)
        self.discount_amount = Decimal('0')
        self.save()

    def __iter__(self):
        """Yield enriched cart items with product objects attached."""
        pids = self.cart.keys()
        products = {str(p.id): p for p in Product.objects.filter(id__in=pids)}
        for pid, item in self.cart.items():
            product = products.get(pid)
            if not product:
                continue
            yield {
                'product': product,
                'qty': item['qty'],
                'price': Decimal(item['price']),
                'total': Decimal(item['price']) * item['qty'],
            }

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def get_item_count(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_total(self, shipping_price=Decimal('0')):
        return self.get_subtotal() - self.discount_amount + Decimal(str(shipping_price))

    def is_empty(self):
        return len(self.cart) == 0
