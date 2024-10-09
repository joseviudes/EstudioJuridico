from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Usuario
from .forms import RegisterForm
# Create your views here.

# class LoginUserView(LoginView):
#     model = Usuario
#     template_name = "usuarios/login.html"

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

# class RegisterView(CreateView):

#     model = Usuario
#     template_name = 'usuarios/register.html'
#     form_class = UserAdminCreationForm
#     success_url = reverse_lazy('index')
    
#     def form_valid(self, form):
#         messages.info(
#             self.request, "Se ha registrado correctamente. Por favor inicie sesión."
#         )
#         return super().form_valid(form)

def registerUser(request):
    
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Se ha registrado correctamente")
            return redirect('index')
        else:
            messages.error(request, "Hubo un error al registrarse, por favor verifique los datos.")
            return redirect("register")
        
    context = {'form':form}
        
    return render(request, 'usuarios/register.html', context)
    

        