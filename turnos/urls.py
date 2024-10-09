from django.urls import path
from .views import ListTurno, singleTurno, createTurno, deleteTurno, agendaView, get_turnos

urlpatterns = [
    path("", ListTurno.as_view(), name="turnos"),
    path("turno/<int:pk>/", singleTurno, name="turno"),
    path("crear-turno/", createTurno, name="crear-turno"),
    path("eliminar-turno/<int:pk>/", deleteTurno, name="eliminar-turno"),
    
    path("agenda/", agendaView, name="agenda"),
    path("get-turnos/", get_turnos, name="get-turnos"),
    
]