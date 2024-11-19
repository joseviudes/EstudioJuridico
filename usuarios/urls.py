from django.urls import path
from .views import loginUser, logoutUser, ListUsuarios , createUsuario, updateUsuario, deleteUsuario

urlpatterns = [

    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),

    path("", ListUsuarios.as_view(), name="usuarios"),
    
    path('crear-usuario/administrador/', createUsuario, {'rol': 'Admin'}, name='crear_administrador'),
    path('crear-usuario/profesional/', createUsuario, {'rol': 'Abogado'}, name='crear_profesional'),
    path('crear-usuario/cliente/', createUsuario, {'rol': 'Cliente'}, name='crear_cliente'),
    path('crear-usuario/secretari@/', createUsuario, {'rol': 'Secretaria'}, name='crear_secretaria'),
    
    path('actualizar-usuario/<int:pk>/', updateUsuario, name="actualizar-usuario"),
    
    path('eliminar-usuario/<int:pk>/', deleteUsuario, name="eliminar-usuario"),

]
