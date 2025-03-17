from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class HomePageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.user_type == 'driver':
                return redirect('driver_dashboard')  # Redirect to driver dashboard
            else:
                return redirect('commuter_dashboard')  # Redirect to commuter dashboard
        
        return redirect('accounts/login')  # Redirect to login if not authenticated