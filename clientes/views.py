from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ClienteForm
from .models import Cliente


class ListCliente(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/clientes.html'
    context_object_name = 'clientes'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(dni__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Añade la consulta al contexto para mantenerla en el formulario
        return context

@login_required
def singleCliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)  # Obtiene el cliente o devuelve 404 si no existe
    
    context = {'cliente': cliente,}
    return render(request, 'clientes/cliente.html', context)

@login_required
def createCliente(request):
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha añadido un cliente correctamente.")
            return redirect('clientes')
        else:
            messages.error(request, "Hubo un error al crear el cliente. Por favor verifique los datos")
    else:
        form = ClienteForm()
        
    context = {'form': form}
    return render(request, 'clientes/create-cliente.html', context)

@login_required
def updateCliente(request, pk):
    # Obtenemos el cliente a actualizar o muestra un error 404 si no existe
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos del cliente se han actualizado correctamente.")
            return redirect('clientes')  # Redirige a la lista de clientes
        else:
            messages.error(request, "Hubo un error al actualizar el cliente. Por favor verifique los datos.")
    else:
        # Si es una solicitud GET, crea un formulario con los datos actuales del expediente
        form = ClienteForm(instance=cliente)
        
    
    context = {'form': form, 'cliente': cliente}
    return render(request, 'clientes/update-cliente.html', context)

@login_required
def deleteCliente(request, pk):
    
    cliente = Cliente.objects.get(pk=pk)
    
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    
    context = {'cliente': cliente}
    return render(request, 'clientes/delete-cliente.html', context)