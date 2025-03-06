from django.urls import path
from .views import register, my_profile

app_name = 'user_management'

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', my_profile, name='my_profile'),
]