from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ClienteForm
from .models import Cliente


def is_admin_or_abogado(user):
    return user.is_authenticated and (user.is_superuser or user.rol == 'Abogado' or user.rol == 'Secretaria')

class SoloAdminYAbogadoMixin(UserPassesTestMixin):
    def test_func(self):
        # Comprobamos si el usuario es admin o abogado
        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.rol == 'Abogado' or self.request.user.rol == 'Secretaria')


class ListCliente(LoginRequiredMixin, SoloAdminYAbogadoMixin, ListView):
    
    model = Cliente
    template_name = 'clientes/clientes.html'
    context_object_name = 'clientes' 
    paginate_by = 10  
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(estado=True)
        query = self.request.GET.get('q')
        order = self.request.GET.get('order')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(dni__icontains=query)
            )
            
        # filtros
        if order == 'apellido_asc':
            queryset = queryset.order_by('apellido')
        elif order == 'apellido_desc':
            queryset = queryset.order_by('-apellido')
        elif order == 'fecha_ingreso_asc':
            queryset = queryset.order_by('fecha_ingreso')
        elif order == 'fecha_ingreso_desc':
            queryset = queryset.order_by('-fecha_ingreso')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['order'] = self.request.GET.get('order', '')
        return context
    
    
class ListClienteInactivo(LoginRequiredMixin, SoloAdminYAbogadoMixin, ListView):
    
    model = Cliente
    template_name = 'clientes/clientes-inactivos.html'
    context_object_name = 'clientes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(estado=False) 
        query = self.request.GET.get('q')
        order = self.request.GET.get('order')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(dni__icontains=query)
            )
            
        # filtros
        if order == 'apellido_asc':
            queryset = queryset.order_by('apellido')
        elif order == 'apellido_desc':
            queryset = queryset.order_by('-apellido')
        elif order == 'fecha_ingreso_asc':
            queryset = queryset.order_by('fecha_ingreso')
        elif order == 'fecha_ingreso_desc':
            queryset = queryset.order_by('-fecha_ingreso')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  
        context['order'] = self.request.GET.get('order', '')
        return context    


@login_required
@user_passes_test(is_admin_or_abogado)
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
@user_passes_test(is_admin_or_abogado)
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
@user_passes_test(is_admin_or_abogado)
def deleteCliente(request, pk):
    
    cliente = Cliente.objects.get(pk=pk)
    
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    
    context = {'cliente': cliente}
    return render(request, 'clientes/delete-cliente.html', context)

@user_passes_test(is_admin_or_abogado)
@login_required
def darDeBajaCliente(request, dni):
    
    cliente = get_object_or_404(Cliente, pk=dni)
    
    if cliente.estado:
        cliente.estado = False
        cliente.save()
        messages.success(request, f"Cliente {cliente.full_name} fué dado de baja correctamente.")
    else:
        messages.info(request, f"Cliente {cliente.full_name} ya se encuentra dado baja.")
        
    return redirect('clientes')

@user_passes_test(is_admin_or_abogado)
@login_required
def darDeAltaCliente(request, dni):
    
    cliente = get_object_or_404(Cliente, pk=dni)
    
    if not cliente.estado:
        cliente.estado = True
        cliente.save()
        messages.success(request, f"Cliente {cliente.full_name} fué dado de alta exitosamente.")
    else:
        messages.info(request, f"Cliente {cliente.full_name} ya está activo.")
        
    return redirect('clientes-inactivos')  