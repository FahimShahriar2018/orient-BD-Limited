"""
Session-based Wishlist management.
Stores product IDs in request.session['wishlist'] as a list of IDs.
"""
from apps.catalog.models import Product

WISHLIST_SESSION_KEY = 'wishlist'


class Wishlist:
    def __init__(self, request):
        self.session = request.session
        self.wishlist = self.session.setdefault(WISHLIST_SESSION_KEY, [])

    def add(self, product_id):
        pid = int(product_id)
        if pid not in self.wishlist:
            self.wishlist.append(pid)
            self.save()
            return True
        return False

    def remove(self, product_id):
        pid = int(product_id)
        if pid in self.wishlist:
            self.wishlist.remove(pid)
            self.save()
            return True
        return False

    def toggle(self, product_id):
        pid = int(product_id)
        if pid in self.wishlist:
            self.wishlist.remove(pid)
            self.save()
            return False  # Removed
        else:
            self.wishlist.append(pid)
            self.save()
            return True  # Added

    def has_product(self, product_id):
        return int(product_id) in self.wishlist

    def get_products(self):
        return Product.objects.filter(id__in=self.wishlist)

    def count(self):
        return len(self.wishlist)

    def clear(self):
        self.session.pop(WISHLIST_SESSION_KEY, None)
        self.session.modified = True

    def save(self):
        self.session.modified = True
