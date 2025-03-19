from django.urls import path
from .views import register, my_profile, user_redirect_view, select_bus, update_profile

app_name = 'user_management'

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', my_profile, name='my_profile'),
    path('select_bus/', select_bus, name='select_bus'),
    path('redirect/', user_redirect_view, name='user_redirect_view'),
    path('profile/edit/', update_profile, name='update_profile'),
]