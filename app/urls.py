from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('reserva/', reserva, name="reserva"),
    path('cuenta/', cuenta, name="cuenta"),
    path('registro/', registro, name="registro"),
    path('perfil/', perfil, name="perfil"),
    path('login/', user_login, name="login"),
    path('actualizar/', editar_usuario, name="actualizar"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]