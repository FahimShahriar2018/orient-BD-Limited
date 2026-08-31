from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in to access the Executive Back-Office.')
            return redirect(f'/account/login/?next={request.path}')
        if not (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser):
            messages.error(request, '403 Forbidden: You do not possess store administrative privileges.')
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
