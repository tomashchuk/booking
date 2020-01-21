from .models import AirportsData, BoardingPasses, Seats, Flights, AircraftsData, Bookings
from datetime import datetime

def foo():
    # f = Seats.objects.all()
    # c = Flights(flight_no='0j83h2', scheduled_arrival=datetime.now(), scheduled_departure=datetime.now(), status="Scheduled", departure_airport=AirportsData.objects.get(airport_code='YKS'), arrival_airport=AirportsData.objects.get(airport_code='KHV'), aircraft_code=AircraftsData.objects.get('773'))
    # c = datetime.now()
    # s = c.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    c = Bookings()
    c.book_ref = '1233'
    c.total_amount = 122.3
    c.save()


