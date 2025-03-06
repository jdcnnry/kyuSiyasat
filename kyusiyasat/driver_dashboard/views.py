from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.shortcuts import render
from bus_management.models import Route, BusLog
from .forms import BusLogForm
from django.contrib.auth.decorators import login_required

@login_required
def driver_dashboard(request):
    return render(request, 'driver_dashboard/driver_dashboard.html', {'user': request.user})

@login_required
def create_bus_log(request):
    if request.method == 'POST':
        form = BusLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_dashboard')  # Redirect to dashboard after saving
    else:
        form = BusLogForm()

    return render(request, 'driver_dashboard/create_bus_log.html', {'form': form})
