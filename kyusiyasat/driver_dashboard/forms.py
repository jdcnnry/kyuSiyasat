from django import forms
from django.utils.timezone import now
from bus_management.models import BusLog, Station, StationAssignment, BusRoute, Bus
import uuid


class BusLogForm(forms.ModelForm):
    passenger_count = forms.IntegerField(min_value=0)  # Ensure non-negative passenger count

    class Meta:
        model = BusLog
        fields = ['bus', 'route', 'from_station', 'to_station', 'traffic_condition', 'passenger_count']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user argument
        super().__init__(*args, **kwargs)

        # Filter the bus field to show only the bus assigned to the logged-in driver
        if self.user and hasattr(self.user, 'profile'):
            profile = self.user.profile
            bus_route = BusRoute.objects.get(bus=profile.bus)
            stations = StationAssignment.objects.filter(route=bus_route.route).values_list('station', flat=True)
            if profile.user_type == 'driver' and profile.bus:
                self.fields['bus'].initial = profile.bus
                self.fields['bus'].disabled = True
                self.fields['route'].initial = bus_route.route
                self.fields['route'].disabled = True
                self.fields['from_station'].queryset = Station.objects.filter(station_id__in=stations)
                self.fields['to_station'].queryset = Station.objects.filter(station_id__in=stations)
            else:
                self.fields['bus'].queryset = Bus.objects.none()  # Show no buses if the user is not a driver or has no bus assigned
        else:
            self.fields['bus'].queryset = Bus.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get("bus")
        route = cleaned_data.get("route")
        from_station = cleaned_data.get("from_station")
        to_station = cleaned_data.get("to_station")
        passenger_count = cleaned_data.get("passenger_count")

        # Initialize a list to store error messages
        errors = []

        if bus and route:
            # Check if the selected bus is assigned to the selected route
            if not BusRoute.objects.filter(bus=bus, route=route).exists():
                errors.append("The selected bus is not assigned to the selected route.")

        if route and from_station and to_station:
            # Get station assignments for the given route
            station_assignments = StationAssignment.objects.filter(route=route).order_by("station_order")

            # Extract station IDs and their orders in the route
            station_order_map = {sa.station.station_id: sa.station_order for sa in station_assignments}

            if from_station.station_id not in station_order_map or to_station.station_id not in station_order_map:
                errors.append("Both stations must be part of the selected route.")

            # Check adjacency
            from_order = station_order_map[from_station.station_id]
            to_order = station_order_map[to_station.station_id]

            if from_order - to_order != -1:
                errors.append("The selected stations must be adjacent.")
        
        if bus and passenger_count is not None:
            # Check if the passenger count exceeds the bus capacity
            bus_capacity = bus.capacity
            if passenger_count > bus_capacity:
                errors.append(f"Passenger count cannot exceed the bus capacity of {bus_capacity}.")

        # If any errors were collected, add them to the form
        if errors:
            for error in errors:
                self.add_error(None, error)  # Add errors to non-field errors, or use a specific field name if needed

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
        fields = ['status']  # Ensure bus_id and status are included
        widgets = {
            'status': forms.Select(choices=Bus.STATUS_CHOICES, attrs={'class': 'form-control'})
        }
    