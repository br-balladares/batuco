from django import forms
from .models import Contacto

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['especialidad', 'veterinario', 'fecha', 'hora', 'motivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veterinario'].queryset = Usuario.objects.filter(tipo_usuario='veterinario')






# formulario de contacto
class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'

