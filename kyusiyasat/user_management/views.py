from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import BusSelectionForm, UserRegistrationForm, ProfileUpdateForm
from .decorators import user_type_required
from django.contrib import messages


def register(request):
    """Handles user registration."""
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
    """Renders the user's profile page."""
    return render(request, 'my_profile.html', {'user': request.user})

@login_required
def user_redirect_view(request):
    """Redirects users to the appropriate dashboard after login."""
    if request.user.is_authenticated:
        if request.user.profile.user_type == 'driver':
            if not request.user.profile.bus:
                return redirect('user_management:select_bus')
            return redirect('driver_dashboard')  
        return redirect('commuter_dashboard')
    
    return redirect('login')

@login_required
@user_type_required('driver')
def select_bus(request):
    """Allows drivers to select their assigned bus."""
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

@login_required
def update_profile(request):
    """Allows users to update their profile information, including profile picture."""
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
        else:
            messages.error(request, "Error updating profile. Please check the form.")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})
