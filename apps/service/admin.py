from django.contrib import admin
from .models import Branch, Complaint


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_flagship', 'display_order']
    list_editable = ['display_order', 'is_flagship']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'order_reference']
