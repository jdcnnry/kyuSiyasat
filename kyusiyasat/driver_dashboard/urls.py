from django.urls import path
from .views import driver_dashboard, create_bus_log, update_bus_status

urlpatterns = [
    path('dashboard/', driver_dashboard, name='driver_dashboard'),
    path('dashboard/log/', create_bus_log, name='create_bus_log'),
    path('dashboard/update_status/', update_bus_status, name='update_bus_status'),
]