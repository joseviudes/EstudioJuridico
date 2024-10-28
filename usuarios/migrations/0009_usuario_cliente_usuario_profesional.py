# Generated by Django 5.1.1 on 2024-10-23 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0013_remove_cliente_usuario'),
        ('profesionales', '0022_remove_profesional_usuario'),
        ('usuarios', '0008_alter_usuario_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cliente',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='profesional',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profesionales.profesional'),
        ),
    ]