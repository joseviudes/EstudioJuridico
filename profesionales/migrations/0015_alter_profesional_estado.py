# Generated by Django 5.1.1 on 2024-10-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0014_alter_profesional_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]