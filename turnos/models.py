from django.db import models
from django.db.models import UniqueConstraint

from clientes.models import Cliente
from profesionales.models import Profesional


# Create your models here.
    
    
HORARIOS = (
        ("1", "07:00 a 08:00"),
        ("2", "08:00 a 09:00"),
        ("3", "09:00 a 10:00"),
        ("4", "10:00 a 11:00"),
        ("5", "11:00 a 12:00"),
    )    
    
    
class Turno(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='turnos')
    
    dia = models.DateField(null=True)
    horario = models.CharField(max_length=10, choices=HORARIOS, null=True)
    motivo = models.TextField(max_length=500)  # Motivo del turno
    id_turno = models.AutoField(primary_key=True)  # ID del turno, se genera automáticamente
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['dia', 'horario'], name='unique_dia_horario')
        ]

    def __str__(self):
        return f"Turno para {self.cliente} el {self.dia} a las {self.horario}"