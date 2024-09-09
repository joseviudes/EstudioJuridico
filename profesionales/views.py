from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView

from .forms import ProfesionalForm
from .models import Profesional


class ListProfesional(ListView):
    model = Profesional
    template_name = 'profesionales/profesionales.html'
    context_object_name = 'profesionales'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación
    
    
def singleProfesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)  # Obtiene el profesional o devuelve 404 si no existe
    
    context = {'profesional': profesional,}
    return render(request, 'profesionales/profesional.html', context)


def createProfesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success("Se ha agregado un profesional.")
            return redirect('profesionales')
        else:
            messages.error("Hubo un error al crear el profesional. Por favor verifique los datos")
    else:
        form = ProfesionalForm()
        
    context = {'form': form}
    return render(request, 'profesionales/create-profesional.html', context)


def updateProfesional(request, pk):
    # Obtenemos el profesional a actualizar o muestra un error 404 si no existe
    profesional = get_object_or_404(Profesional, pk=pk)

    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos del profesional se han actualizado correctamente.")
            return redirect('profesionales')  # Redirige a la lista de profesionales
        else:
            messages.error(request, "Hubo un error al actualizar el profesional. Por favor verifique los datos.")
    else:
        # Si es una solicitud GET crea un formulario con los datos actuales del profesional
        form = ProfesionalForm(instance=profesional)

    context = {'form': form, 'profesional': profesional}
    return render(request, 'profesionales/update-profesional.html', context)


def deleteProfesional(request, pk):
    
    profesional = Profesional.objects.get(id=pk)
    
    if request.method == 'POST':
        profesional.delete()
        return redirect('profesionales')
    
    context = {'object': profesional}
    return render(request, 'profesionales/delete-profesional.html', context)


