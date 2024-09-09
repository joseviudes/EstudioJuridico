from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Expediente

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = '__all__'
        