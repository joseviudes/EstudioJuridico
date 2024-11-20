from django.forms import ModelForm
from django import forms
from django.forms import ModelForm
from datetime import date

from .models import Turno
from profesionales.models import Profesional


class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'solicitante','contacto_solicitante' ,'profesional', 'dia', 'horario', 'motivo']
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del solicitante si es que no es un cliente registrado'}),
            'contacto_solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese telefono o email '}),
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': date.today().strftime('%Y-%m-%d'), 'id': 'id_dia', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
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
            
        if user and user.rol == 'Secretaria': 
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
                
    def clean_dia(self):
        dia = self.cleaned_data.get('dia')
        if dia < date.today():
            raise forms.ValidationError("La fecha no puede ser pasada.")
        
        # Obtener el nombre del día
        nombre_dia = dia.strftime("%A")  # Esto devuelve el día en texto como 'Monday', 'Tuesday', etc.
        
        if nombre_dia in ["Saturday", "Sunday"]:
            raise forms.ValidationError("No se permiten turnos los sábados o domingos.")
        
        return dia
    

    def save(self, commit=True):
        instance = super(TurnoForm, self).save(commit=False)
        
        # Si el rol es "Abogado", asigna automáticamente al profesional
        if hasattr(self, 'user') and self.user.rol == 'Abogado':
            instance.profesional = self.user.profesional 
            
        # Si el rol es "Abogado", asigna automáticamente al profesional
        if hasattr(self, 'user') and self.user.rol == 'Secretaria':
            instance.profesional = self.user.secretaria.profesional 
            
        # Si el rol es "Cliente", asigna automáticamente al cliente
        if hasattr(self, 'user') and self.user.rol == 'Cliente':
            instance.cliente = self.user.cliente 
        
        if commit:
            instance.save()
        return instance

