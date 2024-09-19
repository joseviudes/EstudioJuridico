from django.urls import path
from .views import lista_de_turnos, turno, crear_turno, eliminar_turno

urlpatterns = [
    path("", lista_de_turnos, name="turnos"),
    path("turno/<int:pk>/", turno, name="turno"),
    path("crear-turno/", crear_turno, name="crear-turno"),
    path("eliminar-turno/<int:pk>/", eliminar_turno, name="eliminar-turno"),
    
]