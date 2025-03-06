from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from bus_management.models import Bus, BusLog, Route, Station, BusRoute, StationAssignment

class DriverDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testdriver', password='testpass')

        self.station_one = Station.objects.create(station_id="S001", station_name="Start Station")
        self.station_two = Station.objects.create(station_id="S002", station_name="Second Station")
        self.station_three = Station.objects.create(station_id="S003", station_name="Third Station")
        self.station_four = Station.objects.create(station_id="S004", station_name="Final Station")

        self.bus = Bus.objects.create(bus_id='B001', bus_plate='ABC-123', status='Operating', capacity=50)

        self.route = Route.objects.create(
            route_id="R001",
            route_name="Test Route",
            start_station_id= self.station_one.station_id,
            end_station_id= self.station_four.station_id
        )
        BusRoute.objects.create(bus=self.bus, route=self.route)

        StationAssignment.objects.create(station_assignment_id="SA001", route=self.route, station=self.station_one, station_order=1, distance_to_next=2.5)
        StationAssignment.objects.create(station_assignment_id="SA002", route=self.route, station=self.station_two, station_order=2, distance_to_next=3.0)
        StationAssignment.objects.create(station_assignment_id="SA003", route=self.route, station=self.station_three, station_order=3, distance_to_next=4.0)
        StationAssignment.objects.create(station_assignment_id="SA004", route=self.route, station=self.station_four, station_order=4, distance_to_next=None)

        self.client.login(username='testdriver', password='testpass')

    def test_driver_dashboard_view(self):
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'driver_dashboard/driver_dashboard.html')

    def test_create_bus_log_view_get(self):
        response = self.client.get(reverse('create_bus_log'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'driver_dashboard/create_bus_log.html')

    def test_create_bus_log_view_post(self):
        response = self.client.post(reverse('create_bus_log'), {
            'bus': self.bus.bus_id,
            'route': self.route.route_id,  # Adjust based on available routes
            'from_station': self.station_two.station_id,
            'to_station': self.station_three.station_id,
            'arrival_time': '2025-03-06 10:00:00',
            'time_departed': '2025-03-06 09:30:00',
            'traffic_condition': 'Light',
            'passenger_count': 10,
        })

        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertEqual(BusLog.objects.count(), 1)

    # def test_update_bus_status_view_get(self):
    #     response = self.client.get(reverse('update_bus_status'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'driver_dashboard/update_bus_status.html')

    # def test_update_bus_status_view_post(self):
    #     response = self.client.post(reverse('update_bus_status'), {
    #         'status': 'Not Operating',
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.bus.refresh_from_db()
    #     self.assertEqual(self.bus.status, 'Not Operating')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
