from django.urls import path

from .views import ListProfesional, singleProfesional, createProfesional, updateProfesional, deleteProfesional

urlpatterns = [
    path("", ListProfesional.as_view(), name="profesionales"),
    path("profesional/<int:pk>/", singleProfesional, name="profesional"),
    path("crear-profesional/", createProfesional, name="crear-profesional"),
    path("actualizar-profesional/<int:pk>/", updateProfesional, name="actualizar-profesional"),
    path("eliminar-profesional/<int:pk>/", deleteProfesional, name="eliminar-profesional")
]
