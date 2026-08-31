from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from apps.orders.bd_geodata import ALL_DIVISIONS


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 1711-000001'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email address already exists.')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserAddressForm(forms.ModelForm):
    address_division = forms.ChoiceField(
        choices=[('', 'Select Division')] + [(d, d) for d in ALL_DIVISIONS],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_division'})
    )

    class Meta:
        model = User
        fields = ['address_street', 'address_division', 'address_district', 'address_postal']
        widgets = {
            'address_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House, Road, Block'}),
            'address_district': forms.Select(attrs={'class': 'form-select', 'id': 'id_district'}),
            'address_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1205'}),
        }
