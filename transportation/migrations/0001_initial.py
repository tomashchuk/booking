# Generated by Django 3.0.2 on 2020-01-20 16:32

from decimal import Decimal
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AircraftsData',
            fields=[
                ('aircraft_code', models.CharField(max_length=3, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
                ('model', models.TextField()),
                ('range', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'aircrafts_data',
            },
        ),
        migrations.CreateModel(
            name='AirportsData',
            fields=[
                ('airport_code', models.CharField(max_length=3, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
                ('airport_name', django.contrib.postgres.fields.jsonb.JSONField()),
                ('city', django.contrib.postgres.fields.jsonb.JSONField()),
                ('coordinates', models.TextField()),
                ('timezone', models.TextField()),
            ],
            options={
                'db_table': 'airports_data',
            },
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('book_ref', models.CharField(max_length=6, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(limit_value=6)])),
                ('book_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ],
            options={
                'db_table': 'bookings',
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('ticket_no', models.CharField(max_length=13, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
                ('passenger_id', models.CharField(max_length=20)),
                ('passenger_name', models.TextField()),
                ('contact_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('book_ref', models.ForeignKey(db_column='book_ref', on_delete=django.db.models.deletion.PROTECT, to='transportation.Bookings')),
            ],
            options={
                'db_table': 'tickets',
            },
        ),
        migrations.CreateModel(
            name='TicketFlights',
            fields=[
                ('ticket_no', models.ForeignKey(db_column='ticket_no', on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='transportation.Tickets')),
                ('fare_conditions', models.CharField(choices=[('Economy', 'Economy'), ('Comfort', 'Comfort'), ('Business', 'Business')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ],
            options={
                'db_table': 'ticket_flights',
            },
        ),
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_no', models.CharField(max_length=4)),
                ('fare_conditions', models.CharField(choices=[('Economy', 'Economy'), ('Comfort', 'Comfort'), ('Business', 'Business')], max_length=10)),
                ('aircraft_code', models.ForeignKey(db_column='aircraft_code', on_delete=django.db.models.deletion.PROTECT, to='transportation.AircraftsData')),
            ],
            options={
                'db_table': 'seats',
            },
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_no', models.CharField(db_index=True, max_length=6, validators=[django.core.validators.MinLengthValidator(limit_value=6)])),
                ('scheduled_departure', models.DateTimeField()),
                ('scheduled_arrival', models.DateTimeField()),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('On Time', 'On Time'), ('Delayed', 'Delayed'), ('Departed', 'Departed'), ('Arrived', 'Arrived'), ('Cancelled', 'Cancelled')], max_length=20)),
                ('actual_departure', models.DateTimeField(blank=True, null=True)),
                ('actual_arrival', models.DateTimeField(blank=True, null=True)),
                ('aircraft_code', models.ForeignKey(db_column='aircraft_code', on_delete=django.db.models.deletion.PROTECT, to='transportation.AircraftsData')),
                ('arrival_airport', models.ForeignKey(db_column='arrival_airport', on_delete=django.db.models.deletion.PROTECT, related_name='arrivals', to='transportation.AirportsData')),
                ('departure_airport', models.ForeignKey(db_column='departure_airport', on_delete=django.db.models.deletion.PROTECT, related_name='departures', to='transportation.AirportsData')),
            ],
            options={
                'db_table': 'flights',
            },
        ),
        migrations.AddConstraint(
            model_name='aircraftsdata',
            constraint=models.CheckConstraint(check=models.Q(range__gt=0), name='check_range'),
        ),
        migrations.CreateModel(
            name='BoardingPasses',
            fields=[
                ('ticket_no', models.ForeignKey(db_column='ticket_no', on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='tickets', serialize=False, to='transportation.TicketFlights')),
                ('flight_id', models.IntegerField()),
                ('boarding_no', models.IntegerField(unique=True)),
                ('seat_no', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'boarding_passes',
            },
        ),
        migrations.AddField(
            model_name='ticketflights',
            name='flight_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transportation.Flights'),
        ),
        migrations.AddConstraint(
            model_name='seats',
            constraint=models.CheckConstraint(check=models.Q(('fare_conditions', 'Ecomomy'), ('fare_conditions', 'Comfort'), ('fare_conditions', 'Business'), _connector='OR'), name='check_conditions'),
        ),
        migrations.AlterUniqueTogether(
            name='seats',
            unique_together={('aircraft_code', 'seat_no')},
        ),
        migrations.AddConstraint(
            model_name='flights',
            constraint=models.UniqueConstraint(fields=('flight_no', 'scheduled_departure'), name='basic_check'),
        ),
        migrations.AddConstraint(
            model_name='flights',
            constraint=models.CheckConstraint(check=models.Q(scheduled_arrival__gte=django.db.models.expressions.F('scheduled_departure')), name='greater_check'),
        ),
        migrations.AddConstraint(
            model_name='flights',
            constraint=models.CheckConstraint(check=models.Q(('actual_arrival__isnull', True), models.Q(models.Q(_negated=True, actual_departure__isnull=True), models.Q(_negated=True, actual_arrival__isnull=True), ('actual_arrival__gte', django.db.models.expressions.F('actual_departure'))), _connector='OR'), name='complex'),
        ),
        migrations.AddConstraint(
            model_name='flights',
            constraint=models.CheckConstraint(check=models.Q(('status', 'Scheduled'), ('status', 'On Time'), ('status', 'Delayed'), ('status', 'Departed'), ('status', 'Arrived'), ('status', 'Cancelled'), _connector='OR'), name='status_check'),
        ),
        migrations.AlterUniqueTogether(
            name='flights',
            unique_together={('flight_no', 'scheduled_departure')},
        ),
        migrations.AddConstraint(
            model_name='ticketflights',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=0), name='check_amount'),
        ),
        migrations.AddConstraint(
            model_name='ticketflights',
            constraint=models.CheckConstraint(check=models.Q(('fare_conditions', 'Ecomomy'), ('fare_conditions', 'Comfort'), ('fare_conditions', 'Business'), _connector='OR'), name='check_conditions1'),
        ),
        migrations.AlterUniqueTogether(
            name='ticketflights',
            unique_together={('ticket_no', 'flight_id')},
        ),
        migrations.AlterUniqueTogether(
            name='boardingpasses',
            unique_together={('ticket_no', 'flight_id'), ('flight_id', 'boarding_no'), ('flight_id', 'seat_no')},
        ),
    ]
