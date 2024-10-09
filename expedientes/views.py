from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q

from .forms import ExpedienteForm
from .models import Expediente



class ListExpediente(ListView):
    model = Expediente
    template_name = 'expedientes/expedientes.html'
    context_object_name = 'expedientes'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=query) |
                Q(cliente__apellido__icontains=query) |
                Q(profesional__nombre__icontains=query) |
                Q(profesional__apellido__icontains=query) |
                Q(numero_expediente__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Añade la consulta al contexto para mantenerla en el formulario
        return context


def singleExpediente(request, pk):
    expediente = get_object_or_404(Expediente, pk=pk)  # Obtiene el expediente o devuelve 404 si no existe
    
    context = {'expediente': expediente,}
    return render(request, 'expedientes/expediente.html', context)


def createExpediente(request):
    if request.method == 'POST':
        form = ExpedienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha creado un expediente.")
            return redirect('expedientes')
        else:
            messages.error(request, "Hubo un error al crear el expediente. Por favor verifique los datos")
    else:
        form = ExpedienteForm()
        
    context = {'form': form}
    return render(request, 'expedientes/create-expediente.html', context)


def updateExpediente(request, pk):
    # Obtenemos el expediente a actualizar o muestra un error 404 si no existe
    expediente = get_object_or_404(Expediente, pk=pk)

    if request.method == 'POST':
        form = ExpedienteForm(request.POST, instance=expediente)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos del expediente se han actualizado correctamente.")
            return redirect('expedientes')  # Redirige a la lista de expedientes
        else:
            messages.error(request, "Hubo un error al actualizar el expediente. Por favor verifique los datos.")
    else:
        # Si es una solicitud GET, crea un formulario con los datos actuales del expediente
        form = ExpedienteForm(instance=expediente)
        
    
    context = {'form': form, 'expediente': expediente}
    return render(request, 'expedientes/update-expediente.html', context)


def deleteExpediente(request, pk):
    
    expediente = Expediente.objects.get(pk=pk)
    
    if request.method == 'POST':
        expediente.delete()
        return redirect('expedientes')
    
    context = {'expediente': expediente}
    return render(request, 'expedientes/delete-expediente.html', context)
    

