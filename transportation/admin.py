from django.contrib import admin
from .models import AirportsData, AircraftsData, Bookings, BoardingPasses, Flights, TicketFlights, Tickets, Seats

admin.site.register(AirportsData, AircraftsData)
admin.site.register(Bookings, BoardingPasses)
admin.site.register(Flights, TicketFlights)
admin.site.register(Tickets, Seats)