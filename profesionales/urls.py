from django.urls import path

from .views import ListProfesional, singleProfesional, createProfesional, updateProfesional, deleteProfesional

urlpatterns = [
    path("", ListProfesional.as_view(), name="profesionales"),
    path("profesional/<int:pk>/", singleProfesional, name="profesional"),
    path("create-profesionales/", createProfesional, name="create-profesionales"),
    path("update-profesional/", updateProfesional, name="update-profesional"),
    path("delete-profesional/", deleteProfesional, name="delete-profesional")
]
