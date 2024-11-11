from django.urls import path

from .views import Informe, informeAbogado

urlpatterns = [
    path('', Informe.as_view(), name="informes"),
    path('informe-abogado-turnos/', informeAbogado, name="informe-abogado-turnos")
]
