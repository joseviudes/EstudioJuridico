# Generated by Django 5.1.1 on 2024-09-18 20:22

import profesionales.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0002_profesional_cod_postal_profesional_direccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='dni',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True, validators=[profesionales.models.validar_dni], verbose_name='Dni'),
        ),
        migrations.AlterField(
            model_name='profesional',
            name='telefono',
            field=models.CharField(help_text='ej: 3794541234', max_length=10, null=True, validators=[profesionales.models.validar_telefono]),
        ),
    ]
