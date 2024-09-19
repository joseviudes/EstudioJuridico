from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Turno


class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ['profesional', 'dia', 'horario', 'motivo']
        
