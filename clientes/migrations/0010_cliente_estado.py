# Generated by Django 5.1.1 on 2024-10-16 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_cliente_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
