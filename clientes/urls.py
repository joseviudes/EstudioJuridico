from django.urls import path

from .views import ListCliente, ListClienteInactivo, singleCliente, createCliente, updateCliente, deleteCliente, darDeAltaCliente, darDeBajaCliente

urlpatterns = [
    path("", ListCliente.as_view(), name="clientes"),
    path('clientes-inactivos/', ListClienteInactivo.as_view(), name='clientes-inactivos'),
    path("cliente/<int:pk>/", singleCliente, name='cliente'),
    path("crear-cliente/", createCliente, name="crear-cliente"),
    path("actualizar-cliente/<int:pk>/", updateCliente, name="actualizar-cliente"),
    path("eliminar-cliente/<int:pk>/", deleteCliente, name="eliminar-cliente"),
    
    path("dar-de-baja/<int:dni>/", darDeBajaCliente, name="dar-de-baja-cliente"),
    path("dar-de-alta/<int:dni>/", darDeAltaCliente, name="dar-de-alta-cliente")
    
]
