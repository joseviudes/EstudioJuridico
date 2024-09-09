from django.db import models
from django.forms import ValidationError

# Create your models here.

TIPO_DE_MATRICULA = (
    ("DNI", "DNI"),
    ("CUIL", "CUIL")
)

def validar_telefono(value):
    if len(value) != 10:
        raise ValidationError('El telefono debe tener 10 numeros.')
    if not value.isdigit():
        raise ValidationError('El telefono debe contener solo números.')

class Cliente(models.Model):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    tipo_matricula = models.CharField(max_length=200, choices=TIPO_DE_MATRICULA, default="DNI")
    num_matricula = models.IntegerField(primary_key=True, unique=True) #  PK y de valor unico
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=50)
    lugar_laboral = models.CharField(max_length=100)
    años_aportes = models.IntegerField(default=None)

    def __str__(self):
        return f"{self.apellido} " + f"{self.nombre}"
    
    
class Contacto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, null=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    cod_postal = models.CharField(max_length=4, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, validators=[validar_telefono])
    email = models.EmailField(max_length=250, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.cliente.apellido} " + f"{self.cliente.nombre}" + f"{self.telefono}"