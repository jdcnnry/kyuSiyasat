from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib import messages
from bus_management.models import Bus, BusLog
from .forms import BusLogForm, BusStatusForm
from django.contrib.auth.decorators import login_required
from user_management.decorators import user_type_required
from bus_management.utils import calculate_eta
from user_management.models import Profile


@login_required
@user_type_required('driver')
def driver_dashboard(request):
    driver_profile = Profile.objects.get(user=request.user)
    
    bus = Bus.objects.filter(bus_id=driver_profile.bus.bus_id).first()
    
    latest_log = BusLog.objects.filter(bus=bus).order_by('-arrival_time').first()

    bus_details = {}

    eta = "TBA"

    if latest_log and latest_log.to_station and bus.busroute:
        eta_minutes = calculate_eta(
            current_station=latest_log.from_station,
            route=bus.busroute.route,
            traffic_condition=latest_log.traffic_condition,
            time_departed=latest_log.time_departed
        )

        if eta_minutes is None:
            eta = "TBA"
        elif eta_minutes == 0:
            eta = "Bus is currently at the station."
        elif eta_minutes == 1:
            eta = "1 min"
        else:
            eta = f"{eta_minutes} mins"

    bus_details['eta'] = eta

    bus_details = {
        'bus': bus,
        'plate_number': bus.bus_plate,
        'route': bus.busroute.route.route_name if bus.busroute else "No Assigned Route",
        'time_departed': latest_log.time_departed if latest_log else "TBA",
        'previous_station': latest_log.from_station.station_name if latest_log else "TBA",
        'next_station': latest_log.to_station.station_name if latest_log else "TBA",
        'passengers': latest_log.passenger_count if latest_log else "TBA",
        'traffic_condition': latest_log.traffic_condition if latest_log else "TBA",
        'eta': eta,
        'availability': "Available" if bus.status == "Operating" else "Not Available",
    }
    
    return render(request, 'driver_dashboard.html', {
        'user': request.user,
        'bus': bus,
        'bus_details': bus_details,
        'current_status': bus.status,
    })

@login_required
@user_type_required('driver')
def create_bus_log(request):

    bus = request.user.profile.bus

    if bus.status != "Operating":
        messages.error(request, "Bus is not in operation.")
        return redirect('driver_dashboard')

    if request.method == 'POST':
        form = BusLogForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus log created successfully.")
            return redirect('driver_dashboard')
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
            return redirect('driver_dashboard') 

    bus.refresh_from_db()
    form = BusStatusForm(instance=bus)

    return render(request, 'update_bus_status.html', {'form': form})