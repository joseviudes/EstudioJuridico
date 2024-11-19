from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from .forms import ProfesionalForm, SecretariaForm
from .models import Profesional, Secretaria
from .filters import ProfesionalFilter, SecretariaFilter



def is_admin_or_abogado(user):
    return user.is_authenticated and (user.is_superuser or user.rol == 'Abogado' or user.rol == 'Secretaria')

class SoloAdminYAbogadoMixin(UserPassesTestMixin):
    def test_func(self):
        # Comprobamos si el usuario es admin o abogado
        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.rol == 'Abogado' or self.request.user.rol == 'Secretaria')


class ListProfesional(LoginRequiredMixin, SoloAdminYAbogadoMixin, ListView):
    
    model = Profesional
    template_name = 'profesionales/profesionales.html'
    context_object_name = 'profesionales'
    filterset_class = ProfesionalFilter
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



class ListProfesionalInactivo(LoginRequiredMixin, SoloAdminYAbogadoMixin, ListView):
    
    model = Profesional
    template_name = 'profesionales/profesionales-inactivos.html'
    context_object_name = 'profesionales'
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
        return context    

@login_required
@user_passes_test(is_admin_or_abogado)
def detailProfesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    
    context = {'profesional': profesional,}
    return render(request, 'profesionales/profesional.html', context)


@login_required
@user_passes_test(is_admin_or_abogado)
def createProfesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, request.FILES)
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
@user_passes_test(is_admin_or_abogado)
def updateProfesional(request, pk):
    # Obtenemos el profesional a actualizar o muestra un error 404 si no existe
    profesional = get_object_or_404(Profesional, pk=pk)

    if request.method == 'POST':
        form = ProfesionalForm(request.POST, request.FILES, instance=profesional)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos del profesional se han actualizado correctamente.")
            return redirect('profesionales')  # Redirige a la lista de profesionales
        else:
            print(form.errors)
            messages.error(request, "Hubo un error al actualizar el profesional. Por favor verifique los datos.")
    else:
        # Si es una solicitud GET crea un formulario con los datos actuales del profesional
        form = ProfesionalForm(instance=profesional)

    context = {'form': form, 'profesional': profesional}
    return render(request, 'profesionales/update-profesional.html', context)


@login_required
@user_passes_test(is_admin_or_abogado)
def deleteProfesional(request, pk):
    
    profesional = Profesional.objects.get(pk=pk)
    
    if request.method == 'POST':
        profesional.delete()
        return redirect('profesionales-inactivos')
    
    context = {'profesional': profesional}
    return render(request, 'profesionales/delete-profesional.html', context)


@login_required
@permission_required('profesionales.change_profesional', raise_exception=True)
@user_passes_test(is_admin_or_abogado)
def darDeBajaProfesional(request, dni):
    
    profesional = get_object_or_404(Profesional, pk=dni)
    
    if profesional.estado:
        profesional.estado = False
        profesional.save()
        messages.success(request, f"Profesional {profesional.full_name} fué dado de baja correctamente.")
    else:
        messages.info(request, f"Profesional {profesional.full_name} ya se encuentra dado baja.")
        
    return redirect('profesionales')


@login_required
@permission_required('profesionales.change_profesional', raise_exception=True)
@user_passes_test(is_admin_or_abogado)
def darDeAltaProfesional(request, dni):
    
    profesional = get_object_or_404(Profesional, pk=dni)
    
    if not profesional.estado:
        profesional.estado = True
        profesional.save()
        messages.success(request, f"Profesional {profesional.full_name} fué dado de alta exitosamente.")
    else:
        messages.info(request, f"Profesional {profesional.full_name} ya está activo.")
        
    return redirect('profesionales-inactivos')  


# ---------------------- Secretaria ---------------------

class ListSecretaria(LoginRequiredMixin, SoloAdminYAbogadoMixin, ListView):
    
    model = Secretaria
    template_name = 'profesionales/secretarias.html'
    context_object_name = 'secretarias'
    filterset_class = ProfesionalFilter
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
    
class ListSecretariaInactivo(LoginRequiredMixin, SoloAdminYAbogadoMixin, ListView):
    
    model = Secretaria
    template_name = 'profesionales/secretarias-inactivos.html'
    context_object_name = 'secretarias'
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
        return context 

@login_required
@user_passes_test(is_admin_or_abogado)
def detailSecretaria(request, pk):
    secretaria = get_object_or_404(Secretaria, pk=pk)
    
    context = {'secretaria': secretaria,}
    return render(request, 'profesionales/secretaria.html', context)

@login_required
@user_passes_test(is_admin_or_abogado)
def createSecretaria(request):
    if request.method == 'POST':
        form = SecretariaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado una secretaria.")
            return redirect('profesionales')
        else:
            messages.error(request, "Hubo un error al crear una nueva secretaria. Por favor verifique los datos")
    else:
        form = SecretariaForm()
        
    context = {'form': form}
    return render(request, 'profesionales/create-secretaria.html', context)


@login_required
@user_passes_test(is_admin_or_abogado)
def updateSecretaria(request, pk):
    secretaria = get_object_or_404(Secretaria, pk=pk)

    if request.method == 'POST':
        form = SecretariaForm(request.POST, instance=secretaria)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos de la secretaria se han actualizado correctamente.")
            return redirect('secretarias') 
        else:
            # Mostrar errores específicos del formulario
            messages.error(request, "Hubo un error al actualizar los datos de la secretaria. Por favor verifique los datos.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")

    else:
        form = SecretariaForm(instance=secretaria)  # Corrigiendo aquí para que coincida con el formulario

    context = {'form': form, 'secretaria': secretaria}
    return render(request, 'profesionales/update-secretaria.html', context)

@login_required
@permission_required('profesionales.change_secretaria', raise_exception=True)
@user_passes_test(is_admin_or_abogado)
def darDeBajaSecretaria(request, dni):
    
    secretaria = get_object_or_404(Secretaria, pk=dni)
    
    if secretaria.estado:
        secretaria.estado = False
        secretaria.save()
        messages.success(request, f"Secretari@ {secretaria.full_name} fué dad@ de baja correctamente.")
    else:
        messages.info(request, f"Secretari@ {secretaria.full_name} ya se encuentra dad@ baja.")
        
    return redirect('secretarias')


@login_required
@permission_required('profesionales.change_secretaria', raise_exception=True)
@user_passes_test(is_admin_or_abogado)
def darDeAltaSecretaria(request, dni):
    
    secretaria = get_object_or_404(Secretaria, pk=dni)
    
    if not secretaria.estado:
        secretaria.estado = True
        secretaria.save()
        messages.success(request, f"Secretari@ {secretaria.full_name} fué dad@ de alta exitosamente.")
    else:
        messages.info(request, f"Secretari@ {secretaria.full_name} ya está activ@.")
        
    return redirect('secretarias-inactivos')  