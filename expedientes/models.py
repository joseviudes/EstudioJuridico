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
    apoderado = models.CharField(max_length=250, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    asunto = models.TextField(max_length=250)
    
    def __str__(self):
        return f"Exp. Nº{self.numero_expediente}"
    
    
class Movimientos(models.Model):
    
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADOS)
    ubicacion = models.CharField(max_length=100)
    observaciones = models.TextField()
    archivos = models.ImageField(upload_to='archivos/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return f"Mov {self.id} - {self.expediente.numero_expediente}"

    
    
    