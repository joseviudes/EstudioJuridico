# Generated by Django 5.1.1 on 2024-11-19 02:58

import clientes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0013_remove_cliente_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, validators=[clientes.models.validar_fecha_nacimiento], verbose_name='Fecha de nacimiento'),
        ),
    ]
