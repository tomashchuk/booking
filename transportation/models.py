from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models as gis_models
from compositekey import db
from django.db.models import CheckConstraint, UniqueConstraint, Q, F

CHOICES_FLIGHTS = (
    ('Scheduled', 'Scheduled'),
    ('On Time', 'On Time'),
    ('Delayed', 'Delayed'),
    ('Departed', 'Departed'),
    ('Arrived', 'Arrived'),
    ('Cancelled', 'Cancelled'),
)

CHOICES_COND = (
    ("Economy", "Economy"),
    ("Comfort", "Comfort"),
    ("Business", "Business"),
)


class AircraftData(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3, db_index=True)
    model = JSONField()
    range = models.PositiveIntegerField()

    class Meta:
        constraints = [
            CheckConstraint(check=(Q(range__gt=0)), name='check_range')
        ]


class AirportsData(gis_models.Model):
    airport_code = gis_models.CharField(primary_key=True, max_length=3, db_index=True)
    airport_name = JSONField()
    city = JSONField()
    coordinates = gis_models.PointField()
    timezone = gis_models.TextField()


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6, db_index=True)
    book_date = models.DateTimeField(auto_now_add=True)  #
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True, db_index=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(AirportsData, on_delete=models.PROTECT)
    arrival_airport = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=CHOICES_FLIGHTS)
    aircraft_code = models.ForeignKey(AircraftData, on_delete=models.PROTECT)#
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['flight_no', 'scheduled_departure'], name='basic'),
            CheckConstraint(check=Q(scheduled_arrival__gte=F('scheduled_departure')), name='greater'),
            CheckConstraint(check=(Q(actual_arrival__isnull=True)
            | (~Q(actual_departure__isnull=True)
            & ~Q(actual_arrival__isnull=True)
            & Q(actual_arrival__gte=F('actual_departure')))), name='complex')
        ]


class Tickets(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13, unique=True)
    book_ref = models.ForeignKey(Bookings, on_delete=models.PROTECT)
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = JSONField(blank=True, null=True)


class TicketFlights(models.Model):
    id = db.MultiFieldPK('ticket_no', 'flight_id')
    ticket_no = models.ForeignKey(Tickets, on_delete=models.PROTECT, db_index=True)
    flight_id = models.ForeignKey(Flights, on_delete=models.PROTECT, db_index=True)
    fare_conditions = models.CharField(max_length=10, choices=CHOICES_COND)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        constraints = [
            CheckConstraint(check=(Q(amount__gte=0)), name='check_amount')
        ]


class BoardingPasses(models.Model):
    id = db.MultiFieldPK('ticket_no', 'flight_id')
    ticket_no = models.ForeignKey(TicketFlights, on_delete=models.PROTECT)
    flight_id = models.ForeignKey(TicketFlights, on_delete=models.PROTECT)
    boarding_no = models.AutoField(unique=True)
    seat_no = models.CharField(max_length=4) #!

    class Meta:
        constraints = [
            UniqueConstraint(fields=['flight_id', 'boarding_no'], name='unique_flight_boarding'), #
            UniqueConstraint(fields=['flight_id', 'seat_no'], name='unique_flight_seat')
        ]


class Seats(models.Model):
    id = db.MultiFieldPK('aircraft_code', 'seat_no')
    aircraft_code = models.ForeignKey(AircraftData, max_length=3, on_delete=models.CASCADE)
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10, choices=CHOICES_COND)












