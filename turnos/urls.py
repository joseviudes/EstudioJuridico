from django.urls import path
from .views import ListTurno,singleTurno, createTurno, deleteTurno

urlpatterns = [
    path("", ListTurno.as_view(), name="turnos"),
    path("turnos/<int:pk>/", singleTurno, name="turno"),
    path("create-turno/", createTurno, name="create-turno"),
    path("delete-turno/", deleteTurno, name="delete-turno"),
    
]