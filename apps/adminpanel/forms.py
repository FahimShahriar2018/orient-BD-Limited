from django import forms
from apps.catalog.models import Product


class ProductAdminForm(forms.ModelForm):
    short_specs_raw = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'One highlight bullet per line\ne.g. 16 Cores, 32 Threads\nUp to 5.7 GHz Boost Clock'}),
        help_text='Enter quick-spec bullet highlights, one per line.'
    )
    primary_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text='Upload main display image.'
    )
    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/product.jpg'}),
        help_text='Or enter direct online product image URL.'
    )

    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'brand', 'category', 'price', 'discount_price',
            'count_in_stock', 'warranty', 'is_featured', 'is_deal_of_day',
            'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Product Name'}),
            'sku': forms.TextInput(attrs={'class': 'form-control text-uppercase font-monospace', 'placeholder': 'e.g. CPU-RYZ-7800X3D'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ASUS, MSI, AMD, Intel'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Regular BDT Price'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discounted Price (or 0)'}),
            'count_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock quantity'}),
            'warranty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3 Years Official Warranty'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_deal_of_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
