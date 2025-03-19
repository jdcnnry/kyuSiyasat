from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from user_management.models import Profile

class HomePageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_profile = request.user.profile
            except Profile.DoesNotExist:
                return redirect('login')
            
            if user_profile.user_type == 'driver':
                return redirect('driver_dashboard')
            else:
                return redirect('commuter_dashboard')

        return redirect('login')
