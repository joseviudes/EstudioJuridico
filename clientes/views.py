from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView

from .forms import ClienteForm
from .models import Cliente


class ListCliente(ListView):
    model = Cliente
    template_name = 'clientes/clientes.html'
    context_object_name = 'clientes'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación
    
def singleCliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)  # Obtiene el cliente o devuelve 404 si no existe
    
    context = {'cliente': cliente,}
    return render(request, 'clientes/cliente.html', context)

def createCliente(request):
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success("Se ha creado un cliente.")
            return redirect('clientes')
        else:
            messages.error("Hubo un error al crear el cliente. Por favor verifique los datos")
    else:
        form = ClienteForm()
        
    context = {'form': form}
    return render(request, 'clientes/create-cliente.html', context)


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


def deleteCliente(request, pk):
    
    cliente = Cliente.objects.get(id=pk)
    
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    
    context = {'object': cliente}
    return render(request, 'clientes/delete-cliente.html', context)


lista_de_clientes  = ListCliente.as_view()
cliente            = singleCliente
crear_cliente      = createCliente
actualizar_cliente = updateCliente
eliminar_cliente   = deleteCliente