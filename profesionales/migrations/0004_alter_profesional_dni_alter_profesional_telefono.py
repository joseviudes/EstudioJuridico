# Generated by Django 5.1 on 2024-09-20 19:43

import profesionales.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0003_alter_profesional_dni_alter_profesional_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='dni',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True, validators=[profesionales.models.validar_dni], verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='profesional',
            name='telefono',
            field=models.CharField(max_length=10, null=True, validators=[profesionales.models.validar_telefono]),
        ),
    ]
