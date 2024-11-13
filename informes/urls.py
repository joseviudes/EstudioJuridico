from django.urls import path

from .views import *

urlpatterns = [
    path('', Informe.as_view(), name="informes"),
    path('informe-abogado-turnos/', informeAbogado, name="informe-abogado-turnos"),
    path('descargar-informe-pdf/', generarInformePdf, name='descargar_informe_pdf'),
]
