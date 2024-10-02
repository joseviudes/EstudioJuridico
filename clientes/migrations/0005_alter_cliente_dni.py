# Generated by Django 5.1 on 2024-09-20 19:43

import clientes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True, validators=[clientes.models.validar_dni], verbose_name='DNI'),
        ),
    ]
