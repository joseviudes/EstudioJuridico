# Generated by Django 5.1.1 on 2024-10-11 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_cliente_usuario'),
        ('expedientes', '0002_expediente_apoderado'),
        ('profesionales', '0013_profesional_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expedientes', to='clientes.cliente'),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='profesional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expedientes', to='profesionales.profesional'),
        ),
    ]
