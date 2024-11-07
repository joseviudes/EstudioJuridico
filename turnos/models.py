from datetime import date
from django.db import models
from django.db.models import UniqueConstraint
from django.forms import ValidationError

from clientes.models import Cliente
from profesionales.models import Profesional
from .validators import *


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
    dia = models.DateField(null=True, validators=[validar_dia])
    horario = models.CharField(max_length=50, choices=HORARIOS, null=True)
    motivo = models.TextField(max_length=500, null=True, blank=True, default='-')  
    estado = models.CharField(max_length=25, choices=ESTADOS, default='Pendiente de aprobación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        constraints = [
            models.UniqueConstraint(
                fields=['dia', 'horario', 'profesional'],
                name='unique_turno_profesional'
            )
        ]

    def __str__(self):
            return f"Turno {self.id_turno} - {self.cliente.full_name} con {self.profesional.full_name} de {self.horario}"
        
        
class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"