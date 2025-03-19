from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Profile, User
from bus_management.models import Bus, Route, BusRoute, BusLog, Station, StationAssignment
from django.utils import timezone


class CommuterDashboardTests(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.client = Client()
        
        # Create a Driver User and associate it with a Profile
        self.driver_user = User.objects.create_user(username='testdriver', password='testpass')
        self.driver_profile = Profile.objects.create(user=self.driver_user, user_type='driver')

        # Create a Commuter User
        self.commuter_user = User.objects.create_user(username='testcommuter', password='testpass')
        self.commuter_profile = Profile.objects.create(user=self.commuter_user, user_type='commuter')
            
        # Create a Bus
        self.bus = Bus.objects.create(bus_id='B001', bus_plate='XYZ-789', status='Operating', capacity=50)

        # Assign the bus to the driver
        self.driver_profile.bus = self.bus
        self.driver_profile.save()
        
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
        self.client.login(username='testcommuter', password='testpass')
    
    def test_commuter_dashboard_view(self):
        # Tests that the commuter dashboard page loads correctly and uses the correct template.
        response = self.client.get(reverse('commuter_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commuter_dashboard.html')

    def test_create_bus_log_and_view_as_commuter(self):
        # Test that a commuter can view the bus details.
        self.client.login(username='testdriver', password='testpass')
        
        # Create a bus log
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
        self.assertEqual(response.status_code, 302)  # Expect redirect after creation
        
        self.client.logout()
        self.client.login(username='testcommuter', password='testpass')
        
        response = self.client.get(reverse('bus_detail', kwargs={'bus_id': self.bus.bus_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bus.bus_plate)
        self.assertContains(response, "Available")