from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Expediente

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ExpedienteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
                    # Añadir clase 'required' a los labels de los campos requeridos
                self.fields[field].label_suffix = ' *'
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })