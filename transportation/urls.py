from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('airports', views.AirportsDataView)
router.register('aircrafts', views.AircraftsDataView)
router.register('bookings', views.BookingsView)
router.register('tickets', views.TicketsView)
router.register('flights', views.FlightsView)
router.register('ticketflights', views.TicketsFlightsView)
router.register('boardingpasses', views.BoardingPassesView)
router.register('seats', views.SeatsView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/login/', views.LoginView.as_view(), name="auth-login"),
    path('auth/register/', views.RegisterUsers.as_view(), name="auth-register"),

]
