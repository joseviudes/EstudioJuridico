from django.forms import ValidationError

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