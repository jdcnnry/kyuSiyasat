from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib import messages
from bus_management.models import Bus
from .forms import BusLogForm, BusStatusForm
from django.contrib.auth.decorators import login_required

@login_required
def driver_dashboard(request):
    return render(request, 'driver_dashboard.html', {'user': request.user})

@login_required
def create_bus_log(request):
    if request.method == 'POST':
        form = BusLogForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('driver_dashboard')
    else:
        form = BusLogForm(user=request.user)

    return render(request, 'create_bus_log.html', {'form': form})

@login_required
def update_bus_status(request):
    bus = Bus.objects.filter(bus_plate=request.user.profile.bus.bus_plate).first()

    if request.method == 'POST':
        form = BusStatusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus status updated successfully.")
            return redirect('update_bus_status') 

    # Fetch the latest bus status
    bus.refresh_from_db()
    form = BusStatusForm(instance=bus)

    return render(request, 'update_bus_status.html', {'form': form})