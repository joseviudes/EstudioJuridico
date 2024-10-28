from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value
from django.db.models.functions import Concat

from .forms import TurnoForm
from .models import Turno
from clientes.models import Cliente
from profesionales.models import Profesional
 


class ListTurno(LoginRequiredMixin, ListView):
    model = Turno
    template_name = 'turnos/turnos.html'
    context_object_name = 'turnos'  
    paginate_by = 10  
    
    def get_queryset(self):
        user = self.request.user

        if user.rol == 'Admin':
            # Si es Admin, mostramos todos los turnos
            queryset = Turno.objects.all()
        elif user.rol == 'Cliente':
            # Si es Cliente, mostramos solo los turnos en los que es cliente
            try:
                cliente = Cliente.objects.get(usuario=user)
                queryset = Turno.objects.filter(cliente=cliente)
            except Cliente.DoesNotExist:
                return Turno.objects.none()
        elif user.rol == 'Abogado':
            # Si es Profesional (Abogado), mostramos solo los turnos en los que es el profesional asignado
            try:
                profesional = Profesional.objects.get(usuario=user)
                queryset = Turno.objects.filter(profesional=profesional)
            except Profesional.DoesNotExist:
                return Turno.objects.none()
        else:
            # Si no tiene un rol válido, devolvemos un queryset vacío
            return Turno.objects.none()

        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.annotate(
                full_name_cliente=Concat('cliente__nombre', Value(' '), 'cliente__apellido'),
                full_name_profesional=Concat('profesional__nombre', Value(' '), 'profesional__apellido')
            ).filter(
                Q(full_name_cliente__icontains=query) | 
                Q(full_name_profesional__icontains=query) |  
                Q(dia__icontains=query) |
                Q(motivo__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context



    

@login_required  
def singleTurno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    
    context = {'turno': turno}
    return render(request, 'turnos/turno.html', context)

def createTurno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST, user=request.user) 
        if form.is_valid():
            turno = form.save(commit=False)

            # Verificar si el turno ya está reservado
            turno_existente = Turno.objects.filter(
                profesional=turno.profesional,
                dia=turno.dia,
                horario=turno.horario,
                estado='reservado'
            ).exists()

            if turno_existente:
                messages.error(request, "El turno ya está reservado. Por favor, elegí otro horario.")
                return render(request, 'turnos/create-turno.html', {'form': form})

            # Si el turno está libre, se guarda con el estado 'Pendiente de aprobación'
            turno.estado = 'Pendiente de aprobación'
            turno.save()
            return redirect('turnos')  # Si está autenticado, redirige a 'turnos'
        
    else:
        form = TurnoForm(user=request.user)  # Pasamos el usuario al formulario
    
    context = {'form': form}
    return render(request, 'turnos/create-turno.html', context)


@login_required
def updateTurno(request, pk):
    
    turno = get_object_or_404(Turno, pk=pk)

    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            messages.success(request, "El turno se ha modificado correctamente.")
            return redirect('turnos') 
        else:
            messages.error(request, "Hubo un error al actualizar el turno. Por favor verifique los datos.")
    else:
        
        form = TurnoForm(instance=turno)

    context = {'form': form, 'turno': turno}
    return render(request, 'turnos/update-turno.html', context)


def updateEstado(request, pk):
    
    if request.method == 'POST':
        turno = get_object_or_404(Turno, pk=pk)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in ['Pendiente', 'Aprobado', 'Cancelado', 'Concluido']:
            turno.estado = nuevo_estado
            turno.save()
            return redirect('turnos') 
        
    return HttpResponse(status=400)


@login_required
def deleteTurno(request, pk):
    
    turno = Turno.objects.get(pk=pk)
    
    if request.method == 'POST':
        turno.delete()
        return redirect('turnos')
    
    context = {'turno': turno}
    return render(request, 'turnos/delete-turno.html', context)



# ----------------------- agenda ------------------------

def agendaView(request):
    return render(request, 'turnos/agenda.html')

# @login_required
# def agendaView(request):
#     today = timezone.now().date()
#     turnos_futuros = Turno.objects.filter(dia__gt=today).order_by('dia', 'horario')
#     turnos_pasados = Turno.objects.filter(dia__lt=today).order_by('-dia', '-horario')
    
#     dia_seleccionado = request.GET.get('dia')
#     turnos_dia = []
    
#     if dia_seleccionado:
#         turnos_dia = Turno.objects.filter(dia=dia_seleccionado).order_by('horario')

#     return render(request, 'turnos/agenda.html', {
#         'turnos_futuros': turnos_futuros,
#         'turnos_pasados': turnos_pasados,
#         'turnos_dia': turnos_dia,
#     })


# def obtenerTurnos(request):
    
#     turnos = Turno.objects.all()
#     eventos = []
    
#     for turno in turnos:
#         eventos.append({
#             'title': turno.cliente.nombre,
#             'start': turno.dia.isoformat(),
#             'end': turno.horario.isoformat(),
#             # Puedes agregar más campos si es necesario
#         })
        
#     return JsonResponse(eventos, safe=False)


def turnos_json(request):
    turnos = Turno.objects.all()
    turnos_list = []

    for turno in turnos:
        start_time = turno.horario.split(' a ')[0]
        end_time = turno.horario.split(' a ')[1]
        turnos_list.append({
            'id': turno.id_turno,
            'title': "Turno para: ",  # Añadido título
            'cliente': str(turno.cliente),
            'solicitante': str(turno.solicitante),
            'motivo': str(turno.motivo),
            'start': f"{turno.dia}T{start_time}",  # Asegúrate de que `turno.dia` esté en el formato correcto
            'end': f"{turno.dia}T{end_time}",
            'estado': turno.estado,
            'professional': str(turno.profesional),
        })

    return JsonResponse(turnos_list, safe=False)


def horariosOcupados(request):
    
    dia = request.GET.get('dia')
    profesional_dni = request.GET.get('profesional_dni')
    
    if dia and profesional_dni:
        try:
            # Convertir el string a objeto de fecha
            dia = datetime.strptime(dia, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha incorrecto'}, status=400)
        
        # Filtrar los turnos para el día y profesional seleccionado
        turnos = Turno.objects.filter(dia=dia, profesional_dni=profesional_dni)
        horarios_ocupados = list(turnos.values_list('horario', flat=True))  
        
        return JsonResponse({'horarios_ocupados': horarios_ocupados})
    
    return JsonResponse({'error': 'Fecha o profesional no válido'}, status=400)
        
    