# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid
from django.db import models
from django.utils.timezone import now


class Bus(models.Model):
    bus_id = models.CharField(primary_key=True, max_length=5)
    bus_plate = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('Operating', 'Operating'),
        ('Not Operating', 'Not Operating'),
    ]
    status = models.CharField(max_length=255)
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bus'

    def __str__(self):
        return f"{self.bus_plate} - {self.status}"


class BusLog(models.Model):
    log_id = models.CharField(primary_key=True, max_length=5, default=uuid.uuid4, editable=False)
    bus = models.ForeignKey('Bus', models.DO_NOTHING)
    route = models.ForeignKey('Route', models.DO_NOTHING)
    from_station = models.ForeignKey('Station', models.DO_NOTHING)
    to_station = models.ForeignKey('Station', models.DO_NOTHING, related_name='buslog_to_station_set')
    arrival_time = models.DateTimeField(default=now, editable=False)
    time_departed = models.DateTimeField(default=now, editable=False)

    TRAFFIC_CONDITIONS = [
        ('Light', 'Light'),
        ('Moderate', 'Moderate'),
        ('Heavy', 'Heavy'),
    ]
    
    traffic_condition = models.CharField(max_length=255, choices=TRAFFIC_CONDITIONS)
    passenger_count = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bus_log'


class BusRoute(models.Model):
    bus = models.OneToOneField(Bus, models.DO_NOTHING, primary_key=True)
    route = models.ForeignKey('Route', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bus_route'


class Route(models.Model):
    route_id = models.CharField(primary_key=True, max_length=5)
    route_name = models.CharField(max_length=255)
    start_station = models.ForeignKey('Station', models.DO_NOTHING)
    end_station = models.ForeignKey('Station', models.DO_NOTHING, related_name='route_end_station_set')

    class Meta:
        managed = False
        db_table = 'route'

    def __str__(self):
        return f"{self.route_name}"


class Station(models.Model):
    station_id = models.CharField(primary_key=True, max_length=5)
    station_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'station'

    def __str__(self):
        return f"{self.station_name}"


class StationAssignment(models.Model):
    route = models.OneToOneField(Route, models.DO_NOTHING, primary_key=True)  # The composite primary key (route_id, station_id) found, that is not supported. The first column is selected.
    station = models.ForeignKey(Station, models.DO_NOTHING)
    station_order = models.IntegerField()
    distance_to_next = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station_assignment'
        unique_together = (('route', 'station'),)
