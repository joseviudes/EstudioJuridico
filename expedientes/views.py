from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ExpedienteForm, MovimientosForm, DocumentoFormSet
from .models import Expediente, Movimientos, Documentos
from .filters import ExpedienteFilter


def is_admin_or_abogado(user):
    return user.is_authenticated and (user.is_superuser or user.rol == 'Abogado')

class SoloAdminYAbogadoMixin(UserPassesTestMixin):
    def test_func(self):

        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.rol == 'Abogado')


class ListExpediente(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expedientes/expedientes.html'
    context_object_name = 'expedientes'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(estado=True) 
        query = self.request.GET.get('q')
        order = self.request.GET.get('order')

        if query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=query) |
                Q(cliente__apellido__icontains=query) |
                Q(profesional__nombre__icontains=query) |
                Q(profesional__apellido__icontains=query) |
                Q(numero_expediente__icontains=query)
            )
            
        # filtros
        if order == 'apellido_asc':
            queryset = queryset.order_by('cliente__apellido')
        elif order == 'apellido_desc':
            queryset = queryset.order_by('-cliente__apellido')
        elif order == 'fecha_inicio_asc':
            queryset = queryset.order_by('fecha_inicio')
        elif order == 'fecha_inicio_desc':
            queryset = queryset.order_by('-fecha_inicio')
        elif order == 'apellido_pro_asc':  
            queryset = queryset.order_by('profesional__apellido')
        elif order == 'apellido_pro_desc':  
            queryset = queryset.order_by('-profesional__apellido')

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  
        context['order'] = self.request.GET.get('order', '')
        return context


class ListExpedienteInactivo(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expedientes/expedientes-inactivos.html'
    context_object_name = 'expedientes' 
    paginate_by = 10  
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(estado=False) 
        query = self.request.GET.get('q')
        order = self.request.GET.get('order')

        if query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=query) |
                Q(cliente__apellido__icontains=query) |
                Q(profesional__nombre__icontains=query) |
                Q(profesional__apellido__icontains=query) |
                Q(numero_expediente__icontains=query)
            )
            
        # filtros
        if order == 'apellido_asc':
            queryset = queryset.order_by('cliente__apellido')
        elif order == 'apellido_desc':
            queryset = queryset.order_by('-cliente__apellido')
        elif order == 'fecha_inicio_asc':
            queryset = queryset.order_by('fecha_inicio')
        elif order == 'fecha_inicio_desc':
            queryset = queryset.order_by('-fecha_inicio')
        elif order == 'apellido_pro_asc':  
            queryset = queryset.order_by('profesional__apellido')
        elif order == 'apellido_pro_desc':  
            queryset = queryset.order_by('-profesional__apellido')  

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  
        context['order'] = self.request.GET.get('order', '')
        return context


@login_required
def singleExpediente(request, numero_expediente):
    expediente = get_object_or_404(Expediente, numero_expediente=numero_expediente)  # Obtiene el expediente o devuelve 404 si no existe
    
    context = {'expediente': expediente,}
    return render(request, 'expedientes/expediente.html', context)

@login_required
@user_passes_test(is_admin_or_abogado)
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

@login_required
@user_passes_test(is_admin_or_abogado)
def updateExpediente(request, numero_expediente):
    # Obtenemos el expediente a actualizar o muestra un error 404 si no existe
    expediente = get_object_or_404(Expediente, numero_expediente=numero_expediente)

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

@login_required
@user_passes_test(is_admin_or_abogado)
def deleteExpediente(request, numero_expediente):
    
    expediente = Expediente.objects.get(numero_expediente=numero_expediente)
    
    if request.method == 'POST':
        expediente.delete()
        return redirect('expedientes')
    
    context = {'expediente': expediente}
    return render(request, 'expedientes/delete-expediente.html', context)


@login_required
@permission_required('expedientes.change_expediente', raise_exception=True)
@user_passes_test(is_admin_or_abogado)
def darDeBajaExpediente(request, numero_expediente):
    
    expediente = get_object_or_404(Expediente, pk=numero_expediente)
    
    if expediente.estado:
        expediente.estado = False
        expediente.save()
        messages.success(request, f"Expediente Nº{expediente.numero_expediente} fué dado de baja correctamente.")
    else:
        messages.info(request, f"Expediente Nº{expediente.numero_expediente} ya se encuentra dado baja.")
        
    return redirect('expedientes-inactivos')

