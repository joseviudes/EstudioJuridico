from django.forms import ModelForm
from django import forms
from .models import Turno

class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ['profesional', 'dia', 'horario', 'motivo']
        
        widgets = {
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la fecha', 'type': 'date'}),
            'horario': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese el horario'}), 
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el motivo de la consulta'}),
        }

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
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