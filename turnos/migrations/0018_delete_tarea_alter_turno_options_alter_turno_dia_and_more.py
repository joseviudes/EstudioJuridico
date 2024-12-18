# Generated by Django 5.1.1 on 2024-11-10 23:25

import turnos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0017_tarea'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tarea',
        ),
        migrations.AlterModelOptions(
            name='turno',
            options={'ordering': ['-fecha_creacion']},
        ),
        migrations.AlterField(
            model_name='turno',
            name='dia',
            field=models.DateField(default='2024-01-01', validators=[turnos.validators.validar_dia]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='turno',
            name='horario',
            field=models.CharField(choices=[('07:00 a 07:30', '07:00 a 07:30'), ('07:30 a 08:00', '07:30 a 08:00'), ('08:00 a 08:30', '08:00 a 08:30'), ('08:30 a 09:00', '08:30 a 09:00'), ('09:00 a 09:30', '09:00 a 09:30'), ('09:30 a 10:00', '09:30 a 10:00'), ('10:00 a 10:30', '10:00 a 10:30'), ('10:30 a 11:00', '10:30 a 11:00'), ('11:00 a 11:30', '11:00 a 11:30')], default='07:00 a 07:30', max_length=50),
            preserve_default=False,
        ),
    ]
