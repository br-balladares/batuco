from django.contrib import admin
from .models import Contacto, Usuario, Reserva, TipoUsuario, Mascota
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Reserva)
admin.site.register(Contacto)
admin.site.register(TipoUsuario)
admin.site.register(Mascota)
