from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from bus_management.models import Bus, BusLog, Route, Station, BusRoute, StationAssignment
from user_management.models import Profile
from django.utils import timezone


class DriverDashboardTests(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.client = Client()

        # Create a User and associate it with a Driver Profile
        self.user = User.objects.create_user(username='testdriver', password='testpass')

        # Create a Bus
        self.bus = Bus.objects.create(bus_id='B001', bus_plate='ABC-123', status='Operating', capacity=50)

        # Assign the user as a Driver with a Bus
        self.profile = Profile.objects.create(user=self.user, user_type='driver', bus=self.bus)

        # Create Stations
        self.station_one = Station.objects.create(station_id="S001", station_name="Start Station")
        self.station_two = Station.objects.create(station_id="S002", station_name="Second Station")
        self.station_three = Station.objects.create(station_id="S003", station_name="Third Station")
        self.station_four = Station.objects.create(station_id="S004", station_name="Final Station")

        # Create a Route
        self.route = Route.objects.create(
            route_id="R001",
            route_name="Test Route",
            start_station_id=self.station_one.station_id,
            end_station_id=self.station_four.station_id
        )

        # Assign the Bus to the Route
        self.bus_route = BusRoute.objects.create(bus=self.bus, route=self.route)

        # Assign Stations to the Route in Order
        StationAssignment.objects.create(station_assignment_id="SA001", route=self.route, station=self.station_one, station_order=1, distance_to_next=2.5)
        StationAssignment.objects.create(station_assignment_id="SA002", route=self.route, station=self.station_two, station_order=2, distance_to_next=3.0)
        StationAssignment.objects.create(station_assignment_id="SA003", route=self.route, station=self.station_three, station_order=3, distance_to_next=4.0)
        StationAssignment.objects.create(station_assignment_id="SA004", route=self.route, station=self.station_four, station_order=4, distance_to_next=None)

        # Log in the test user
        self.client.login(username='testdriver', password='testpass')

    def test_driver_dashboard_view(self):
        # Tests if the driver dashboard page loads correctly and uses the correct template.
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'driver_dashboard.html')

    def test_create_bus_log_view_get(self):
        # Tests if the "Create Bus Log" page loads successfully and renders the correct template.
        response = self.client.get(reverse('create_bus_log'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_bus_log.html')

    def test_create_bus_log_view_post(self):
        # Tests if submitting a valid bus log form successfully creates a new BusLog entry.
        self.client.login(username='testdriver', password='testpass')

        response = self.client.post(reverse('create_bus_log'), {
            'bus': self.bus.pk,
            'route': self.route.pk,
            'from_station': self.station_two.pk,
            'to_station': self.station_three.pk,
            'arrival_time': timezone.now(),
            'time_departed': timezone.now(),
            'traffic_condition': 'Light',
            'passenger_count': 10,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BusLog.objects.count(), 1)

    def test_update_bus_status_view_get(self):
        # Tests if the "Update Bus Status" page loads successfully and renders the correct template.
        response = self.client.get(reverse('update_bus_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_bus_status.html')

    def test_update_bus_status_view_post(self):
        # Tests if a driver can successfully update a bus's status
        response = self.client.post(reverse('update_bus_status'), {
            'status': 'Not Operating',
        })
        self.assertEqual(response.status_code, 302)
        self.bus.refresh_from_db()
        self.assertEqual(self.bus.status, 'Not Operating')

    def test_redirect_if_not_logged_in(self):
        # Tests if an unauthenticated user is redirected when trying to access the driver dashboard.
        self.client.logout()
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login