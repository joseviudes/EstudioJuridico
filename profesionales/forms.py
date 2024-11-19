from django.forms import ModelForm
from django import forms
from .models import Profesional, Secretaria

class ProfesionalForm(ModelForm):
    class Meta:
        model = Profesional
        fields = '__all__'
        exclude = ('usuario','estado')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_egreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'motivo_egreso': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3795 123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
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
        
        self.fields['fecha_ingreso'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_egreso'].input_formats = ['%Y-%m-%d']
        
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


class SecretariaForm(ModelForm):
    class Meta:
        model = Secretaria
        fields = '__all__'
        exclude = ('estado',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_egreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'motivo_egreso': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            
            
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'cod_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3400'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3795 123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
            
            
        }
        
        def __init__(self, *args, **kwargs):
        
            super(SecretariaForm, self).__init__(*args, **kwargs)
            
            self.fields['fecha_ingreso'].input_formats = ['%Y-%m-%d']
            self.fields['fecha_egreso'].input_formats = ['%Y-%m-%d']
            
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