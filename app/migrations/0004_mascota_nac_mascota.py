# Generated by Django 5.1.1 on 2024-10-02 18:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_correo_usu_usuario_correo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='nac_mascota',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
