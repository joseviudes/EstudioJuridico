from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .forms import TurnoForm
from .models import Turno
from clientes.models import Cliente

# Create your views here.


class ListTurno(ListView):
    model = Turno
    template_name = 'turnos/turnos.html'
    context_object_name = 'turnos'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación

@login_required  
def singleTurno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)  # Obtiene el turno o devuelve 404 si no existe
    
    context = {'turno': turno}
    return render(request, 'turnos/turno.html', context)

@login_required  # Asegúrate de que el usuario esté autenticado
def createTurno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            # Asigna automáticamente el cliente basado en el usuario autenticado
            cliente = Cliente.objects.get(usuario=request.user)  # Asegúrate de que haya una relación entre Cliente y Usuario
            turno = form.save(commit=False)  # No guardes aún
            turno.cliente = cliente  # Asigna el cliente
            turno.save()  # Ahora guarda el turno
            return redirect('turnos')  # Redirige a la lista de turnos o a donde necesites
    else:
        form = TurnoForm()
        
    context = {'form': form}
    return render(request, 'turnos/create-turno.html', context)


@login_required
def deleteTurno(request, pk):
    
    turno = Turno.objects.get(id=pk)
    
    if request.method == 'POST':
        turno.delete()
        return redirect('turnos')
    
    context = {'object': turno}
    return render(request, 'delete-turno.html', context)
