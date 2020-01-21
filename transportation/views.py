from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions

from .models import AirportsData, AircraftsData, Bookings, BoardingPasses, Flights, TicketFlights, Tickets, Seats
from .serializers import AirportsDataSerializer, AircraftsDataSerializer, BookingsSerializer,\
    BoardingPassesSerializer, FlightsSerializer, TicketFlightsSerializer, TicketsSerializer, SeatsSerializer, TokenSerializer, UserSerializer, RSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AirportsDataView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = AirportsData.objects.all()
    serializer_class = AirportsDataSerializer


class AircraftsDataView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = AircraftsData.objects.all()
    serializer_class = AircraftsDataSerializer


class BookingsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer


class BoardingPassesView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = BoardingPasses.objects.all()
    serializer_class = BoardingPassesSerializer


class FlightsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Flights.objects.all()
    serializer_class = FlightsSerializer


class TicketsFlightsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TicketFlights.objects.all()
    serializer_class = TicketFlightsSerializer


class TicketsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer


class SeatsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializer


class LoginView(generics.CreateAPIView):

    """
    auth/login/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsers(generics.CreateAPIView):
    """
    auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = RSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(status=status.HTTP_201_CREATED)