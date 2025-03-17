from django.urls import path
from .views import commuter_dashboard

urlpatterns = [
    path('dashboard/', commuter_dashboard, name='commuter_dashboard'),
]
