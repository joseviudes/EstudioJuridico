# Generated by Django 5.1.1 on 2024-09-08 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0002_cliente_remove_contacto_profesional_contacto_cliente_and_more'),
        ('profesionales', '0002_profesional_remove_contacto_cliente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('motivo', models.TextField(max_length=500)),
                ('id_turno', models.AutoField(primary_key=True, serialize=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turnos', to='clientes.cliente')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turnos', to='profesionales.profesional')),
            ],
        ),
    ]
