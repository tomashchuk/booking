from django.contrib import admin
from .models import AirportsData, AircraftsData, Bookings, BoardingPasses, Flights, TicketFlights, Tickets, Seats

admin.site.register(AirportsData)
admin.site.register(AircraftsData)
admin.site.register(Bookings)
admin.site.register(BoardingPasses)
admin.site.register(Flights)
admin.site.register(TicketFlights)
admin.site.register(Tickets)
admin.site.register(Seats)