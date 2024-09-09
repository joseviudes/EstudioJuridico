from django.contrib.auth.models import User
from django.db import models
from profesionales.models import Profesional
from clientes.models import Cliente

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_profesional = models.BooleanField(default=False)  # Campo para distinguir el tipo de usuario
    profesional = models.OneToOneField(Profesional, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username