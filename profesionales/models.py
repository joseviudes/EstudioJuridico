from django.db import models
from django.forms import ValidationError

# Create your models here.

# TIPO_DE_MATRICULA = (
#     ("DNI", "DNI"),
#     ("CUIL", "CUIL")
# )

ESPECIALIDADES = (
    ("Familia", "Familia"),
    ("Laboral", "Laboral")
)

def validar_telefono(value):
    if len(value) != 10:
        raise ValidationError('El telefono debe tener 10 numeros.')
    if not value.isdigit():
        raise ValidationError('El telefono debe contener solo números.')
    
def validar_dni(value):
    if len(value) < 7 and len(value) > 8:
        raise ValidationError('El DNI debe tener como minimo 7 numeros y como maximo 8.')
    if not value.isdigit():
        raise ValidationError('El DNI debe contener solo números.')


class Profesional(models.Model):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    dni = models.CharField('Dni', max_length=8, primary_key=True, unique=True, validators=[validar_dni]) #  PK y de valor unico
    idMatriculaProf = models.IntegerField('Numero de matricula del profesional',unique=True)
    especialidad = models.CharField(max_length=200, choices=ESPECIALIDADES)
    fecha_ingreso = models.DateField('Fecha de ingreso')  
    fecha_egreso = models.DateField('Fecha de egreso',null=True, blank=True)  # es opcional
    motivo_egreso = models.TextField('Motivo de egreso', max_length=250, null=True, blank=True)
    
    # Contacto
    direccion = models.CharField(max_length=250, null=True, blank=True)
    cod_postal = models.CharField(max_length=4, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, validators=[validar_telefono], help_text="ej: 3794541234")
    email = models.EmailField(max_length=250, null=True, blank=True)
    
    class Meta:  
        verbose_name_plural = 'Profesionales'  # Nombre en plural
    
    def __str__(self):
        return f"{self.apellido} " + f"{self.nombre}"
