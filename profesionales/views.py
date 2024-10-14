from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfesionalForm
from .models import Profesional


class ListProfesional(LoginRequiredMixin, ListView):
    model = Profesional
    template_name = 'profesionales/profesionales.html'
    context_object_name = 'profesionales'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación

@login_required
def detailProfesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    
    context = {'profesional': profesional,}
    return render(request, 'profesionales/profesional.html', context)

@login_required
def createProfesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado un profesional.")
            return redirect('profesionales')
        else:
            messages.error(request, "Hubo un error al crear el profesional. Por favor verifique los datos")
    else:
        form = ProfesionalForm()
        
    context = {'form': form}
    return render(request, 'profesionales/create-profesional.html', context)

@login_required
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

@login_required
def deleteProfesional(request, pk):
    
    profesional = Profesional.objects.get(pk=pk)
    
    if request.method == 'POST':
        profesional.delete()
        return redirect('profesionales')
    
    context = {'profesional': profesional}
    return render(request, 'profesionales/delete-profesional.html', context)
