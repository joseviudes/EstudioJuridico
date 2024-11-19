from django.db.models.base import Model
from django import forms
from .models import Cliente
from datetime import timedelta, date

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ('usuario', 'estado', 'nacionalidad')

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ocupación laboral'}),
            'lugar_laboral': forms.TextInput(attrs={'class': 'form-control'}),
            'años_aportes': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese su direccion'}),
            'cod_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3400'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3795 123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)

        # Fecha actual
        today = date.today()

        # Calcula el rango de fechas permitidas para 'fecha_ingreso'
        start_date = today - timedelta(days=2)  # 2 días antes
        end_date = today + timedelta(days=2)  # 2 días después

        # Establece los valores de min y max para 'fecha_ingreso'
        self.fields['fecha_ingreso'].widget.attrs.update({
            'min': start_date.strftime('%Y-%m-%d'),
            'max': end_date.strftime('%Y-%m-%d'),
        })

        # Calcula la fecha mínima para 'fecha_nacimiento' (100 años atrás)
        min_birth_date = today - timedelta(days=100*365)  # Aproximadamente 100 años atrás

        # Establece los valores de min y max para 'fecha_nacimiento'
        self.fields['fecha_nacimiento'].widget.attrs.update({
            'max': today.strftime('%Y-%m-%d'),  # No permite seleccionar una fecha posterior a la actual
            'min': min_birth_date.strftime('%Y-%m-%d'),  # No permite seleccionar una fecha menor a 100 años atrás
        })

        # Marcar como no obligatorio los campos opcionales
        self.fields['fecha_nacimiento'].required = False  # No es obligatorio
        self.fields['telefono'].required = False  # No es obligatorio
        self.fields['cod_postal'].required = False  # No es obligatorio
        self.fields['ocupacion'].required = False  # No es obligatorio
        self.fields['lugar_laboral'].required = False  # No es obligatorio
        self.fields['años_aportes'].required = False  # No es obligatorio
        self.fields['email'].required = False  # No es obligatorio

        # Aplicar clase 'form-control' y añadir * a campos requeridos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.label_suffix = " *"  # Marca los campos obligatorios con un asterisco
