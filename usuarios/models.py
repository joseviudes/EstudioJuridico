from django.db import models
from django.core import validators
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group, Permission
from django.contrib.auth.models import User


class Usuario(models.Model):
    usuario = models.ForeignKey(User, related_name="usuarios", 
		on_delete=models.DO_NOTHING)
    fecha_ingreso = models.DateTimeField(auto_now_add=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
         verbose_name = 'Usuario'
         verbose_name_plural = 'Usuarios'
         
    def __str__(self):
		    return (
			f"{self.usuario} "
			f"({self.fecha_ingreso:%Y-%m-%d %H:%M}): ")
 