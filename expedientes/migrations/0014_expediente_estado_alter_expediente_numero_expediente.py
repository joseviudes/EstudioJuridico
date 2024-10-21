# Generated by Django 5.1.1 on 2024-10-20 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expedientes', '0013_remove_expediente_tipo_expediente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='numero_expediente',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='Nº del expediente'),
        ),
    ]
