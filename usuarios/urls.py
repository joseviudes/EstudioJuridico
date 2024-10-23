from django.urls import path
from .views import loginUser, logoutUser, ListUsuarios , createUsuario, updateUsuario, deleteUsuario

urlpatterns = [

    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),

    path("", ListUsuarios.as_view(), name="usuarios"),
    path('crear-usuario/', createUsuario, name="crear-usuario"),
    path('actualizar-usuario/<int:pk>/', updateUsuario, name="actualizar-usuario"),
    path('eliminar-usuario/<int:pk>/', deleteUsuario, name="eliminar-usuario"),

]
