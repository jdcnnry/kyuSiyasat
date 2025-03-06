from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.shortcuts import render
from bus_management.models import Route, BusLog
from .forms import BusLogForm

def driver_dashboard(request):
    return render(request, 'driver_dashboard/driver_dashboard.html')
