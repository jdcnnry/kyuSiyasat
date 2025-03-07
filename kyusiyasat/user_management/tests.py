from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from bus_management.models import Bus
from .forms import UserRegistrationForm


class ProfileModelTest(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.user_driver = User.objects.create_user(username='driver_user', password='testpassword')
        self.user_commuter = User.objects.create_user(username='commuter_user', password='testpassword')
        self.profile_driver = Profile.objects.create(user=self.user_driver, user_type='driver')
        self.profile_commuter = Profile.objects.create(user=self.user_commuter, user_type='commuter')

    def test_profile_creation(self):
        # Test that profiles are created correctly.
        self.assertEqual(self.profile_driver.user.username, 'driver_user')
        self.assertEqual(self.profile_driver.user_type, 'driver')
        self.assertEqual(self.profile_commuter.user.username, 'commuter_user')
        self.assertEqual(self.profile_commuter.user_type, 'commuter')

    def test_profile_str_representation(self):
        # Test the string representation of the Profile model.
        self.assertEqual(str(self.profile_driver), 'driver_user - driver')
        self.assertEqual(str(self.profile_commuter), 'commuter_user - commuter')

    def test_user_profile_relation(self):
        # Test that the one-to-one relationship is working correctly.
        self.assertEqual(self.user_driver.profile, self.profile_driver)
        self.assertEqual(self.user_commuter.profile, self.profile_commuter)

    def test_user_type_choices(self):
        # Test that user_type choices are valid.
        valid_choices = dict(Profile.USER_TYPE_CHOICES)
        self.assertIn(self.profile_driver.user_type, valid_choices)
        self.assertIn(self.profile_commuter.user_type, valid_choices)


class UserRegistrationTest(TestCase):
    def test_user_registration_form_valid(self):
        # Test that the registration form is valid with correct data.
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'driver',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        # Test that the form is invalid when passwords do not match.
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass123!',
            'user_type': 'driver',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_view(self):
        # Test the user registration view.
        response = self.client.post(reverse('user_management:register'), {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'driver',
        })
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser', user_type='driver').exists())

    def test_register_driver_redirects_to_driver_dashboard(self):
        # Test that registering as a driver redirects to the driver dashboard.
        response = self.client.post(reverse('user_management:register'), {
            'username': 'driveruser',
            'first_name': 'Driver',
            'last_name': 'User',
            'email': 'driver@example.com',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!',
            'user_type': 'driver',
        })
        self.assertRedirects(response, reverse('user_management:select_bus'))  

        driver_user = User.objects.get(username='driveruser')
        bus = Bus.objects.create(bus_id='B002', bus_plate='XYZ-456', status='Operating', capacity=50)
        Profile.objects.filter(user=driver_user).update(bus=bus)

        self.client.login(username='driveruser', password='Testpassword123!')
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'driver_dashboard.html')
