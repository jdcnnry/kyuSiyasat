from django.test import TestCase
from django.urls import reverse
from user_management.models import Profile, User

class GettingStartedTest(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        
        # Create a commuter user
        self.commuter_user = User.objects.create_user(username='commuter', password='testpassword')
        Profile.objects.create(user=self.commuter_user, user_type='commuter')

        # Create a driver user
        self.driver_user = User.objects.create_user(username='driver', password='testpassword')
        Profile.objects.create(user=self.driver_user, user_type='driver')

    def test_getting_started_driver_requires_login(self):
        # Test that unauthenticated users are redirected from getting_started_driver.
        response = self.client.get(reverse('pages:getting_started_driver'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_getting_started_driver_authenticated(self):
        # Test that authenticated drivers can access getting_started_driver.
        self.client.login(username='driver', password='testpassword')
        response = self.client.get(reverse('pages:getting_started_driver'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'getting_started_driver.html')

    def test_getting_started_commuter_requires_login(self):
        # Test that unauthenticated users are redirected from getting_started_commuter.
        response = self.client.get(reverse('pages:getting_started_commuter'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_getting_started_commuter_authenticated(self):
        # Test that authenticated commuters can access getting_started_commuter.
        self.client.login(username='commuter', password='testpassword')
        response = self.client.get(reverse('pages:getting_started_commuter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'getting_started_commuter.html')


class RoutesTest(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.commuter_user = User.objects.create_user(username='commuter', password='testpassword')
        Profile.objects.create(user=self.commuter_user, user_type='commuter')

        self.driver_user = User.objects.create_user(username='driver', password='testpassword')
        Profile.objects.create(user=self.driver_user, user_type='driver')

    def test_routes_page_requires_login(self):
        # Test that unauthenticated users are redirected from routes_page.
        response = self.client.get(reverse('pages:routes'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_routes_page_authenticated(self):
        # Test that authenticated users can access routes_page.
        self.client.login(username='commuter', password='testpassword')
        response = self.client.get(reverse('pages:routes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes.html')
