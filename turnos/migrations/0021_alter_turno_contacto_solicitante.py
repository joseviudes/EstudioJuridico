# Generated by Django 5.1.1 on 2024-11-16 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0020_turno_contacto_solicitante_alter_turno_profesional_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='contacto_solicitante',
            field=models.CharField(blank=True, default='-', max_length=150, null=True, verbose_name='Contacto del solicitante'),
        ),
    ]
