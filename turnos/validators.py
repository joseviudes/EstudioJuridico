from datetime import date
from django.forms import ValidationError


def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('No se puede seleccionar una fecha pasada.')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('Seleccione un dia habil.') 
    
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