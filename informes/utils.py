from django.db.models import Count
from django.utils import timezone
from django.db.models import Count, F, Value
from django.db.models.functions import Concat

from turnos.models import Turno


def abogado_mas_turnos_del_mes():
    
    mes_actual = timezone.now().month
    
    return (
        Turno.objects.filter(dia__month=mes_actual)
        .annotate(profesional_nombre_completo=Concat(F('profesional__nombre'), Value(' '), F('profesional__apellido')))
        .values('profesional_nombre_completo')
        .annotate(total_turnos=Count('id_turno'))
        .order_by('-total_turnos')
        .first()
    )