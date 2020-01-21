from django.contrib import admin
from .models import AirportsData, AircraftsData, Bookings, BoardingPasses, Flights, TicketFlights, Tickets, Seats

admin.site.register(AirportsData, AircraftsData, Bookings, BoardingPasses, Flights, TicketFlights, Tickets, Seats)
