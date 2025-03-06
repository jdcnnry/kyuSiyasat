from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from bus_management.models import Bus
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Your Email Address")
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, widget=forms.Select, label="Are you a Driver or a Commuter?")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            user_profile = Profile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
            user_profile.save()
        return user
    
class BusSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        assigned_buses = Profile.objects.exclude(bus__isnull=True).values_list('bus', flat=True)
        available_buses = Bus.objects.filter(status='Operating').exclude(bus_id__in=assigned_buses)

        self.fields['bus'] = forms.ModelChoiceField(
                queryset=available_buses,
                label="Select Your Bus"
            )