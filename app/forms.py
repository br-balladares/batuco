from django import forms
from .models import Contacto, Reserva


#Formulario de reserva





# formulario de contacto
class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        #fields = ["nombre","correo","tipo_consulta","mensaje","avisos"]
        fields = '__all__'

