"""
Order utility functions: tracking code generation, invoice helpers.
"""
import random
import string
from datetime import datetime


def generate_tracking_number():
    """Generate unique ORIENT-YYYY-XXXXXX tracking code."""
    year = datetime.now().year
    suffix = ''.join(random.choices(string.digits, k=6))
    return f'ORIENT-{year}-{suffix}'


def format_bdt(amount):
    """Format Decimal/float as ৳ string with commas."""
    try:
        return f'৳{int(amount):,}'
    except (TypeError, ValueError):
        return '৳0'
