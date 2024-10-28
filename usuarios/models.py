from django.db import models
from django.contrib.auth.models import AbstractUser

from clientes.models import Cliente
from profesionales.models import Profesional


ROLES = (
  ('Admin', 'Admin'),
  ('Abogado', 'Abogado'),
  ('Cliente', 'Cliente'),
)

class Usuario(AbstractUser):
  
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    profesional = models.OneToOneField(Profesional, on_delete=models.CASCADE, null=True, blank=True)
    
    email = models.EmailField(unique=True, default=None)
    rol = models.CharField(max_length=15, choices=ROLES)
    fecha_ingreso = models.DateTimeField(auto_now_add=True, null=True)
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Puedes incluir otros campos si es necesario

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.email} ({self.rol})"