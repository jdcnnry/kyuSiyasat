from django.urls import path
from .views import register, my_profile, user_redirect_view

app_name = 'user_management'

urlpatterns = [
    path('home/', user_redirect_view, name='home'),
    path('register/', register, name='register'),
    path('profile/', my_profile, name='my_profile'),
]