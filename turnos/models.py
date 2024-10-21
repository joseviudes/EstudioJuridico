from datetime import date
from django.db import models
from django.db.models import UniqueConstraint
from django.forms import ValidationError

from clientes.models import Cliente
from profesionales.models import Profesional


# Create your models here.
    
    
HORARIOS = (
        ("07:00 a 07:30", "07:00 a 07:30"),
        ("07:30 a 08:00", "07:30 a 08:00"),
        ("08:00 a 08:30", "08:00 a 08:30"),
        ("08:30 a 09:00", "08:30 a 09:00"),
        ("09:00 a 09:30", "09:00 a 09:30"),
        ("09:30 a 10:00", "09:30 a 10:00"),
        ("10:00 a 10:30", "10:00 a 10:30"),
        ("10:30 a 11:00", "10:30 a 11:00"),
        ("11:00 a 11:30", "11:00 a 11:30"),
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
    horario = models.CharField(max_length=50, choices=HORARIOS, null=True)
    motivo = models.TextField(max_length=500)  # Motivo del turno
    id_turno = models.AutoField(primary_key=True)  # ID del turno, se genera automáticamente
    
    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        constraints = [
            models.UniqueConstraint(
                fields=['dia', 'horario', 'profesional'],
                name='unique_turno_profesional'
            )
        ]

    def __str__(self):
        return f"Turno {self.id_turno} - {self.cliente.get_full_name()} con {self.profesional.get_full_name()} de {self.horario}"