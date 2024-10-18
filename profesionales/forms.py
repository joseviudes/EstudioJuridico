from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Profesional

class ProfesionalForm(ModelForm):
    class Meta:
        model = Profesional
        fields = '__all__'
        exclude = ('usuario',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_egreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3795 123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correodeejemplo@gmail.com'}),
        }
             
    foto = forms.ImageField(
        required=False,  
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',  
            'placeholder': 'Seleccione una imagen',  
            'accept': 'image/*',  
        })
    )
                
    def __init__(self, *args, **kwargs):
        super(ProfesionalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
                # Añadir clase 'required' a los labels de los campos requeridos
                self.fields[field].label_suffix = " *"
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
