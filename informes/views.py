from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count

from turnos.models import Turno
from profesionales.models import Profesional

    
class Informe(TemplateView):
    
    def get(self,request, *args, **kwargs):
        return render(request, 'informes/informes.html')
    
    
# def informeAbogado(request):
#     datos = abogado_mas_turnos_del_mes()  # Llamada sin pasar request
#     return render(request, 'informes/informe1.html', {'datos': datos})


def informeAbogado(request):
    # Obtener el mes actual
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Obtener el abogado con más turnos en el mes
    abogado_mas_turnos = (Turno.objects.filter(dia__month=mes_actual, dia__year=anio_actual)
                          .values('profesional')
                          .annotate(total_turnos=Count('id_turno'))
                          .order_by('-total_turnos')
                          .first())

    # Si hay un abogado con más turnos
    if abogado_mas_turnos:
        # Obtener el objeto Profesional con más turnos
        profesional = Profesional.objects.get(dni=abogado_mas_turnos['profesional'])
        abogado_mas_turnos['profesional'] = profesional  # Añadir el objeto Profesional al contexto
    else:
        profesional = None

    # Obtener el total de turnos para cada abogado en el mes actual
    turnos_por_abogado = (Turno.objects.filter(dia__month=mes_actual, dia__year=anio_actual)
                          .values('profesional__nombre', 'profesional__apellido')
                          .annotate(total_turnos=Count('id_turno'))
                          .order_by('-total_turnos'))

    context = {
        'abogado_mas_turnos': abogado_mas_turnos,
        'turnos_por_abogado': turnos_por_abogado,
    }

    return render(request, 'informes/informe1.html', context)


