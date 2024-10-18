from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Usuario
from .forms import UsuarioForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'admin'


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
    

class CreateUsuarioView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/create-usuario.html'
    success_url = reverse_lazy('index')  # Reemplaza con tu URL de éxito

    def form_valid(self, form):
        # Guardar el usuario con la contraseña proporcionada
        user = form.save()
        
        # Enviar correo electrónico al nuevo usuario
        send_mail(
            'Bienvenido a Nuestro Estudio Jurídico',
            f'Hola {user.username},\n\nTu cuenta ha sido creada. Puedes iniciar sesión en nuestro sitio web con tu email: {user.email} y la contraseña que te ha proporcionado el estudio.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return super().form_valid(form)

        