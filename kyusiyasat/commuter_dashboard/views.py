from django.shortcuts import render, get_object_or_404
from bus_management.models import Bus, BusRoute, Route, BusLog, Station
from user_management.models import Profile
from bus_management.utils import calculate_eta
from django.contrib.auth.decorators import login_required
from user_management.decorators import user_type_required


@login_required
@user_type_required('commuter')
def commuter_dashboard(request):
    buses = Bus.objects.all().select_related('busroute__route')

    # Get filter values from request
    status_filter = request.GET.get('status', '')
    route_filter = request.GET.get('route', '')

    # Apply filters if selected
    if status_filter:
        buses = buses.filter(status=status_filter)
    if route_filter:
        buses = buses.filter(busroute__route__route_id=route_filter)

    routes = Route.objects.all()  # Get all routes for the filter dropdown

    # Fetch drivers and next station for each bus
    for bus in buses:
        driver_profile = Profile.objects.filter(user_type='driver', bus=bus).select_related('user').first()
        bus.driver_name = driver_profile.user.get_full_name() if driver_profile else "TBA"

        latest_log = BusLog.objects.filter(bus=bus).select_related('to_station').order_by('-arrival_time').first()
        bus.next_station = latest_log.to_station.station_name if latest_log and latest_log.to_station else "No assigned destination"

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

        bus.eta = eta

    return render(request, 'commuter_dashboard.html', {
        'buses': buses,
        'routes': routes,
        'status_filter': status_filter,
        'route_filter': route_filter,
    })


@login_required
@user_type_required('commuter')
def bus_detail(request, bus_id):
    bus = get_object_or_404(Bus.objects.select_related('busroute__route'), pk=bus_id)

    # Get driver if assigned
    driver = Profile.objects.filter(user_type='driver', bus=bus).select_related('user').first()
    driver_name = driver.user.get_full_name() if driver else "TBA"

    latest_log = BusLog.objects.filter(bus=bus).select_related('from_station').order_by('-arrival_time').first()

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
        'driver': driver_name,
        'route': bus.busroute.route.route_name if hasattr(bus, 'busroute') and bus.busroute.route else "No Assigned Route",
        'plate_number': bus.bus_plate,
        'eta': eta,
        'time_departed': latest_log.time_departed if latest_log else "TBA",
        'previous_station': latest_log.from_station.station_name if latest_log else "TBA",
        'next_station': latest_log.to_station.station_name if latest_log else "TBA",
        'passengers': latest_log.passenger_count if latest_log else "TBA",
        'traffic_condition': latest_log.traffic_condition if latest_log else "TBA",
        'availability': "Available" if bus.status == "Operating" else "Not Available"
    }

    return render(request, 'bus_detail.html', bus_details)