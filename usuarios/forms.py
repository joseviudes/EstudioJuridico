from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['usuario', 'nombre', 'email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['usuario', 'email', 'is_active', 'is_staff']
