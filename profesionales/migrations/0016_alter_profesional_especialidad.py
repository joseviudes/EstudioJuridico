# Generated by Django 5.1.1 on 2024-10-20 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0015_alter_profesional_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='especialidad',
            field=models.CharField(blank=True, choices=[('Familia', 'Familia'), ('Laboral', 'Laboral')], max_length=200, null=True),
        ),
    ]
