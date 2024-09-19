from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import TurnoForm
from .models import Turno

# Create your views here.


class ListTurno(ListView):
    model = Turno
    template_name = 'turnos/turnos.html'
    context_object_name = 'turnos'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación

    
def singleTurno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)  # Obtiene el turno o devuelve 404 si no existe
    
    context = {'turno': turno}
    return render(request, 'turnos/turno.html', context)
    
    
def createTurno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success("Se ha agendado el turno!.")
            return redirect('turnos')
        else:
            messages.error("Hubo un error al agendar el turno. Por favor verifique los datos")
    else:
        form = TurnoForm()
        
    context = {'form': form}
    return render(request, 'turnos/create-turno.html', context)


def deleteTurno(request, pk):
    
    turno = Turno.objects.get(id=pk)
    
    if request.method == 'POST':
        turno.delete()
        return redirect('turnos')
    
    context = {'object': turno}
    return render(request, 'delete-turno.html', context)



lista_de_turnos  = ListTurno.as_view()
turno           = singleTurno
crear_turno     = createTurno
#actualizar_turno = updateTurno
eliminar_turno   = deleteTurno