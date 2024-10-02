from django.urls import path

from .views import ListCliente, singleCliente, createCliente, updateCliente, deleteCliente

urlpatterns = [
    path("", ListCliente.as_view(), name="clientes"),
    path("cliente/<int:pk>/", singleCliente, name='cliente'),
    path("crear-cliente/", createCliente, name="crear-cliente"),
    path("actualizar-cliente/<int:pk>/", updateCliente, name="actualizar-cliente"),
    path("eliminar-cliente/<int:pk>/", deleteCliente, name="eliminar-cliente"),
]
