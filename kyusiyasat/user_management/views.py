from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import BusSelectionForm, UserRegistrationForm, ProfileUpdateForm, CustomPasswordChangeForm
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
                return redirect('pages:getting_started_commuter')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def my_profile(request):
    """Renders the user's profile page."""
    return render(request, 'my_profile.html', {'user': request.user})

def user_redirect_view(request):
    """Redirects users to the appropriate page after login."""
    if request.user.is_authenticated:
        if not request.user.profile.has_seen_getting_started:
            # Redirect to the appropriate "getting started" page
            if request.user.profile.user_type == 'driver':
                return redirect('pages:getting_started_driver')
            else:
                return redirect('pages:getting_started_commuter')
        
        # Redirect based on user type after they have seen the getting started page
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
            return redirect('pages:getting_started_driver')
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
            return redirect('user_management:my_profile')
          
        else:
            messages.error(request, "Error updating profile. Please check the form.")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]

            # Authenticate the user with the current password
            user = authenticate(username=request.user.username, password=current_password)

            if user is not None:
                # Set the new password and keep the user logged in
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

                messages.success(request, "Your password has been successfully changed.")
                return redirect('user_management:my_profile')
            else:
                messages.error(request, "The current password is incorrect.")
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'registration/change_password.html', {'form': form})