from django.db import models
from django.forms import ValidationError
from profesionales.models import Profesional 
from clientes.models import Cliente
# Create your models here.

ESTADOS = (
    ("En letra", "En letra"),
    ("A despacho", "A despacho"),
    ("Giro", "Giro"),
    ("En fiscalía", "En fiscalía"),
    ("Prearchivado", "Prearchivado"),
    ("Archivado", "Archivado"),
    
)

TIPOS_EXPEDIENTES = (
    ("Alimentos", "Alimentos"),
    ("Division de bienes", "Division de bienes"),
)

class Expediente(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="expedientes")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="expedientes")
    
    numero_expediente = models.CharField(max_length=50, primary_key=True, unique=True)
    tipo_expediente = models.CharField(max_length=50, choices=TIPOS_EXPEDIENTES)
    apoderado = models.CharField(max_length=250, null=True, blank=True, default="-")
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    asunto = models.TextField(max_length=250)
    
    def __str__(self):
        return f"Exp. Nº{self.numero_expediente}"
    
    
def validar_tipo_archivo(archivos):
    tipos_permitidos = ['pdf', 'doc', 'docx', 'jpg', 'png', 'txt']
    extension = archivos.name.split('.')[-1].lower()
    if extension not in tipos_permitidos:
        raise ValidationError(f'El archivo debe ser de los siguientes tipos: {", ".join(tipos_permitidos)}')
  

class Movimientos(models.Model):
    
    id_mov = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    fecha = models.DateField(default="-", null=True, blank=True)
    sit_actual = models.CharField('Situación actual', max_length=50, choices=ESTADOS, null=True, blank=True, default="-")
    tipo = models.CharField(default="-", max_length=150, null=True, blank=True)
    detalle = models.TextField(default="-", max_length=500, null=True, blank=True)
    ubicacion = models.CharField(default="-", max_length=100, null=True, blank=True)
    archivos = models.FileField(upload_to='documentos/', null=True, blank=True, validators=[validar_tipo_archivo])

    class Meta:
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return f"Mov {self.id} - {self.expediente.numero_expediente}"

    
    
    