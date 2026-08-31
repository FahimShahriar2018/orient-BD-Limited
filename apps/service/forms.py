from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'phone', 'order_reference', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 1XXXXXXXXX'}),
            'order_reference': forms.TextInput(attrs={'class': 'form-control font-monospace', 'placeholder': 'ORIENT-2026-XXXXXX (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RMA Warranty Claim for GPU / Courier Delay'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your issue, serial number, or warranty requirement in detail...'}),
        }
