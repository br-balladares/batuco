from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('reserva/', reserva, name="reserva"),
    path('cuenta/', cuenta, name="cuenta"),
    path('registro/', registro, name="registro"),
]