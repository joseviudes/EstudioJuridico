from django.db import models
from django.forms import ValidationError

# Create your models here.

TIPO_DE_MATRICULA = (
    ("DNI", "DNI"),
    ("CUIL", "CUIL")
)

ESPECIALIDADES = (
    ("FLIA", "Familia"),
    ("LAB", "Laboral")
)

def validar_telefono(value):
    if len(value) != 10:
        raise ValidationError('El telefono debe tener 10 numeros.')
    if not value.isdigit():
        raise ValidationError('El telefono debe contener solo números.')


class Profesional(models.Model):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    tipo_matricula = models.CharField(max_length=200, choices=TIPO_DE_MATRICULA, default="DNI")
    num_matricula = models.IntegerField(primary_key=True, unique=True, default=0) #  PK y de valor unico
    idMatriculaProf = models.IntegerField(unique=True)
    especialidad = models.CharField(max_length=200, choices=ESPECIALIDADES)
    fecha_ingreso = models.DateField()  
    fecha_egreso = models.DateField(null=True, blank=True)  # es opcional
    motivo_egreso = models.TextField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return f"{self.apellido} " + f"{self.nombre}"
    

class Contacto(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.DO_NOTHING, null=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    cod_postal = models.CharField(max_length=4, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, validators=[validar_telefono])
    email = models.EmailField(max_length=250, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.profesional.apellido} " + f"{self.profesional.nombre}"