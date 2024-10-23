from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required

from .models import Usuario
from .forms import UsuarioForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'Admin'


def loginUser(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Se ha iniciado sesión.")
            return redirect("index")
        else:
            messages.error(request, "Hubo un error al iniciar sesión, por favor verifique los datos.")
            return redirect("login")
    
    return render(request, 'usuarios/login.html', {})


def logoutUser(request):
    logout(request)
    messages.success(request, "Se ha cerrado sesión.")
    return redirect("index")


class ListUsuarios(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'  # nombre del objeto en el contexto 
    paginate_by = 10  #paginación
    
@login_required
def createUsuario(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Establecer contraseña
            user.save()
            messages.success(request, f'Usuario {user.email} creado exitosamente.')
            return redirect('usuarios')  
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/create-usuario.html', {'form': form})


@login_required
def updateUsuario(request, pk):
    
    user = get_object_or_404(Usuario, pk=pk) 

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {user.email} actualizado exitosamente.')
            return redirect('usuarios')  # Cambia por la URL de éxito
    else:
        form = UsuarioForm(instance=user)

    return render(request, 'usuarios/update-usuario.html', {'form': form, 'usuario': user})



@login_required
def deleteUsuario(request, pk):

    user = get_object_or_404(Usuario, pk=pk)  # Busca el usuario por su ID

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuario {user.email} eliminado exitosamente.')
        return redirect('index')  # Cambia por la URL de éxito

    return render(request, 'usuarios/delete-usuario.html', {'usuario': user})