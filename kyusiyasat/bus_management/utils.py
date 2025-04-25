from django.utils.timezone import now
from .models import StationAssignment

def calculate_eta(current_station, traffic_condition, time_departed, route, base_speed_kph=50):
    try:
        current_sa = StationAssignment.objects.get(route=route, station=current_station)
    except StationAssignment.DoesNotExist:
        return None

    distance_to_next = current_sa.distance_to_next
    if distance_to_next is None:
        return None

    traffic_multiplier = {
        'Light': 1.0,
        'Moderate': 3.0,
        'Heavy': 5.0,
    }

    multiplier = traffic_multiplier.get(traffic_condition, 1.0)

    time_for_segment = (distance_to_next / base_speed_kph) * 60 * multiplier

    time_elapsed = (now() - time_departed).total_seconds() / 60

    eta_remaining = round(time_for_segment - time_elapsed)

    return max(eta_remaining, 0)