# Generated by Django 5.1.1 on 2024-10-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0018_alter_profesional_idmatriculaprof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='idMatriculaProf',
            field=models.IntegerField(unique=True, verbose_name='Nº de matricula del profesional'),
        ),
    ]
