from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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
        self.assertEqual(str(self.profile_driver), 'driver_user - Driver')
        self.assertEqual(str(self.profile_commuter), 'commuter_user - Commuter')

    def test_user_profile_relation(self):
        # Test that the one-to-one relationship is working correctly.
        self.assertEqual(self.user_driver.profile, self.profile_driver)
        self.assertEqual(self.user_commuter.profile, self.profile_commuter)

    def test_user_type_choices(self):
        # Test that user_type choices are valid.
        valid_choices = dict(Profile.USER_TYPE_CHOICES)
        self.assertIn(self.profile_driver.user_type, valid_choices)
        self.assertIn(self.profile_commuter.user_type, valid_choices)


class UpdateProfileTest(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword', first_name='OldFirst', last_name='OldLast', email='old@gmail.com')
        self.profile = Profile.objects.create(user=self.user, user_type='commuter')
        self.client.login(username='testuser', password='testpassword')

    def test_update_profile(self):
        # Test that the profile is updated correctly.
        url = reverse('user_management:update_profile')
        data = {
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
            'email': 'new@gmail.com',
        }
        response = self.client.post(url, data, follow=True)
        
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        
        self.assertEqual(self.user.first_name, 'NewFirst')
        self.assertEqual(self.user.last_name, 'NewLast')
        self.assertEqual(self.user.email, 'new@gmail.com')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_profile.html')


class UserRegistrationTest(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.user_driver = User.objects.create_user(
            username="driver_user",
            password="Testpassword123!"
        )

    def test_deactivated_user_cannot_login(self):
        # Test that a deactivated user cannot log in.
        self.user_driver.is_active = False
        self.user_driver.save()

        response = self.client.post(reverse('login'), {
            'username': 'driver_user',
            'password': 'Testpassword123!'
        })
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_invalid_login(self):
        # Test that an invalid login attempt does not redirect
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")  # Check for error message


    def test_duplicate_user_registration(self):
        # Test that the registration form is invalid with a duplicate username.
        form_data = {
            'username': 'driver_user',  # Duplicate username
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser2@gmail.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'driver',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)  # Username should trigger an error

    def test_unauthorized_access_redirect(self):
        # Test that unauthorized users are redirected to the login page.
        response = self.client.get(reverse('user_management:my_profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_registration_form_valid(self):
        # Test that the registration form is valid with correct data.
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@gmail.com',
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
            'email': 'testuser@gmail.com',
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
            'email': 'testuser@gmail.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'driver',
        })
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser', user_type='driver').exists())

    def test_register_driver_redirects_to_getting_started(self):
        # Test that registering as a driver redirects to the driver dashboard.
        response = self.client.post(reverse('user_management:register'), {
            'username': 'driveruser',
            'first_name': 'Driver',
            'last_name': 'User',
            'email': 'driver@gmail.com',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!',
            'user_type': 'driver',
        })
        self.assertRedirects(response, reverse('user_management:select_bus'))  

        driver_user = User.objects.get(username='driveruser')
        bus = Bus.objects.create(bus_id='B002', bus_plate='XYZ-456', status='Operating', capacity=50)
        Profile.objects.filter(user=driver_user).update(bus=bus)

        self.assertTrue(User.objects.filter(username='driveruser').exists())
        self.client.login(username='driveruser', password='Testpassword123!')
        response = self.client.get(reverse('pages:getting_started_driver'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'getting_started_driver.html')

    def test_register_commuter_redirects_to_getting_started(self):
        # Test that registering as a commuter redirects to the commuter dashboard.
        response = self.client.post(reverse('user_management:register'), {
            'username': 'commuteruser',
            'first_name': 'Commuter',
            'last_name': 'User',
            'email': 'commuter@gmail.com',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!',
            'user_type': 'commuter',
        })
        self.assertRedirects(response, reverse('pages:getting_started_commuter'))  

        self.assertTrue(User.objects.filter(username='commuteruser').exists())
        self.client.login(username='commuteruser', password='Testpassword123!')
        response = self.client.get(reverse('pages:getting_started_commuter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'getting_started_commuter.html')
    
    def test_commuter_cannot_select_bus(self):
        # Test that a commuter cannot access the select_bus view.
        User = get_user_model()

        commuter = User.objects.create_user(
            username='commuter_user',
            password='testpassword'
        )

        Profile.objects.create(user=commuter, user_type='commuter')
        self.client.login(username='commuter_user', password='testpassword')

        response = self.client.get(reverse('user_management:select_bus'))
        self.assertRedirects(response, reverse('commuter_dashboard'))
