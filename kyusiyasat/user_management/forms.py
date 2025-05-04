from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bus_management.models import Bus
from .models import Profile
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, widget=forms.Select, label="Role")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirm Password"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[-1]
        
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'mail.com', 'hotmail.com']
        if domain not in allowed_domains:
            raise ValidationError("Please use an email address with one of the following domains: @%s" % ', @'.join(allowed_domains))
        return email

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
        available_buses = Bus.objects.exclude(bus_id__in=assigned_buses).order_by('bus_plate')

        self.fields['bus'] = forms.ModelChoiceField(
                queryset=available_buses,
                label="Select Your Bus"
            )
        
class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    user_type = forms.CharField(
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['image','first_name', 'last_name', 'email', 'user_type']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[-1]
        
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'mail.com', 'hotmail.com']
        if domain not in allowed_domains:
            raise ValidationError("Please use an email address with one of the following domains: @%s" % ', @'.join(allowed_domains))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.fields['user_type'].initial = self.instance.get_user_type_display()

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()

        return profile

class CustomPasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if self.user and not self.user.check_password(current_password):
            raise ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "New passwords do not match.")

        return cleaned_data