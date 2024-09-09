from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        