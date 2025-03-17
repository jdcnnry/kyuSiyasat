from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'profile') and request.user.profile.user_type == user_type:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('commuter_dashboard' if user_type == 'driver' else 'driver_dashboard')
        return wrapper
    return decorator
