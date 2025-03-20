from django.urls import path
from .views import commuter_dashboard, bus_detail

urlpatterns = [
    path('dashboard/', commuter_dashboard, name='commuter_dashboard'),
    path('bus/<str:bus_id>/', bus_detail, name='bus_detail'),
]