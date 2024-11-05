from django import forms
from django.db import models

from .models import Usuario, Cliente, Profesional

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Confirmar Contraseña")
    
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
        # Extraemos el rol del usuario si está presente
        self.rol = kwargs.pop('rol', None)
        super().__init__(*args, **kwargs)

        # Configuramos los campos según el rol
        if self.rol == 'Admin':
            self.fields.pop('cliente')
            self.fields.pop('profesional')
            self.fields['password'].label = "Contraseña"
            
        elif self.rol == 'Abogado':
            self.fields.pop('cliente')  # Oculta campo cliente si el rol es Abogado
            self.fields['profesional'].queryset = Profesional.objects.filter(
                models.Q(usuario__isnull=True) | models.Q(dni=self.instance.profesional.dni) if self.instance.profesional else models.Q()
            )

        elif self.rol == 'Cliente':
            self.fields.pop('profesional')  # Oculta campo profesional si el rol es Cliente
            self.fields['cliente'].queryset = Cliente.objects.filter(
                models.Q(usuario__isnull=True) | models.Q(dni=self.instance.cliente.dni) if self.instance.cliente else models.Q()
            )
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Solo valida la confirmación de contraseña si el rol es Admin
        if self.rol == 'Admin' and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data
