from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model with phone, role, and saved address."""

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]

    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    # Saved default delivery address
    address_street = models.TextField(blank=True)
    address_division = models.CharField(max_length=50, blank=True)
    address_district = models.CharField(max_length=50, blank=True)
    address_postal = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email or self.username

    def is_admin_user(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser
