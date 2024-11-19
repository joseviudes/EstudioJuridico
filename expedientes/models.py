from django.db import models
from django.forms import ValidationError
from profesionales.models import Profesional 
from clientes.models import Cliente
import datetime

# Definición de los posibles estados de un expediente
ESTADOS = (
    ("En letra", "En letra"),
    ("A despacho", "A despacho"),
    ("Giro", "Giro"),
    ("En fiscalía", "En fiscalía"),
    ("Prearchivado", "Prearchivado"),
    ("Archivado", "Archivado"),
)

# Tipos de expediente disponibles
TIPOS_EXPEDIENTE = (
    ("DOC", "Documento"),
    ("INV", "Investigación"),
    ("CON", "Contrato"),
    ("TRA", "Tratado"),
    # Agregar más tipos según se necesiten
)

class Expediente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="expedientes")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="expedientes")
    numero_expediente = models.CharField('Nº del expediente', max_length=50, primary_key=True, unique=True)
    caratula = models.TextField(max_length=500, null=True, blank=True)
    jurisdiccion = models.CharField('Jurisdicción', max_length=250, null=True, blank=True)
    dependencia = models.CharField(max_length=250, null=True, blank=True)
    apoderado = models.CharField(max_length=250, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    asunto = models.CharField(max_length=250, null=True, blank=True)
    estado = models.BooleanField(default=True)

    tipo_expediente = models.CharField('Tipo de expediente', max_length=3, choices=TIPOS_EXPEDIENTE, null=True, blank=True)

    def __str__(self):
        return f"Exp. Nº{self.numero_expediente}"

    def save(self, *args, **kwargs):
        # Si el expediente no tiene número asignado, lo generamos
        if not self.numero_expediente:
            self.numero_expediente = self.generar_numero_expediente()
        
        # Guardamos el expediente
        super(Expediente, self).save(*args, **kwargs)
        
    def generar_numero_expediente(self):
        """
        Genera el número de expediente en formato AAMM-NNNN-XXX.
        """
        # Verificamos que tipo_expediente no sea None
        if not self.tipo_expediente:
            raise ValidationError("El campo 'tipo_expediente' es obligatorio.")

        # Obtener el año y mes actual
        anio_mes = datetime.date.today().strftime("%y%m")  # AAMM (por ejemplo, 2411 para noviembre 2024)

        # Contamos cuántos expedientes del mismo tipo existen para ese año y mes
        secuencia = Expediente.objects.filter(
            numero_expediente__startswith=f"{anio_mes}-",  # Filtramos por año y mes
            tipo_expediente=self.tipo_expediente  # Filtrar por el tipo de expediente
        ).count() + 1  # +1 para el siguiente número secuencial

        # Generamos el número de expediente completo con el tipo de expediente
        return f"{anio_mes}-{secuencia:04d}-{self.tipo_expediente[:3].upper()}"


def validar_tipo_archivo(archivos):
    tipos_permitidos = ['pdf', 'doc', 'docx', 'jpg', 'png', 'txt', 'pptx']
    extension = archivos.name.split('.')[-1].lower()
    if extension not in tipos_permitidos:
        raise ValidationError(f'El archivo debe ser de los siguientes tipos: {", ".join(tipos_permitidos)}')
  

class Movimientos(models.Model):
    
    id_mov = models.AutoField(primary_key=True)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    fecha = models.DateField(null=True)
    sit_actual = models.CharField('Situación actual', max_length=50, choices=ESTADOS, null=True)
    tipo = models.CharField(max_length=150, null=True)
    detalle = models.TextField(max_length=500, null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True)
    # documentos = models.FileField(upload_to='documentos/', null=True, blank=True, validators=[validar_tipo_archivo])

    class Meta:
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return f"Mov {self.id} - {self.expediente.numero_expediente}"
    

class Documentos(models.Model):
    movimiento = models.ForeignKey(Movimientos, on_delete=models.CASCADE, related_name='documentos')
    documentos = models.FileField(upload_to='documentos/', validators=[validar_tipo_archivo])

    def __str__(self):
        return f"Documento para movimiento {self.movimiento.id_mov}"

    
    
    