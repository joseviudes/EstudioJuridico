from django import forms
from django.db import models

from .models import Usuario, Cliente, Profesional
from profesionales.models import Secretaria

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Contraseña")

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(usuario__isnull=True),
        required=False,
        label="Vincular Cliente"
    )
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.filter(usuario__isnull=True),
        required=False,
        label="Vincular Profesional"
    )
    
    secretaria = forms.ModelChoiceField(
        queryset=Secretaria.objects.filter(usuario__isnull=True),
        required=False,
        label="Vincular Secretaria"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'cliente', 'profesional', 'secretaria']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'secretaria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el rol del usuario si está presente
        self.rol = kwargs.pop('rol', None)
        super().__init__(*args, **kwargs)

        # Configuramos los campos según el rol
        if self.rol == 'Admin':
            # Oculta los campos de cliente y profesional si el rol es Admin
            self.fields.pop('cliente')
            self.fields.pop('profesional')
            self.fields.pop('secretaria')
            self.fields['password'].label = "Contraseña"
            
        elif self.rol == 'Abogado':
            # Oculta el campo cliente si el rol es Abogado
            self.fields.pop('cliente')
            self.fields.pop('secretaria')
            # Filtra los profesionales para mostrar solo aquellos sin usuario asignado o el actual
            self.fields['profesional'].queryset = Profesional.objects.filter(
                models.Q(usuario__isnull=True) | 
                models.Q(dni=self.instance.profesional.dni) if self.instance.profesional else models.Q()
            )

        elif self.rol == 'Cliente':
            # Oculta el campo profesional si el rol es Cliente
            self.fields.pop('profesional')
            self.fields.pop('secretaria')
            # Filtra los clientes para mostrar solo aquellos sin usuario asignado o el actual
            self.fields['cliente'].queryset = Cliente.objects.filter(
                models.Q(usuario__isnull=True) | 
                models.Q(dni=self.instance.cliente.dni) if self.instance.cliente else models.Q()
            )

        elif self.rol == 'Secretaria':
            # Oculta el campo profesional si el rol es Cliente
            self.fields.pop('cliente')
            
            # Filtra los clientes para mostrar solo aquellos sin usuario asignado o el actual
            self.fields['secretaria'].queryset = Secretaria.objects.filter(
                models.Q(usuario__isnull=True) | 
                models.Q(dni=self.instance.secretaria.dni) if self.instance.secretaria else models.Q()
            )