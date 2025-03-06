from django.urls import path
from .views import driver_dashboard, create_bus_log

urlpatterns = [
    path('dashboard/', driver_dashboard, name='driver_dashboard'),
    path('dashboard/log/', create_bus_log, name='create_bus_log'),
]
