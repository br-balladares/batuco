# Generated by Django 4.2.6 on 2024-09-11 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_contacto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='correo_usu',
            new_name='correo',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='direccion_usu',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='nombre_usu',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='rut_usu',
            new_name='rut',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='correo_vet',
        ),
    ]
