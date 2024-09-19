# Generated by Django 5.1.1 on 2024-09-18 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('profesionales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('numero_expediente', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('tipo_expediente', models.CharField(choices=[('Alimentos', 'Alimentos'), ('Division de bienes', 'Division de bienes')], max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_finalizacion', models.DateField(blank=True, null=True)),
                ('asunto', models.TextField(max_length=250)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='expedientes', to='clientes.cliente')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='expedientes', to='profesionales.profesional')),
            ],
        ),
        migrations.CreateModel(
            name='Movimientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('Activo', 'Activo'), ('Giro', 'Giro'), ('Paralizado', 'Paralizado')], max_length=50)),
                ('ubicacion', models.CharField(max_length=100)),
                ('observaciones', models.TextField()),
                ('archivos', models.ImageField(blank=True, null=True, upload_to='archivos/')),
                ('expediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expedientes.expediente')),
            ],
            options={
                'verbose_name_plural': 'Movimientos',
            },
        ),
    ]
