from rest_framework import serializers
from .models import AirportsData, AircraftsData, Bookings, BoardingPasses, Flights, TicketFlights, Tickets, Seats
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class RSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class AirportsDataSerializer(serializers.HyperlinkedModelSerializer):
    # def validate(self, data):
    #     code = data['airport_code']
    #     if len(code) != 3:
    #         raise serializers.ValidationError('Inval')
    #     return data

    class Meta:
        model = AirportsData
        fields = ('airport_code', 'url', 'airport_name', 'city', 'coordinates', 'timezone')


class AircraftsDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AircraftsData
        fields = ('aircraft_code', 'url', 'model', 'range')


class BookingsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bookings
        fields = ('book_ref', 'url', 'book_date', 'total_amount')


class BoardingPassesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BoardingPasses
        fields = ('ticket_no', 'url', 'flight_id', 'boarding_no', 'seat_no')


class TicketsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tickets
        fields = ('ticket_no', 'url', 'passenger_id', 'passenger_name', 'contact_data', 'book_ref',)


class FlightsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Flights
        fields = ('flight_id', 'url', 'flight_no', 'scheduled_departure',
                  'scheduled_arrival', 'status',  'actual_departure',
                  'actual_arrival', 'aircraft_code', 'arrival_airport',
                  'departure_airport')


class TicketFlightsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TicketFlights
        fields = ('ticket_no', 'url', 'flight_id',  'fare_conditions', 'amount')


class SeatsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Seats
        fields = ('id', 'url', 'seat_no', 'fare_conditions', 'aircraft_code')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)