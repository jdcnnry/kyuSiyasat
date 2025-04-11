from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib import messages
from bus_management.models import Bus, BusLog
from .forms import BusLogForm, BusStatusForm
from django.contrib.auth.decorators import login_required
from user_management.decorators import user_type_required
from user_management.models import Profile


@login_required
@user_type_required('driver')
def driver_dashboard(request):
    driver_profile = Profile.objects.get(user=request.user)
    
    bus = Bus.objects.filter(bus_id=driver_profile.bus.bus_id).first()  # Adjust to use bus ID
    
    latest_log = BusLog.objects.filter(bus=bus).order_by('-arrival_time').first()
    
    bus_details = {
        'bus': bus,
        'plate_number': bus.bus_plate,
        'route': bus.busroute.route.route_name if bus.busroute else "No Assigned Route",
        'time_departed': latest_log.time_departed if latest_log else "TBA",
        'previous_station': latest_log.from_station.station_name if latest_log else "TBA",
        'next_station': latest_log.to_station.station_name if latest_log else "TBA",
        'passengers': latest_log.passenger_count if latest_log else "TBA",
        'traffic_condition': latest_log.traffic_condition if latest_log else "TBA",
        'availability': "Available" if bus.status == "Operating" else "Not Available",
    }
    
    return render(request, 'driver_dashboard.html', {
        'user': request.user,
        'bus': bus,
        'bus_details': bus_details,
        'current_status': bus.status,
    })

@login_required
def create_bus_log(request):
    if request.method == 'POST':
        form = BusLogForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus log created successfully.")
            return redirect('create_bus_log')
        else:
            messages.error(request, "Please enter both adjacent stations.")
    else:
        form = BusLogForm(user=request.user)

    return render(request, 'create_bus_log.html', {'form': form})

@login_required
@user_type_required('driver')
def update_bus_status(request):
    bus = Bus.objects.filter(bus_plate=request.user.profile.bus.bus_plate).first()

    if request.method == 'POST':
        form = BusStatusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus status updated successfully.")
            return redirect('update_bus_status') 

    bus.refresh_from_db()
    form = BusStatusForm(instance=bus)

    return render(request, 'update_bus_status.html', {'form': form})