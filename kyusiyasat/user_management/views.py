from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.profile.user_type == 'driver':
                return redirect('driver_dashboard')  # Replace with your driver dashboard URL
            else:
                return redirect('commuter_dashboard')  # Replace with your commuter dashboard URL
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def my_profile(request):
    return render(request, 'registration/my_profile.html', {'user': request.user})

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def user_redirect_view(request):
    """Redirect users to the appropriate dashboard after login."""
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_driver') and request.user.is_driver:
            return redirect('driver_dashboard')  # Redirect driver users
        else:
            return redirect('user_dashboard')  # Redirect regular users

    return redirect('login')  # Default case