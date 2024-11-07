from django.urls import path
from .views import * 

urlpatterns = [
    path("", ListTurno.as_view(), name="turnos"),
    path("turno/<int:pk>/", singleTurno, name="turno"),
    path("crear-turno/", createTurno, name="crear-turno"),
    path("actualizar-turno/<int:pk>/", updateTurno, name="actualizar-turno"),
    path("actualizar-estado/<int:pk>/", updateEstado, name="actualizar-estado"),
    path("eliminar-turno/<int:pk>/", deleteTurno, name="eliminar-turno"),
    path("horarios-ocupados/", horariosOcupados, name='horarios-ocupados'),
    
    path("agenda/", agendaView, name="agenda"),
    path("turnos-json/", turnos_json, name='turnos-json'),
    
    path("crear-tarea/", createTarea, name="crear-tarea"),
    path("tareas-json/", tareas_json, name="tareas-json"),
    
]