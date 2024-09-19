import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group, Permission


class Usuario(AbstractBaseUser, PermissionsMixin):
    
    usuario = models.CharField(max_length=30, unique=True, help_text='Su nombre de usuario debe ser su nombre completo.')
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fecha_joined = models.DateTimeField('Fecha que se unió', auto_now_add=True)
    
    groups = models.ManyToManyField(Group, related_name='usuario_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='usuario_permissions', blank=True)
    
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return self.nombre or self.usuario
    
    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(' ')[0]