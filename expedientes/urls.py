from django.urls import path

from .views import lista_de_expedientes, expediente, crear_expedientes, actualizar_expediente, eliminar_expediente

urlpatterns = [
    path("", lista_de_expedientes, name="expedientes"),
    path("expediente/<int:pk>/", expediente, name='expediente'),
    path("crear-expediente/", crear_expedientes, name="crear-expediente"),
    path("actualizar-expediente/<int:pk>/", actualizar_expediente, name="actualizar-expediente"),
    path("eliminar-expediente/<int:pk>/", eliminar_expediente, name="eliminar-expediente"),
]


