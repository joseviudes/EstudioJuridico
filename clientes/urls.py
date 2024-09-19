from django.urls import path

from .views import lista_de_clientes, cliente, crear_cliente, actualizar_cliente, eliminar_cliente

urlpatterns = [
    path("", lista_de_clientes, name="clientes"),
    path("cliente/<int:pk>/", cliente, name='cliente'),
    path("crear-cliente/", crear_cliente, name="crear-cliente"),
    path("actualizar-cliente/<int:pk>/", actualizar_cliente, name="actualizar-cliente"),
    path("eliminar-cliente/<int:pk>/", eliminar_cliente, name="eliminar-cliente"),
]
