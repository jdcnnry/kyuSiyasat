from django.test import TestCase
from django.utils.timezone import now
from bus_management.models import Bus, BusLog, Route, Station
import uuid


class BusModelTest(TestCase):
    def setUp(self):
        self.bus = Bus.objects.create(
            bus_id="B0001",
            bus_plate="ABC-123",
            status="Operating",
            capacity=49
        )

    def test_bus_creation(self):
        # Test if the bus is created correctly
        self.assertEqual(self.bus.bus_id, "B0001")
        self.assertEqual(self.bus.bus_plate, "ABC-123")
        self.assertEqual(self.bus.status, "Operating")
        self.assertEqual(self.bus.capacity, 49)

    def test_bus_str(self):
        # Test the string representation of Bus
        self.assertEqual(str(self.bus), "ABC-123 - Operating")

class StationModelTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(
            station_id="S0001",
            station_name="Quezon City Hall Gate 3 Kalayaan Ave."
        )

    def test_station_creation(self):
        # Test if the station is created correctly
        self.assertEqual(self.station.station_id, "S0001")
        self.assertEqual(self.station.station_name, "Quezon City Hall Gate 3 Kalayaan Ave.")

    def test_station_str(self):
        # Test the string representation of Station
        self.assertEqual(str(self.station), "Quezon City Hall Gate 3 Kalayaan Ave.")

class RouteModelTest(TestCase):
    def setUp(self):
        self.start_station = Station.objects.create(station_id="S0001", station_name="Quezon City Hall Gate 3 Kalayaan Ave.")
        self.end_station = Station.objects.create(station_id="S0002", station_name="Kalayaan Avenue cor. Masigla St.")

        self.route = Route.objects.create(
            route_id="R0001",
            route_name="Route 1a",
            start_station=self.start_station,
            end_station=self.end_station
        )

    def test_route_creation(self):
        # Test if the route is created correctly
        self.assertEqual(self.route.route_id, "R0001")
        self.assertEqual(self.route.route_name, "Route 1a")
        self.assertEqual(self.route.start_station.station_name, "Quezon City Hall Gate 3 Kalayaan Ave.")
        self.assertEqual(self.route.end_station.station_name, "Kalayaan Avenue cor. Masigla St.")

    def test_route_str(self):
        # Test the string representation of Route
        self.assertEqual(str(self.route), "Route 1a")

class BusLogModelTest(TestCase):
    def setUp(self):
        self.bus = Bus.objects.create(bus_id="B0002", bus_plate="XYZ-789", status="Not Operating", capacity=50)
        self.start_station = Station.objects.create(station_id="S0001", station_name="Quezon City Hall Gate 3 Kalayaan Ave.")
        self.end_station = Station.objects.create(station_id="S0002", station_name="Kalayaan Avenue cor. Masigla St.")
        self.route = Route.objects.create(route_id="R0001", route_name="Route 1a", start_station=self.start_station, end_station=self.end_station)

        self.bus_log = BusLog.objects.create(
            log_id=str(uuid.uuid4())[:5],
            bus=self.bus,
            route=self.route,
            from_station=self.start_station,
            to_station=self.end_station,
            arrival_time=now(),
            time_departed=now(),
            traffic_condition="Light",
            passenger_count=30
        )

    def test_bus_log_creation(self):
        # Test if the bus log is created correctly
        self.assertEqual(self.bus_log.bus.bus_plate, "XYZ-789")
        self.assertEqual(self.bus_log.route.route_name, "Route 1a")
        self.assertEqual(self.bus_log.from_station.station_name, "Quezon City Hall Gate 3 Kalayaan Ave.")
        self.assertEqual(self.bus_log.to_station.station_name, "Kalayaan Avenue cor. Masigla St.")
        self.assertEqual(self.bus_log.traffic_condition, "Light")
        self.assertEqual(self.bus_log.passenger_count, 30)
