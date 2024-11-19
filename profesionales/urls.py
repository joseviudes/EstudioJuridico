from django.urls import path

from .views import *

urlpatterns = [
    path("", ListProfesional.as_view(), name="profesionales"),
    path("profesionales-inactivos/", ListProfesionalInactivo.as_view(), name='profesionales-inactivos'),
    path("profesional/<int:pk>/", detailProfesional, name="profesional"),
    path("crear-profesional/", createProfesional, name="crear-profesional"),
    path("actualizar-profesional/<int:pk>/", updateProfesional, name="actualizar-profesional"),
    path("eliminar-profesional/<int:pk>/", deleteProfesional, name="eliminar-profesional"),
    path("dar-de-baja/<int:dni>/", darDeBajaProfesional, name="dar-de-baja-profesional"),
    path("dar-de-alta/<int:dni>/", darDeAltaProfesional, name="dar-de-alta-profesional"),
    
    path("secretarias/", ListSecretaria.as_view(), name="secretarias"),
    path("secretarias-inactivos/", ListSecretariaInactivo.as_view(), name='secretarias-inactivos'),
    path("secretaria/<int:pk>/", detailSecretaria, name="secretaria"),
    path("crear-secretaria/", createSecretaria, name="crear-secretaria"),
    path("actualizar-secretaria/<int:pk>/", updateSecretaria, name="actualizar-secretaria"),
    path("dar-de-baja-secretaria/<int:dni>/", darDeBajaSecretaria, name="dar-de-baja-secretaria"),
    path("dar-de-alta-secretaria/<int:dni>/", darDeAltaSecretaria, name="dar-de-alta-secretaria"),
    
]
