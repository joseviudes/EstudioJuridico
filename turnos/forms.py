from django.forms import ModelForm
from django import forms
from django.forms import ModelForm

from .models import Turno
from profesionales.models import Profesional


class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'solicitante', 'profesional', 'dia', 'horario', 'motivo']
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del solicitante si es que no es un cliente registrado'}),
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el motivo de la consulta'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibe el usuario cuando se inicia el form
        super(TurnoForm, self).__init__(*args, **kwargs)
        
        
        # Filtrar profesionales activos
        self.fields['profesional'].queryset = Profesional.objects.filter(estado=True)
        
        # Ocultar el campo "profesional" si el usuario es abogado
        if user and user.rol == 'Abogado': 
            self.fields.pop('profesional')
            
        if user and user.rol == 'Cliente': 
            self.fields.pop('cliente'),
            self.fields.pop('solicitante')
        
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

    def save(self, commit=True):
        instance = super(TurnoForm, self).save(commit=False)
        
        # Si el rol es "Abogado", asigna automáticamente al profesional
        if hasattr(self, 'user') and self.user.rol == 'Abogado':
            instance.profesional = self.user.profesional 
            
        # Si el rol es "Cliente", asigna automáticamente al profesional
        if hasattr(self, 'user') and self.user.rol == 'Cliente':
            instance.cliente = self.user.cliente 
        
        if commit:
            instance.save()
        return instance

