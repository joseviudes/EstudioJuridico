from django.urls import path

from .views import lista_de_profesionales, profesional, crear_profesional, actualizar_profesional, eliminar_profesional

urlpatterns = [
    path("", lista_de_profesionales, name="profesionales"),
    path("profesional/<int:pk>/", profesional, name="profesional"),
    path("crear-profesional/", crear_profesional, name="crear-profesional"),
    path("actualizar-profesional/<int:pk>/", actualizar_profesional, name="actualizar-profesional"),
    path("eliminar-profesional/<int:pk>/", eliminar_profesional, name="eliminar-profesional")
]
