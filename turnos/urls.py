from django.urls import path
from .views import ListTurno, singleTurno, createTurno, updateTurno, deleteTurno, agendaView, obtenerTurnos

urlpatterns = [
    path("", ListTurno.as_view(), name="turnos"),
    path("turno/<int:pk>/", singleTurno, name="turno"),
    path("crear-turno/", createTurno, name="crear-turno"),
    path("actualizar-turno/<int:pk>/", updateTurno, name="actualizar-turno"),
    path("eliminar-turno/<int:pk>/", deleteTurno, name="eliminar-turno"),
    
    path("agenda/", agendaView, name="agenda"),
    path("api/turno/", obtenerTurnos, name="obtener-turnos"),
    
]