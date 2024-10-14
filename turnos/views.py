from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .forms import TurnoForm
from .models import Turno
from clientes.models import Cliente
from profesionales.models import Profesional

# Create your views here.


from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.views.generic import ListView
from .models import Turno, Cliente, Profesional  # Asegúrate de importar tus modelos

class ListTurno(LoginRequiredMixin, ListView):
    model = Turno
    template_name = 'turnos/turnos.html'
    context_object_name = 'turnos'  
    paginate_by = 10  
    
    def get_queryset(self):
        user = self.request.user
        queryset = None
        
        if user.rol == 'admin':
            # Administradores ven todos los turnos
            queryset = Turno.objects.all()
        elif user.rol == 'cliente':
            try:
                # Obtener la instancia del cliente relacionado con el usuario
                cliente = Cliente.objects.get(usuario=user)
                # Filtrar turnos por cliente
                queryset = Turno.objects.filter(cliente=cliente)
            except Cliente.DoesNotExist:
                # Si no hay cliente asociado, retorna un queryset vacío
                return Turno.objects.none()
        elif user.rol == 'abogado':
            try:
                # Obtener la instancia del profesional relacionado con el usuario
                profesional = Profesional.objects.get(usuario=user)
                queryset = Turno.objects.filter(profesional=profesional)
            except Profesional.DoesNotExist:
                return Turno.objects.none()
        else:
            # Otros roles no tienen acceso a turnos
            return Turno.objects.none()
        
        # Filtrar por la consulta de búsqueda
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.annotate(
                full_name_cliente=Concat('cliente__nombre', Value(' '), 'cliente__apellido'),
                full_name_profesional=Concat('profesional__nombre', Value(' '), 'profesional__apellido')
            ).filter(
                Q(full_name_cliente__icontains=query) |  # Filtrar por nombre completo del cliente
                Q(full_name_profesional__icontains=query) |  # Filtrar por nombre completo del profesional
                Q(dia__icontains=query) |
                Q(motivo__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Añade la consulta al contexto para mantenerla en el formulario
        return context

    

@login_required  
def singleTurno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)  # Obtiene el turno o devuelve 404 si no existe
    
    context = {'turno': turno}
    return render(request, 'turnos/turno.html', context)

@login_required
def createTurno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            # Intenta obtener el cliente asociado al usuario
            try:
                cliente = Cliente.objects.get(usuario=request.user)  
            except Cliente.DoesNotExist:
                messages.error(request, "No se ha encontrado un cliente asociado con el usuario.")
                return redirect('crear-turno')  # Redirige o maneja el error

            # Si el cliente es encontrado, crea el turno
            turno = form.save(commit=False)  
            turno.cliente = cliente  
            turno.save()  
            return redirect('turnos')  # Redirige a la lista de turnos
    else:
        form = TurnoForm()

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
            messages.error(request, "Hubo un error al actualizar el profesional. Por favor verifique los datos.")
    else:
        
        form = TurnoForm(instance=turno)

    context = {'form': form, 'turno': turno}
    return render(request, 'turnos/update-turno.html', context)


@login_required
def deleteTurno(request, pk):
    
    turno = Turno.objects.get(pk=pk)
    
    if request.method == 'POST':
        turno.delete()
        return redirect('turnos')
    
    context = {'turno': turno}
    return render(request, 'turnos/delete-turno.html', context)

@login_required
def agendaView(request):
    today = timezone.now().date()
    turnos_futuros = Turno.objects.filter(dia__gt=today).order_by('dia', 'horario')
    turnos_pasados = Turno.objects.filter(dia__lt=today).order_by('-dia', '-horario')
    
    dia_seleccionado = request.GET.get('dia')
    turnos_dia = []
    
    if dia_seleccionado:
        turnos_dia = Turno.objects.filter(dia=dia_seleccionado).order_by('horario')

    return render(request, 'turnos/agenda.html', {
        'turnos_futuros': turnos_futuros,
        'turnos_pasados': turnos_pasados,
        'turnos_dia': turnos_dia,
    })


def get_turnos(request):
    turnos = Turno.objects.all().values('id_turno', 'cliente__nombre', 'dia', 'horario')
    
    eventos = [{
        'title': str(turno.cliente),
        'start': turno.dia.isoformat(),  # Formato ISO para FullCalendar
    } for turno in turnos]
    return JsonResponse(eventos, safe=False)