@login_required
@permission_required('expedientes.change_expediente', raise_exception=True)
@user_passes_test(is_admin_or_abogado)
def darDeAltaExpediente(request, numero_expediente):
    
    expediente = get_object_or_404(Expediente, pk=numero_expediente)
    
    if not expediente.estado:
        expediente.estado = True
        expediente.save()
        messages.success(request, f"Expediente Nº{expediente.numero_expediente} fué dado de alta exitosamente.")
    else:
        messages.info(request, f"Expediente Nº{expediente.numero_expediente} ya está activo.")
        
    return redirect('expedientes')  
    
    
# ----------------- Movimientos -------------------


@login_required
def ListMovimientos(request, numero_expediente):
    expediente = get_object_or_404(Expediente, numero_expediente=numero_expediente)  # Filtra el expediente por su número
    movimientos = Movimientos.objects.filter(expediente=expediente)  # Filtra los movimientos del expediente
    
    context = {
        'expediente': expediente,
        'movimientos': movimientos,
    }
    
    return render(request, 'expedientes/movimientos.html', context)


@login_required
@user_passes_test(is_admin_or_abogado)
def createMovimiento(request, numero_expediente):
    expediente = get_object_or_404(Expediente, numero_expediente=numero_expediente)
    
    if request.method == 'POST':
        form = MovimientosForm(request.POST)
        documento_formset = DocumentoFormSet(request.POST, request.FILES)
        
        if form.is_valid() and documento_formset.is_valid():
            movimiento = form.save(commit=False)
            movimiento.expediente = expediente  
            movimiento.save()

            for documento_form in documento_formset:
                if documento_form.cleaned_data.get('archivo'):  # Verificar si hay archivo en el formset
                    documento = documento_form.save(commit=False)
                    documento.movimiento = movimiento  
                    documento.save()

            return redirect('movimientos', numero_expediente=numero_expediente) 

    else:
        form = MovimientosForm()
        documento_formset = DocumentoFormSet(queryset=Documentos.objects.none()) 

    context = {
        'form': form,
        'documento_formset': documento_formset,
        'expediente': expediente
    }
    
    return render(request, 'expedientes/create-movimiento.html', context)


    
@login_required
@user_passes_test(is_admin_or_abogado)
def updateMovimiento(request, id_mov):
    movimiento = get_object_or_404(Movimientos, id_mov=id_mov)
    expediente = movimiento.expediente

    if request.method == 'POST':
        form = MovimientosForm(request.POST, request.FILES, instance=movimiento)
        documento_formset = DocumentoFormSet(request.POST, request.FILES, instance=movimiento)

        if form.is_valid() and documento_formset.is_valid():
            form.save()

            # Guardar los documentos asociados
            for documento_form in documento_formset:
                if documento_form.cleaned_data.get('archivo'):
                    documento = documento_form.save(commit=False)
                    documento.movimiento = movimiento
                    documento.save()

            for documento_form in documento_formset.deleted_forms:
                documento_form.instance.delete()

            messages.success(request, "Los datos del movimiento del expediente se han actualizado correctamente.")
            return redirect('movimientos', numero_expediente=expediente.numero_expediente)
        else:
            messages.error(request, "Hubo un error al actualizar el movimiento del expediente. Por favor verifique los datos.")
    else:
        form = MovimientosForm(instance=movimiento)
        documento_formset = DocumentoFormSet(instance=movimiento) 

    context = {
        'form': form,
        'documento_formset': documento_formset,
        'movimiento': movimiento,
        'expediente': expediente,
    }
    
    return render(request, 'expedientes/update-movimiento.html', context)



@login_required
@user_passes_test(is_admin_or_abogado)
def deleteMovimiento(request, id_mov):

    movimiento = get_object_or_404(Movimientos, id_mov=id_mov)

    if request.method == 'POST':
        numero_expediente = movimiento.expediente.numero_expediente  
        movimiento.delete()
        messages.success(request, "El movimiento del expediente se ha eliminado correctamente.")
        return redirect('movimientos', numero_expediente=numero_expediente)

    context = {'movimiento': movimiento}
    return render(request, 'expedientes/delete-movimiento.html', context)
    