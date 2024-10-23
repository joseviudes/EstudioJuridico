from django.forms import ModelForm
from django import forms
from django.forms import ModelForm
from .models import Turno

class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        # Incluimos nombre_completo y dni en los campos del formulario
        fields = ['nombre_completo', 'dni', 'telefono','profesional', 'dia', 'horario', 'motivo']
        
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre completo'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su DNI'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3795 123456'}),
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el motivo de la consulta'}),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)  
        super(TurnoForm, self).__init__(*args, **kwargs)
        
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
        
        if user and user.is_authenticated:
            self.fields['nombre_completo'].widget = forms.HiddenInput()
            self.fields['dni'].widget = forms.HiddenInput()
            self.fields['telefono'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        cliente = self.instance.cliente  # Verificamos si ya hay un cliente asignado
        user = self.initial.get('user')  # Obtenemos el usuario pasado desde la vista

        # Si el usuario no está autenticado, los campos nombre_completo y dni deben ser obligatorios
        if not user or not user.is_authenticated:
            nombre_completo = cleaned_data.get('nombre_completo')
            dni = cleaned_data.get('dni')
            telefono = cleaned_data.get('telefono')

            if not nombre_completo:
                self.add_error('nombre_completo', "Este campo es obligatorio para usuarios no registrados.")
            if not dni:
                self.add_error('dni', "Este campo es obligatorio para usuarios no registrados.")
            if not telefono:
                self.add_error('telefono', "Este campo es obligatorio para usuarios no registrados.")
        
        return cleaned_data

