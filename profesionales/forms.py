from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Profesional

class ProfesionalForm(ModelForm):
    class Meta:
        model = Profesional
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ProfesionalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.required:
                field.widget.attrs['class'] = 'required-field'