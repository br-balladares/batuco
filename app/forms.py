from django import forms
from .models import Contacto, Usuario, Mascota
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth. models import User
import re


#Formulario de reserva

# formulario de contacto
class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        #fields = ["nombre","correo","tipo_consulta","mensaje","avisos"]
        fields = '__all__'


class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')

    class Meta:
        model = Usuario
        fields = [
            'nombre', 'direccion', 'correo', 'telefono', 
            'ciudad', 'comuna', 'rut', 'icono', 'password'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'icono': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        rut_pattern = re.compile(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]{1}$')
        if not rut_pattern.match(rut):
            raise forms.ValidationError("El RUT debe tener el formato 12.345.678-9.")
        return rut
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$')
        if not password_pattern.match(password):
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un carácter especial.")
        return password

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'direccion', 'telefono', 'ciudad', 'comuna', 'icono'
        ]
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'icono': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre_mascota', 'edad_mascota', 'especie_mascota', 'raza_mascota']

