# Generated by Django 5.1.1 on 2024-09-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True, verbose_name='Dni'),
        ),
    ]
