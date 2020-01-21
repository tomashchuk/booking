from decimal import Decimal
from django.core.validators import MinValueValidator, MinLengthValidator
from django.contrib.postgres.fields import JSONField
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.db import models


CHOICES_FLIGHTS = [
    ('Scheduled', 'Scheduled'),
    ('On Time', 'On Time'),
    ('Delayed', 'Delayed'),
    ('Departed', 'Departed'),
    ('Arrived', 'Arrived'),
    ('Cancelled', 'Cancelled'),
]
CHOICES_COND = [
    ("Economy", "Economy"),
    ("Comfort", "Comfort"),
    ("Business", "Business"),
]


class AircraftsData(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3, validators=[MinLengthValidator(limit_value=3)])
    model = models.TextField()
    range = models.PositiveIntegerField()

    def __str__(self):
        return self.aircraft_code + " " + str(self.model)

    class Meta:
        constraints = [
            CheckConstraint(check=(Q(range__gt=0)), name='check_range')
        ]
        db_table = 'aircrafts_data'


class AirportsData(models.Model):
    airport_code = models.CharField(primary_key=True, max_length=3, validators=[MinLengthValidator(limit_value=3)])
    airport_name = JSONField()
    city = JSONField()
    coordinates = models.TextField() # проблеми з GDAL бібліотекою, тому не PointField
    timezone = models.TextField()

    def __str__(self):
        return str(self.airport_name) + " " + self.airport_code

    class Meta:
        db_table = 'airports_data'


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6, validators=[MinLengthValidator(limit_value=6)])
    book_date = models.DateTimeField(auto_now_add=True)  #
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.book_ref + " " + self.book_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    class Meta:
        db_table = 'bookings'


class Tickets(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13, validators=[MinLengthValidator(limit_value=3)])
    book_ref = models.ForeignKey(Bookings, on_delete=models.PROTECT, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = JSONField(blank=True, null=True)

    def __str__(self):
        return self.ticket_no

    class Meta:
        db_table = 'tickets'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6, db_index=True, validators=[MinLengthValidator(limit_value=6)])
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(AirportsData, on_delete=models.PROTECT, db_column='departure_airport', to_field='airport_code', related_name='departures')
    arrival_airport = models.ForeignKey(AirportsData, on_delete=models.PROTECT, db_column='arrival_airport', to_field='airport_code', related_name='arrivals')
    status = models.CharField(max_length=20, choices=CHOICES_FLIGHTS)
    aircraft_code = models.ForeignKey(AircraftsData, on_delete=models.PROTECT, db_column='aircraft_code', to_field='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.flight_id) + " " + self.flight_no

    class Meta:
        constraints = [
            UniqueConstraint(fields=['flight_no', 'scheduled_departure'], name='basic_check'),
            CheckConstraint(check=Q(scheduled_arrival__gte=F('scheduled_departure')), name='greater_check'),
            CheckConstraint(check=(Q(actual_arrival__isnull=True)
            | (~Q(actual_departure__isnull=True)
            & ~Q(actual_arrival__isnull=True)
            & Q(actual_arrival__gte=F('actual_departure')))), name='complex'),
            CheckConstraint(check=(Q(status='Scheduled') | Q(status='On Time') | Q(status='Delayed') | Q(status='Departed') | Q(status='Arrived') | Q(status='Cancelled')), name='status_check')
        ]
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)


class TicketFlights(models.Model):
    ticket_no = models.ForeignKey(Tickets, on_delete=models.PROTECT, db_column='ticket_no', primary_key=True, to_field='ticket_no')
    flight_id = models.ForeignKey(Flights, on_delete=models.PROTECT, to_field='flight_id')
    fare_conditions = models.CharField(max_length=10, choices=CHOICES_COND)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return str(self.flight_id) + str(self.ticket_no)

    class Meta:
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight_id'),)
        constraints = [
            CheckConstraint(check=(Q(amount__gte=0)), name='check_amount'),
            CheckConstraint(check=(Q(fare_conditions='Ecomomy') | Q(fare_conditions='Comfort') | Q(fare_conditions='Business')), name='check_conditions1')
        ]


class BoardingPasses(models.Model):
    ticket_no = models.ForeignKey(TicketFlights, on_delete=models.PROTECT, db_column='ticket_no', primary_key=True, to_field='ticket_no', related_name='tickets')
    flight_id = models.IntegerField() # складені ключі не підтримуються
    boarding_no = models.IntegerField(unique=True)
    seat_no = models.CharField(max_length=4)

    def __str__(self):
        return self.boarding_no

    class Meta:
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)
        # constraints = [
        #     UniqueConstraint(fields=['flight_id', 'boarding_no'], name='unique_flight_boarding'), #
        #     UniqueConstraint(fields=['flight_id', 'seat_no'], name='unique_flight_seat')
        # ]


class Seats(models.Model):
    aircraft_code = models.ForeignKey(AircraftsData, on_delete=models.PROTECT, db_column='aircraft_code')
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10, choices=CHOICES_COND)

    def __str__(self):
        return str(self.aircraft_code) + " " + self.seat_no

    class Meta:
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)
        constraints= [
        CheckConstraint(
            check=(Q(fare_conditions='Ecomomy') | Q(fare_conditions='Comfort') | Q(fare_conditions='Business')), name='check_conditions'),

        ]
