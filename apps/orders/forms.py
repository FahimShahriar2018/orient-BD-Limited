from django import forms
from .bd_geodata import ALL_DIVISIONS


class CheckoutForm(forms.Form):
    # Customer Details
    full_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'})
    )

    # Address Cascade (REQ-F-CHK-02)
    division = forms.ChoiceField(
        choices=[('', 'Select Division')] + [(d, d) for d in ALL_DIVISIONS],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_division'})
    )
    district = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter delivery address (House, Road, Area)'})
    )
    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'})
    )
    delivery_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter delivery instructions or landmark (optional)'})
    )

    # Shipping Method (REQ-F-CHK-03)
    shipping_method = forms.ChoiceField(
        choices=[
            ('inside_dhaka', 'Standard Delivery Inside Dhaka (৳100)'),
            ('outside_dhaka', 'Outside Dhaka Courier (Sundarban / Steadfast) (৳200)'),
            ('express', 'Express Same-Day Priority Delivery (৳300)'),
            ('pickup', 'Orient Showroom Pickup (Motijheel, Dhaka) (FREE)'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    # Payment Method (REQ-F-CHK-04)
    payment_method = forms.ChoiceField(
        choices=[
            ('cod', 'Cash on Delivery (COD)'),
            ('bkash', 'bKash Mobile Banking'),
            ('nagad', 'Nagad Mobile Banking'),
            ('card', 'Online Bank / Credit Card'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    # MFS Transaction Details
    trx_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control text-uppercase font-monospace', 'placeholder': 'Enter transaction ID (TrxID)'})
    )
    sender_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sender mobile number'})
    )

    # Online Bank / Card Details
    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control font-monospace', 'placeholder': 'Enter 16-digit card number', 'maxlength': '19', 'id': 'id_card_number'})
    )
    card_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cardholder name', 'id': 'id_card_name'})
    )
    card_expiry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control text-center font-monospace', 'placeholder': 'MM/YY', 'maxlength': '5', 'id': 'id_card_expiry'})
    )
    card_cvv = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control text-center font-monospace', 'placeholder': 'CVV', 'maxlength': '4', 'id': 'id_card_cvv'}, render_value=True)
    )
    card_bank = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bank / card type (e.g. Visa, Mastercard, DBBL Nexus)', 'id': 'id_card_bank'})
    )


class PublicOrderTrackForm(forms.Form):
    tracking_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg text-uppercase font-monospace', 'placeholder': 'Enter tracking number (e.g. ORIENT-2026-XXXXXX)'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter recipient mobile number (e.g. 01XXXXXXXXX)'})
    )
