from django import forms
from .models import Contacto, Reserva
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth. models import User


#Formulario de reserva





# formulario de contacto
class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        #fields = ["nombre","correo","tipo_consulta","mensaje","avisos"]
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']