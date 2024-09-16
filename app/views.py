from django.shortcuts import render
from .models import *
from .forms import ContactoForm

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "contacto guardado"
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html', data)

def reserva(request):
    return render(request, 'app/reserva.html')

def cuenta(request):
    return render(request, 'app/cuenta.html')