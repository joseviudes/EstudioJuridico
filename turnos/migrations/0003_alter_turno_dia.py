# Generated by Django 5.1 on 2024-10-03 19:39

import turnos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0002_alter_turno_dia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='dia',
            field=models.DateField(null=True, validators=[turnos.models.validar_dia]),
        ),
    ]
