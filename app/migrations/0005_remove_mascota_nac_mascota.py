# Generated by Django 5.1.1 on 2024-10-02 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_mascota_nac_mascota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mascota',
            name='nac_mascota',
        ),
    ]