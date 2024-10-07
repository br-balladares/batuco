from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import UsuarioRegistroForm, UsuarioUpdateForm,ContactoForm
from django.contrib.auth import logout

# Create your views here.
@never_cache
def home(request):
    return render(request, 'app/home.html')

@never_cache
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

@never_cache
def reserva(request):
    return render(request, 'app/reserva.html')

@never_cache
def cuenta(request):
    return render(request, 'app/cuenta.html')

@never_cache
def editar_usuario(request):
    usuario = request.user  # Obtén el usuario actual
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return render(request, 'app/cambio_exitoso.html')  # Redirige a una página de éxito
    else:
        form = UsuarioUpdateForm(instance=usuario)

    return render(request, 'app/actualizar.html', {'form': form})


@never_cache
def registro(request):
    data = {
        'form': UsuarioRegistroForm()
    }
    
    if request.method == 'POST':
        formulario = UsuarioRegistroForm(data=request.POST, files=request.FILES)
        
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            password = formulario.cleaned_data.get('password')  # Obtener la contraseña
            usuario.set_password(password)  # Establecer la contraseña encriptada
            usuario.save()  # Guardar el usuario en la base de datos
            
            # Autenticar el usuario con el correo y la contraseña
            user = authenticate(username=usuario.correo, password=password)  
            if user is not None:  # Verificar que el usuario se autenticó correctamente
                login(request, user)  # Iniciar sesión automáticamente
                messages.success(request, "Te has registrado correctamente")
                return redirect(to="home")
            else:
                messages.error(request, "Error al autenticar el usuario. Por favor, intenta nuevamente.")
        
        data["form"] = formulario 

    return render(request, 'registration/registro.html', data)


@login_required
@never_cache
def perfil(request):
    user = request.user
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actualizado')
            return redirect('perfil')
    else:
        form = UsuarioUpdateForm(instance=user)

    context = {
        'form': form,
        'usuario': user
    }
    return render(request, 'app/perfil.html', context)

@never_cache
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('correo_usu')  # Campo de correo electrónico
        password = request.POST.get('password')

        # Autenticación
        user = authenticate(request, correo_usu=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('perfil')
        else:
            messages.error(request, 'Credenciales inválidas.')
    
    return render(request, 'app/login.html')