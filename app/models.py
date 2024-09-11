from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
import uuid
import datetime

class CustomUserManager(BaseUserManager):
    def crear_usuario(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def crear_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.crear_usuario(email, password, **extra_fields)

class TipoUsuario(models.Model):
    id_tipo_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_tipo

class Especialidad(models.Model):
    id_especialidad = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_especialidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_especialidad

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_usu = models.CharField(max_length=100)
    direccion_usu = models.CharField(max_length=200)
    correo_usu = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    ciudad = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    rut_usu = models.CharField(max_length=12, unique=True)
    correo_vet = models.EmailField(blank=True, null=True)
    tipo_permiso = models.CharField(max_length=50)
    icono = models.ImageField(upload_to='user_icons/', blank=True, null=True)
    status = models.BooleanField(default=True)

    # Foraneas
    id_tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, blank=True)

    # Campos de Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Campos que generan conflicto con Django's User
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'correo_usu'
    REQUIRED_FIELDS = ['nombre_usu', 'rut_usu']

    def __str__(self):
        return self.correo_usu

class Mascota(models.Model):
    id_mascota = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_mascota = models.CharField(max_length=100)
    edad_mascota = models.IntegerField(null=True, blank=True)
    especie_mascota = models.CharField(max_length=100)
    tipo_mascota = models.CharField(max_length=100)

    #Foranea
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mascotas')

    def __str__(self):
        return self.nombre_mascota

class Tratamiento(models.Model):
    id_tratamiento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_tratamiento = models.CharField(max_length=100)
    costo_tratamiento = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre_tratamiento

class Atencion(models.Model):
    id_atencion = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    motivo_atencion = models.CharField(max_length=1000)
    fecha_atencion = models.DateField(default=datetime.date.today,null=False,blank=False)
    observacion_atencion = models.CharField(max_length=200)

    def __str__(self):
        return f"Atención: {self.motivo_atencion} - {self.fecha_atencion}"

class Ficha(models.Model):
    id_ficha = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sintomas = models.CharField(max_length=1000)
    examenes = models.CharField(max_length=200)
    observacion_ficha = models.CharField(max_length=200)

    # Foraneas
    id_atencion = models.ForeignKey(Atencion, on_delete=models.CASCADE, related_name='atencion')
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascota')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario')
    id_tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='tratamiento')

    def __str__(self):
        return f"Ficha: {self.observacion_ficha} - {self.examenes}"

class Reserva(models.Model):
    id_reserva = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hora_reserva = models.DateTimeField(
        default=datetime.datetime.now,
        null=False,
        blank=False,
        help_text="Fecha y hora de la reserva."
    )

    # Campo de Fecha
    fecha_reserva = models.DateField(
        default=datetime.date.today,
        null=False,
        blank=False,
        help_text="Fecha en la que se hizo la reserva."
    )

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.fecha_reserva} {self.hora_reserva}"




# formulario de contacto
opciones_consulta = [
    [0, "Consulta"],
    [1, "Reclamo"],
    [2, "Sugerencia"],
    [3, "Agradecimientos"],
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre

