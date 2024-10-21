from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Expediente, Movimientos

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = '__all__'
        exclude = ('tipo_expediente','estado')
        widgets = {
            'cliente': forms.Select(attrs={'class':'form-control', 'autofocus': 'autofocus'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_finalizacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'caratula' : forms.TextInput(attrs={'class': 'form-control'})
        }
        
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
                

class MovimientosForm(ModelForm):
    class Meta:
        model = Movimientos
        fields = '__all__'
        exclude = ['expediente']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
        }


    def __init__(self, *args, **kwargs):
        super(MovimientosForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
                self.fields[field].label_suffix = ' *'
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
