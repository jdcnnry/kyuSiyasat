from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.shortcuts import render
from bus_management.models import Route, BusLog, Bus
from .forms import BusLogForm, BusStatusForm
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

@login_required
def update_bus_status(request):
    bus = Bus.objects.filter(bus_plate=request.user.username).first()  # Adjust based on your user-bus relationship

    if not bus:
        return redirect('driver_dashboard')  # Redirect if no bus is found

    if request.method == 'POST':
        form = BusStatusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            return redirect('driver_dashboard')  # Redirect after updating status
    else:
        form = BusStatusForm(instance=bus)

    return render(request, 'driver_dashboard/update_bus_status.html', {'form': form})
