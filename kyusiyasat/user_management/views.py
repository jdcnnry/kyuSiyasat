from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import BusSelectionForm, UserRegistrationForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.profile.user_type == 'driver':
                return redirect('user_management:select_bus')  
            else:
                
                return redirect('commuter_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def my_profile(request):
    return render(request, 'my_profile.html', {'user': request.user})

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def user_redirect_view(request):
    """Redirect users to the appropriate dashboard after login."""
    if request.user.is_authenticated:
        if request.user.profile.user_type == 'driver':
            if not request.user.profile.bus:
                return redirect('user_management:select_bus')
            else:
                return redirect('driver_dashboard')  
        else:
            return redirect('commuter_dashboard')

    return redirect('login')

@login_required
def select_bus(request):
    if not request.user.profile.user_type == 'driver':
        return redirect('commuter_dashboard')

    if request.method == 'POST':
        form = BusSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            bus = form.cleaned_data['bus']
            profile = request.user.profile
            profile.bus = bus
            profile.save()
            return redirect('driver_dashboard') 
    else:
        form = BusSelectionForm(user=request.user)

    return render(request, 'registration/select_bus.html', {'form': form})

def update_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_management:my_profile') 
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})