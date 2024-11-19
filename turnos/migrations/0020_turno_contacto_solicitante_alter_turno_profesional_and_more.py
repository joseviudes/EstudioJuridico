# Generated by Django 5.1.1 on 2024-11-16 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0022_remove_profesional_usuario'),
        ('turnos', '0019_alter_turno_horario'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='contacto_solicitante',
            field=models.CharField(blank=True, default='-', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='profesional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turnos', to='profesionales.profesional'),
        ),
        migrations.AlterField(
            model_name='turno',
            name='solicitante',
            field=models.CharField(blank=True, default='-', max_length=100, null=True),
        ),
    ]