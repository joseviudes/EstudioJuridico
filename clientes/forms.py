from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ('usuario', 'estado', 'nacionalidad')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            # 'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            # 'nacionalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nacionalidad'}),
            'ocupación': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ocupación'}),
            'lugar_laboral': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar laboral'}),
            'años_aportes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Años de aportes'}),
            
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese su direccion'}),
            'cod_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3400'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3795 123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),

        }
        
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
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
        
        