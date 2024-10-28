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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Log para verificar los valores de entrada
        print(f"Intento de login con: username={username}, password={'*' * len(password)}")
        
        # Autenticación de usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"Usuario autenticado: {user.username}")
            
            # Verificación para usuarios Admin
            if user.is_superuser or (not hasattr(user, 'profesional') and not hasattr(user, 'cliente')):
                print("Usuario es Admin o no tiene rol vinculado; omitiendo verificaciones adicionales.")
                login(request, user)
                messages.success(request, "Se ha iniciado sesión.")
                return redirect("index")

            # Verificación de usuarios con rol profesional
            if hasattr(user, 'profesional'):
                profesional = user.profesional
                print(f"Verificando profesional asociado: {profesional}")
                
                if not profesional.estado:
                    print("Profesional asociado inactivo.")
                    messages.error(request, "Tu cuenta de profesional no está activa.")
                    return redirect("login")

            # Verificación de usuarios con rol cliente
            elif hasattr(user, 'cliente'):
                cliente = user.cliente
                print(f"Verificando cliente asociado: {cliente}")
                
                if not cliente.estado:
                    print("Cliente asociado inactivo.")
                    messages.error(request, "Tu cuenta de cliente no está activa.")
                    return redirect("login")

            # Si pasa todas las verificaciones
            print("Verificación completada, iniciando sesión.")
            login(request, user)
            messages.success(request, "Se ha iniciado sesión.")
            return redirect("index")

        else:
            # Autenticación fallida
            print("Error de autenticación: Usuario o contraseña incorrectos.")
            messages.error(request, "Hubo un error al iniciar sesión, por favor verifica tus datos.")
            return redirect("login")

    # Si el método no es POST, renderizar el formulario de login
    return render(request, 'usuarios/login.html')




def logoutUser(request):
    logout(request)
    messages.success(request, "Se ha cerrado sesión.")
    return redirect("index")


class ListUsuarios(LoginRequiredMixin, AdminRequiredMixin, ListView):
 
    model = Usuario
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios' 
    paginate_by = 10
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Usuario.objects.filter(rol='Cliente').select_related('cliente')
        context['profesionales'] = Usuario.objects.filter(rol='Abogado').select_related('profesional')  # Cambiado a 'profesional'
        context['admins'] = Usuario.objects.filter(rol='Admin')
        return context
    

@login_required
def createUsuario(request, rol):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            # Asignación del rol y vínculo con cliente o profesional según el rol
            if rol == 'Cliente' and form.cleaned_data['cliente']:
                user.rol = rol
                user.cliente = form.cleaned_data['cliente']
            elif rol == 'Abogado' and form.cleaned_data['profesional']:
                user.rol = rol
                user.profesional = form.cleaned_data['profesional']
            elif rol == 'Admin':
                user.rol = rol
            
            user.save()
            messages.success(request, f'Usuario {user.email} creado exitosamente como {rol}.')
            return redirect('usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/create-usuario.html', {'form': form, 'tipo_usuario': rol})






from django.contrib.auth.hashers import make_password

@login_required
def updateUsuario(request, pk):
    user = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        
        if form.is_valid():
            # Verifica si la contraseña ha sido cambiada y encripta si es necesario
            password = form.cleaned_data.get('password')
            if password:
                print("Actualizando contraseña...")
                user.password = make_password(password)
            
            # Imprime los valores de cliente y profesional para diagnóstico
            cliente = form.cleaned_data.get('cliente')
            profesional = form.cleaned_data.get('profesional')
            print(f"Vinculando Cliente: {cliente}")
            print(f"Vinculando Profesional: {profesional}")

            # Guarda el formulario
            form.save()
            messages.success(request, f'Usuario {user.email} actualizado exitosamente.')
            return redirect('usuarios')  # Cambia por la URL de éxito
        else:
            print("Formulario inválido:", form.errors)

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