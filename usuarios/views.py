from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Usuario
from .forms import UserAdminCreationForm
# Create your views here.

class LoginView(LoginView):
    model = Usuario
    template_name = "usuarios/login.html"


class RegisterView(CreateView):

    model = Usuario
    template_name = 'usuarios/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        messages.info(
            self.request, "Se ha registrado correctamente. Por favor inicie sesión."
        )
        return super().form_valid(form)
    

        