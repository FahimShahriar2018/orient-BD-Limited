from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='bdt')
def bdt_format(value):
    """Format currency as Bangladeshi Taka (৳ 123,456) with commas."""
    if value is None or value == '':
        return '৳ 0'
    try:
        val = Decimal(str(value))
        if val % 1 == 0:
            return f"৳ {int(val):,}"
        return f"৳ {val:,.2f}"
    except (ValueError, TypeError):
        return f"৳ {value}"


@register.filter(name='discount_calc')
def discount_calc(price, discount_price):
    """Calculate percentage savings between regular and discount price."""
    try:
        p = float(price)
        dp = float(discount_price)
        if dp > 0 and p > dp:
            return int(round(((p - dp) / p) * 100))
    except (ValueError, TypeError, ZeroDivisionError):
        pass
    return 0


@register.filter(name='range_stars')
def range_stars(number):
    """Return a range up to int(number) for star rendering."""
    try:
        return range(int(number or 0))
    except (ValueError, TypeError):
        return range(0)


@register.filter(name='empty_stars')
def empty_stars(number):
    """Return range for empty stars (5 - rating)."""
    try:
        return range(max(0, 5 - int(number or 0)))
    except (ValueError, TypeError):
        return range(5)


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Safe dict key lookup in templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
