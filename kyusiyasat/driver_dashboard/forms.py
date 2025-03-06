# forms.py
from django import forms
from bus_management.models import BusLog

class BusLogForm(forms.ModelForm):
    class Meta:
        model = BusLog
        fields = [
            'bus', 'route', 'from_station', 'to_station', 'arrival_time', 
            'time_departed', 'traffic_condition', 'passenger_count'
        ]
        widgets = {
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'time_departed': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }