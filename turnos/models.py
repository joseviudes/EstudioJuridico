from django.db import models

from clientes.models import Cliente
from profesionales.models import Profesional
from .validators import *


HORARIOS = (
        ("08:00 a 08:30", "08:00 a 08:30"),
        ("08:30 a 09:00", "08:30 a 09:00"),
        ("09:00 a 09:30", "09:00 a 09:30"),
        ("09:30 a 10:00", "09:30 a 10:00"),
        ("10:00 a 10:30", "10:00 a 10:30"),
        ("10:30 a 11:00", "10:30 a 11:00"),
        ("11:00 a 11:30", "11:00 a 11:30"),
        ("11:30 a 12:00", "11:30 a 12:00"),
        
        ("17:00 a 17:30", "17:00 a 17:30"),
        ("17:30 a 18:00", "17:30 a 18:00"),
        ("18:00 a 18:30", "18:00 a 18:30"),
        ("18:30 a 19:00", "18:30 a 19:00"),
        ("19:00 a 19:30", "19:00 a 19:30"),
        ("19:30 a 20:00", "19:30 a 20:00"),
        ("20:00 a 20:30", "20:00 a 20:30"),
        ("20:30 a 21:00", "20:30 a 21:00"),
    )    

ESTADOS = (
    ('Pendiente de aprobación', 'Pendiente de aprobación'),
    ('Aprobado', 'Aprobado'),
    ('Cancelado', 'Cancelado'),
    ('Concluido','Concluido'),
)  
    
class Turno(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos', null=True, blank=True, default='-')
    solicitante = models.CharField(max_length=100, null=True, blank=True)
    
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='turnos', default='-')
    
    id_turno = models.AutoField(primary_key=True)
    dia = models.DateField(validators=[validar_dia])
    horario = models.CharField(max_length=50, choices=HORARIOS)
    motivo = models.TextField(max_length=500, null=True, blank=True, default='-')  
    estado = models.CharField(max_length=25, choices=ESTADOS, default='Pendiente de aprobación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-fecha_creacion']
        constraints = [
            models.UniqueConstraint(
                fields=['dia', 'horario', 'profesional'],
                name='unique_turno_profesional'
            )
        ]

    def __str__(self):
            return f"Turno {self.id_turno} - {self.cliente.full_name} con {self.profesional.full_name} de {self.horario}"
        
        