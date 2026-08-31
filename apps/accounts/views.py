from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserAddressForm
from apps.orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.save()
            login(request, user)
            messages.success(request, f'Welcome to Orient Computers, {user.first_name}! Your account is ready.')
            return redirect('accounts:dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    next_url = request.GET.get('next', 'accounts:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url if next_url else 'accounts:dashboard')
        else:
            messages.error(request, 'Invalid username/email or password. Please try again.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully signed out.')
    return redirect('core:home')


@login_required
def dashboard_view(request):
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_orders_count = Order.objects.filter(user=request.user).count()

    context = {
        'recent_orders': recent_orders,
        'total_orders_count': total_orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        address_form = UserAddressForm(request.POST, instance=request.user)
        if profile_form.is_valid() and address_form.is_valid():
            profile_form.save()
            address_form.save()
            messages.success(request, 'Your profile and default delivery address have been updated.')
            return redirect('accounts:profile')
    else:
        profile_form = UserProfileForm(instance=request.user)
        address_form = UserAddressForm(instance=request.user)

    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'address_form': address_form,
    })


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/password_change.html', {'form': form})
