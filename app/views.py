from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def contacto(request):
    return render(request, 'app/contacto.html')

def reserva(request):
    return render(request, 'app/reserva.html')

def cuenta(request):
    return render(request, 'app/cuenta.html')