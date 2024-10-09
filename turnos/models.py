from datetime import date
from django.db import models
from django.db.models import UniqueConstraint
from django.forms import ValidationError

from clientes.models import Cliente
from profesionales.models import Profesional


# Create your models here.
    
    
HORARIOS = (
        ("1", "07:00 a 07:30"),
        ("2", "07:30 a 08:00"),
        ("3", "08:00 a 08:30"),
        ("4", "08:30 a 09:00"),
        ("5", "09:00 a 09:30"),
        ("6", "09:30 a 10:00"),
        ("7", "10:00 a 10:30"),
        ("8", "10:30 a 11:00"),
        ("9", "11:00 a 11:30"),
    )    
    
def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('No se puede seleccionar una fecha pasada.')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('Seleccione un dia habil.')    
    
class Turno(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='turnos')
    
    dia = models.DateField(null=True, validators=[validar_dia])
    horario = models.CharField(max_length=10, choices=HORARIOS, null=True)
    motivo = models.TextField(max_length=500)  # Motivo del turno
    id_turno = models.AutoField(primary_key=True)  # ID del turno, se genera automáticamente
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['dia', 'horario'], name='unique_dia_horario')
        ]

    def __str__(self):
        return f"Turno para {self.cliente} el {self.dia} a las {self.horario}"