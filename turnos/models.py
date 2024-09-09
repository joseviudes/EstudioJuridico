from django.db import models
from clientes.models import Cliente
from profesionales.models import Profesional

# Create your models here.
    
class Turno(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='turnos')
    
    fecha = models.DateField()  # Fecha del turno
    hora = models.TimeField()   # Hora del turno
    motivo = models.TextField(max_length=500)  # Motivo del turno
    id_turno = models.AutoField(primary_key=True)  # ID del turno, se genera automáticamente

    def __str__(self):
        return f"Turno {self.id_turno} - {self.cliente.nombre} " f"{self.cliente.apellido} con {self.profesional.nombre} " f"{self.profesional.apellido} el {self.fecha} a las {self.hora}"