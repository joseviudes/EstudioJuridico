# Generated by Django 5.1.1 on 2024-10-21 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0008_alter_turno_horario'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='estado',
            field=models.CharField(choices=[('libre', 'Libre'), ('reservado', 'Reservado'), ('cancelado', 'Cancelado')], default='libre', max_length=10),
        ),
        migrations.AlterField(
            model_name='turno',
            name='motivo',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]