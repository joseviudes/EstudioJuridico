from django import forms
from .models import Usuario, Cliente, Profesional

class UsuarioForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    
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