from django.urls import path
from .views import ListTurno, singleTurno, createTurno, deleteTurno

urlpatterns = [
    path("", ListTurno.as_view(), name="turnos"),
    path("turno/<int:pk>/", singleTurno, name="turno"),
    path("crear-turno/", createTurno, name="crear-turno"),
    path("eliminar-turno/<int:pk>/", deleteTurno, name="eliminar-turno"),
    
]