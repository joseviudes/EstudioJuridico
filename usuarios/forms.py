from django import forms
from django.db import models

from .models import Usuario, Cliente, Profesional

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Hacer que la contraseña sea opcional
    
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

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'cliente', 'profesional']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Verificar si el usuario ya tiene un cliente/profesional vinculado y ajustar el queryset
        if self.instance and self.instance.cliente:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                models.Q(usuario__isnull=True) | models.Q(dni=self.instance.cliente.dni)
            )
        
        if self.instance and self.instance.profesional:
            self.fields['profesional'].queryset = Profesional.objects.filter(
                models.Q(usuario__isnull=True) | models.Q(dni=self.instance.profesional.dni)
            )
