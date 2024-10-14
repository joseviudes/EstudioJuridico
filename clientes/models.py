from django.db import models
from django.forms import ValidationError

from usuarios.models import Usuario

# Create your models here.

# TIPO_DE_MATRICULA = (
#     ("DNI", "DNI"),
#     ("CUIL", "CUIL")
# )

def validar_telefono(value):
    if len(value) != 10:
        raise ValidationError('El telefono debe tener 10 digitos.')
    if not value.isdigit():
        raise ValidationError('El telefono debe contener solo números.')
    
def validar_dni(value):
    if len(value) < 7 and len(value) > 8:
        raise ValidationError('El DNI debe tener como minimo 7 digitos y como maximo 8.')
    if not value.isdigit():
        raise ValidationError('El DNI debe contener solo números.')
    
def validar_codPostal(value):
    if len(value) != 4:
        raise ValidationError('El código postal debe tener 4 digitos.')
    if not value.isdigit():
        raise ValidationError('El código postal debe contener solo digitos.')


class Cliente(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True)
    
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    dni = models.CharField('DNI', max_length=8, primary_key=True, unique=True, validators=[validar_dni])  # PK y de valor único
    fecha_nacimiento = models.DateField('Fecha de nacimiento', blank=True, null=True)
    nacionalidad = models.CharField('Nacionalidad', max_length=50)
    ocupacion = models.CharField('Ocupación', max_length=50, blank=True, null=True)
    lugar_laboral = models.CharField('Lugar laboral', max_length=100, blank=True, null=True)
    años_aportes = models.IntegerField('Años de aportes', default=None, blank=True, null=True)
    
    # contacto
    direccion = models.CharField(max_length=250, null=True, blank=True)
    cod_postal = models.CharField('Codigo postal', max_length=4, null=True, blank=True, validators=[validar_codPostal])
    telefono = models.CharField(max_length=10, null=True, validators=[validar_telefono])
    email = models.EmailField(max_length=250, null=True, blank=True)

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.get_full_name()
    
    
