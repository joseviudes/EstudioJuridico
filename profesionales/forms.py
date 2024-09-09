from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Profesional

class ProfesionalForm(ModelForm):
    class Meta:
        model = Profesional
        fields = ['nombre', 'apellido', 'tipo_matricula', 'num_matricula', 'idMatriculaProf', 'especialidad', 'fecha_ingreso', 'fecha_egreso', 'motivo_egreso']
        