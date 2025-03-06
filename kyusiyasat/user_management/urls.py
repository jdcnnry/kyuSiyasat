from django.urls import path
from .views import register

app_name = 'user_management'

urlpatterns = [
    path('register/', register, name='register'),
]