from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password', 'rol']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encripta la contraseña
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
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
                
            