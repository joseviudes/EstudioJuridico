from django.db import models
from PIL import Image

from .validators import *

ESPECIALIDADES = (
     ("Derecho de familia", "Derecho de familia"),
     ("Derecho penal", "Derecho penal"),
     ("Derecho laboral","Derecho laboral"),
     ("Derecho de daños","Derecho de daños"),
     ("Derecho sucesorio","Derecho sucesorio"),
     ("Derecho de daños","Derecho de daños"),
     ("Derecho de daños","Derecho de daños"),
     ("Derecho deportivo", "Derecho deportivo"),
 )

ESTADOS = (
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo')
)


class Profesional(models.Model):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    dni = models.CharField('DNI', max_length=8, primary_key=True, unique=True, validators=[validar_dni])  # PK y de valor único
    idMatriculaProf = models.CharField('Nº de matricula del profesional', max_length=50, unique=True)
    foto = models.ImageField('Foto', upload_to='images/', null=True, blank=True)
    
    especialidad = models.CharField(max_length=200, choices=ESPECIALIDADES, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_ingreso = models.DateField('Fecha de ingreso')  
    fecha_egreso = models.DateField('Fecha de egreso', null=True, blank=True)
    motivo_egreso = models.TextField('Motivo de egreso', max_length=250, null=True, blank=True)
    
    # Contacto
    domicilio = models.CharField(max_length=250, null=True, blank=True)
    cod_postal = models.CharField('Codigo Postal', max_length=4, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, validators=[validar_telefono])
    email = models.EmailField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Profesionales'

    # Propiedad full_name que combina el nombre y el apellido
    @property
    def full_name(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.full_name  


class Secretaria(models.Model):
    
    profesional = models.ForeignKey(Profesional, related_name='secretarias', on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField('DNI', max_length=8, primary_key=True, unique=True, validators=[validar_dni])
    foto = models.ImageField('Foto', upload_to='images/', null=True, blank=True)
    
    estado = models.BooleanField(default=True)
    fecha_ingreso = models.DateField('Fecha de ingreso')  
    fecha_egreso = models.DateField('Fecha de egreso', null=True, blank=True)
    motivo_egreso = models.TextField('Motivo de egreso', max_length=250, null=True, blank=True)
    
    # Contacto
    domicilio = models.CharField(max_length=250, null=True, blank=True)
    cod_postal = models.CharField('Codigo Postal', max_length=4, null=True, blank=True)
    telefono = models.CharField(max_length=10, validators=[validar_telefono])
    email = models.EmailField(max_length=250, null=True, blank=True)


    @property
    def full_name(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.full_name 