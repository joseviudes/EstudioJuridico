from django.db import models
from usuarios.models import Usuario

# Create your models here.

class Notificacion(models.Model):
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_Creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    
    