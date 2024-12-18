# Generated by Django 5.1.1 on 2024-11-19 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expedientes', '0020_alter_movimientos_fecha_alter_movimientos_sit_actual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='tipo_expediente',
            field=models.CharField(blank=True, choices=[('FAM', 'Familia'), ('LAB', 'Laboral'), ('JUB', 'Jubilación'), ('SUC', 'Sucesorios')], max_length=3, null=True, verbose_name='Tipo de expediente'),
        ),
    ]
