from django import forms
from django.utils.timezone import now
from bus_management.models import BusLog, StationAssignment, BusRoute, Bus
import uuid


class BusLogForm(forms.ModelForm):
    passenger_count = forms.IntegerField(min_value=0)  # Ensure non-negative passenger count

    class Meta:
        model = BusLog
        fields = ['bus', 'route', 'from_station', 'to_station', 'traffic_condition', 'passenger_count']

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get("bus")
        route = cleaned_data.get("route")
        from_station = cleaned_data.get("from_station")
        to_station = cleaned_data.get("to_station")

        if bus and route:
            # Check if the selected bus is assigned to the selected route
            if not BusRoute.objects.filter(bus=bus, route=route).exists():
                raise forms.ValidationError("The selected bus is not assigned to the selected route.")

        if route and from_station and to_station:
            # Get station assignments for the given route
            station_assignments = StationAssignment.objects.filter(route=route).order_by("station_order")

            # Extract station IDs and their orders in the route
            station_order_map = {sa.station.station_id: sa.station_order for sa in station_assignments}

            if from_station.station_id not in station_order_map or to_station.station_id not in station_order_map:
                raise forms.ValidationError("Both stations must be part of the selected route.")

            # Check adjacency
            from_order = station_order_map[from_station.station_id]
            to_order = station_order_map[to_station.station_id]

            if abs(from_order - to_order) != 1:
                raise forms.ValidationError("The selected stations must be adjacent.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.arrival_time = now()
        instance.time_departed = now()
        instance.log_id = str(uuid.uuid4())[:5]  # Generate a short unique ID

        if commit:
            instance.save()
        return instance
    
class BusStatusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Bus.STATUS_CHOICES, attrs={'class': 'form-control'})
        }
