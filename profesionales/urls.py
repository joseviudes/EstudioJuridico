from django.urls import path

from .views import ListProfesional, ListProfesionalInactivo, detailProfesional, createProfesional, updateProfesional, deleteProfesional, darDeAltaProfesional, darDeBajaProfesional

urlpatterns = [
    path("", ListProfesional.as_view(), name="profesionales"),
    path('profesionales-inactivos/', ListProfesionalInactivo.as_view(), name='profesionales-inactivos'),
    path("profesional/<int:pk>/", detailProfesional, name="profesional"),
    path("crear-profesional/", createProfesional, name="crear-profesional"),
    path("actualizar-profesional/<int:pk>/", updateProfesional, name="actualizar-profesional"),
    path("eliminar-profesional/<int:pk>/", deleteProfesional, name="eliminar-profesional"),
    
    path("dar-de-baja/<int:dni>/", darDeBajaProfesional, name="dar-de-baja-profesional"),
    path("dar-de-alta/<int:dni>/", darDeAltaProfesional, name="dar-de-alta-profesional"),
    
]
