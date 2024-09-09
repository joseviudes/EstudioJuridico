from django.db import models
from profesionales.models import Profesional 
from clientes.models import Cliente
# Create your models here.

ESTADOS = (
    ("Activo", "Activo"),
    ("Giro", "Giro"),
    ("Paralizado", "Paralizado"),
)

TIPOS_EXPEDIENTES = (
    ("Alimentos", "Alimentos"),
    ("Division de bienes", "Division de bienes"),
)

class Expediente(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, related_name="expedientes")
    profesional = models.ForeignKey(Profesional, on_delete=models.DO_NOTHING, related_name="expedientes")
    
    numero_expediente = models.CharField(max_length=50, primary_key=True, unique=True)
    tipo_expediente = models.CharField(max_length=50, choices=TIPOS_EXPEDIENTES)
    fecha_inicio = models.DateField()
    estado = models.CharField(max_length=50, choices=ESTADOS)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    asunto = models.TextField(max_length=250)
    motivo = models.TextField(max_length=250)
    
    def __str__(self):
        return f"Expediente {self.numero_expediente}"