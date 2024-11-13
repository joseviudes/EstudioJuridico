from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Max
import calendar
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.timezone import now

from turnos.models import Turno
from profesionales.models import Profesional

    
class Informe(TemplateView):
    
    def get(self,request, *args, **kwargs):
        return render(request, 'informes/informes.html')
    
    
# def informeAbogado(request):
#     datos = abogado_mas_turnos_del_mes()  # Llamada sin pasar request
#     return render(request, 'informes/informe1.html', {'datos': datos})



def informeAbogado(request):
    # Obtener mes y año de los parámetros GET, o usar el mes y año actual como predeterminado
    hoy = timezone.now()
    mes_actual = int(request.GET.get('mes', hoy.month))
    anio_actual = int(request.GET.get('anio', hoy.year))

    # Obtener los turnos del mes y año seleccionados, incluyendo los objetos 'profesional' completos
    turnos_por_abogado = (Turno.objects.filter(dia__month=mes_actual, dia__year=anio_actual)
                          .select_related('profesional')  # Incluye el objeto 'profesional' completo
                          .values('profesional', 'profesional__nombre', 'profesional__apellido', 'profesional__foto')
                          .annotate(total_turnos=Count('id_turno'))
                          .order_by('-total_turnos'))

    # Encontrar la cantidad máxima de turnos
    max_turnos = turnos_por_abogado.aggregate(Max('total_turnos'))['total_turnos__max']
    abogados_con_mas_turnos = [abogado for abogado in turnos_por_abogado if abogado['total_turnos'] == max_turnos]

    # Generar lista de meses y años para el selector del formulario
    meses = [(i, calendar.month_name[i]) for i in range(1, 13)]
    anios = range(hoy.year - 5, hoy.year + 1)  # Últimos 5 años hasta el actual

    context = {
        'abogados_con_mas_turnos': abogados_con_mas_turnos,
        'turnos_por_abogado': turnos_por_abogado,
        'meses': meses,
        'anios': anios,
        'mes_actual': mes_actual,
        'anio_actual': anio_actual,
    }

    return render(request, 'informes/informe1.html', context)



def generarInformePdf(request):
    # Obtener los datos necesarios (usa los mismos datos de tu informe actual)
    hoy = now()
    mes_actual = int(request.GET.get('mes', hoy.month))
    anio_actual = int(request.GET.get('anio', hoy.year))

    turnos_por_abogado = (Turno.objects.filter(dia__month=mes_actual, dia__year=anio_actual)
                          .select_related('profesional')
                          .values('profesional__nombre', 'profesional__apellido')
                          .annotate(total_turnos=Count('id_turno'))
                          .order_by('-total_turnos'))


    context = {
        'turnos_por_abogado': turnos_por_abogado,
        'mes_actual': mes_actual,
        'anio_actual': anio_actual,
    }

    # Renderizar el template del PDF
    template = get_template('informes/informe-pdf.html')
    html = template.render(context)

    # Generar el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{mes_actual}_{anio_actual}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

