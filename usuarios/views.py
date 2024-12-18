from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required

from .models import Usuario
from .forms import UsuarioForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'Admin'

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Log para verificar los valores de entrada
        print(f"Intento de login con: username={username}, password={'*' * len(password)}")

        # Comprobación de existencia del usuario
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            print("Error: El usuario no existe.")
            messages.error(request, "No existe un usuario con este nombre de usuario. Por favor intenta de nuevo.")
            return redirect("login")

        # Si el usuario existe, intenta autenticar con la contraseña proporcionada
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Usuario autenticado: {user.username}")

            # Verificación para usuarios Admin
            if user.is_superuser or (not hasattr(user, 'profesional') and not hasattr(user, 'cliente') and not hasattr(user, 'secretaria')):
                print("Usuario es Admin o no tiene rol vinculado; omitiendo verificaciones adicionales.")
                login(request, user)
                messages.success(request, "Se ha iniciado sesión.")
                return redirect("profesionales")  # Redirigir a 'profesionales' para Admin

            # Verificación de usuarios con rol profesional (Abogado)
            if hasattr(user, 'profesional') and user.profesional is not None:
                profesional = user.profesional
                print(f"Verificando profesional asociado: {profesional}")
                
                if not profesional.estado:
                    print("Profesional asociado inactivo.")
                    messages.error(request, "Tu cuenta de profesional no está activa.")
                    return redirect("login")

                login(request, user)
                messages.success(request, "Se ha iniciado sesión.")
                return redirect("clientes")  # Redirigir a 'clientes' para Abogado

            # Verificación de usuarios con rol cliente
            elif hasattr(user, 'cliente') and user.cliente is not None:
                cliente = user.cliente
                print(f"Verificando cliente asociado: {cliente}")
                
                if not cliente.estado:
                    print("Cliente asociado inactivo.")
                    messages.error(request, "Tu cuenta de cliente no está activa.")
                    return redirect("login")

                login(request, user)
                messages.success(request, "Se ha iniciado sesión.")
                return redirect("expedientes")  # Redirigir a 'expedientes' para Cliente

            # Verificación de usuarios con rol secretaria
            elif hasattr(user, 'secretaria') and user.secretaria is not None:
                secretaria = user.secretaria
                print(f"Verificando secretaria asociada: {secretaria}")

                if not secretaria.estado:
                    print("Secretaria asociada inactiva.")
                    messages.error(request, "Tu cuenta de secretaria no está activa.")
                    return redirect("login")

                login(request, user)
                messages.success(request, "Se ha iniciado sesión.")
                return redirect("clientes")  # Redirigir a 'secretarias' para Secretaria

        else:
            # Si el usuario existe pero la contraseña es incorrecta
            print("Error: Contraseña incorrecta.")
            messages.error(request, "La contraseña es incorrecta. Por favor, intenta nuevamente.")
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
        context['secretarias'] = Usuario.objects.filter(rol='Secretaria').select_related('secretaria')
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
            elif rol == 'Secretaria' and form.cleaned_data['secretaria']:
                user.rol = rol
                user.secretaria = form.cleaned_data['secretaria']
            elif rol == 'Admin':
                user.rol = rol
            
            user.save()
            messages.success(request, f'Usuario {user.email} creado exitosamente como {rol}.')
            return redirect('usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/create-usuario.html', {'form': form, 'tipo_usuario': rol})


@login_required
def updateUsuario(request, pk):
    user = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user, rol=user.rol)
        if form.is_valid():
            # Verifica si la contraseña ha sido cambiada y encripta si es necesario
            password = form.cleaned_data.get('password')
            if password:
                user.password = make_password(password)
            form.save()
            messages.success(request, f'Usuario {user.email} actualizado exitosamente.')
            return redirect('usuarios')
        else:
            print("Formulario inválido:", form.errors)
    else:
        form = UsuarioForm(instance=user, rol=user.rol)

    return render(request, 'usuarios/update-usuario.html', {'form': form, 'usuario': user})


@login_required
def deleteUsuario(request, pk):

    user = get_object_or_404(Usuario, pk=pk)  # Busca el usuario por su ID

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuario {user.email} eliminado exitosamente.')
        return redirect('usuarios')  # Cambia por la URL de éxito

    return render(request, 'usuarios/delete-usuario.html', {'usuario': user})