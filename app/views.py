from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import UsuarioRegistroForm, UsuarioUpdateForm,ContactoForm, MascotaForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
@login_required
def editar_usuario(request):
    usuario = request.user
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información actualizada exitosamente.', extra_tags='perfil')
            return redirect('perfil')
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


@login_required
def mascota(request):
    usuario = request.user

    # Manejar la eliminación de mascotas
    if request.method == 'POST' and 'mascota_id' in request.POST:
        mascota_id = request.POST['mascota_id']
        try:
            # Busca la mascota utilizando el UUID
            mascota = Mascota.objects.get(id_mascota=mascota_id, id_usuario=usuario)
            mascota.delete()
            messages.success(request, '¡Mascota eliminada con éxito!')
        except Mascota.DoesNotExist:
            messages.error(request, 'La mascota no existe o no te pertenece.')

    # Obtener las mascotas del usuario
    mascotas = Mascota.objects.filter(id_usuario=usuario)
    return render(request, 'app/mascota.html', {'mascotas': mascotas})

@login_required
def agregar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.id_usuario = request.user  # Asignar el usuario actual
            mascota.save()
            messages.success(request, 'Mascota agregada con éxito.')
            return redirect('mascota')  # Redirigir a la vista de mascotas
    else:
        form = MascotaForm()
    
    return render(request, 'app/agregar_mascota.html', {'form': form})

def calcular_edad(fecha_nacimiento):
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

@csrf_exempt
def administracion_view(request):
    # Cargar los datos que necesitas de cada modelo
    usuarios = list(Usuario.objects.values(
        'id_usuario', 'nombre', 'direccion', 'correo', 
        'telefono', 'ciudad', 'comuna', 'rut', 
        'tipo_permiso', 'status'
    ))
    
    for usuario in usuarios:
        usuario['id_usuario'] = str(usuario['id_usuario'])  # Convertir UUID a string
        usuario['status'] = str(usuario['status'])  # Asegurarse de que el status sea un string

    roles = list(TipoUsuario.objects.values(
        'id_tipo_usuario', 'nombre_tipo'
    ))

    mascotas = list(Mascota.objects.values(
        'id_mascota', 'nombre_mascota', 'edad_mascota', 
        'especie_mascota', 'raza_mascota', 'id_usuario' 
    ))

    reservas = list(Reserva.objects.values(
        'id_reserva', 'fecha_reserva', 'hora_reserva'
    ))
    
    for mascota in mascotas:
        mascota['id_mascota'] = str(mascota['id_mascota'])  # Convertir UUID a string
        mascota['id_usuario'] = str(mascota['id_usuario'])  # Convertir UUID a string

    if request.method == 'POST':
        # Manejar la actualización del usuario
        if request.POST.get('action') == 'update':
            user_id = request.POST.get('id_usuario')
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            tipo_permiso = request.POST.get('tipo_permiso')

            try:
                # Convertir el user_id de vuelta a UUID
                user_id_uuid = uuid.UUID(user_id)
                
                usuario = Usuario.objects.get(id_usuario=user_id_uuid)
                usuario.nombre = nombre
                usuario.correo = correo
                usuario.tipo_permiso = tipo_permiso
                usuario.save()
                messages.success(request, 'Usuario actualizado correctamente.')
                return HttpResponse('Usuario actualizado exitosamente.')
            except Usuario.DoesNotExist:
                return HttpResponse('Usuario no encontrado.', status=404)
            except ValueError:
                return HttpResponse('ID de usuario no es un UUID válido.', status=400)

        # Manejar la eliminación del usuario
        elif request.POST.get('action') == 'delete':
            user_id = request.POST.get('id_usuario')
            try:
                # Convertir el user_id de vuelta a UUID
                user_id_uuid = uuid.UUID(user_id)
                
                Usuario.objects.filter(id_usuario=user_id_uuid).delete()
                return JsonResponse({'message': 'Usuario eliminado correctamente.'}, status=200)
            except ValueError:
                return JsonResponse({'error': 'ID de usuario no es un UUID válido.'}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'Error al eliminar el usuario: ' + str(e)}, status=400)

    # Devolver la plantilla
    context = {
        'usuarios': usuarios,
        'roles': roles,
        'mascotas': mascotas,
        'reservas': reservas,
    }
    return render(request, 'app/administracion.html', context)




@csrf_exempt
def save_mascota(request):
    if request.method == 'POST':
        data = request.POST
        mascota = Mascota.objects.get(id_mascota=data['id_mascota'])
        mascota.nombre_mascota = data['nombre_mascota']
        mascota.edad_mascota = data['edad_mascota']
        mascota.especie_mascota = data['especie_mascota']
        mascota.raza_mascota = data['raza_mascota']
        mascota.save()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_mascota(request):
    if request.method == 'POST':
        mascota_id = request.POST.get('id_mascota')
        Mascota.objects.filter(id_mascota=mascota_id).delete()
        return JsonResponse({'status': 'deleted'})



