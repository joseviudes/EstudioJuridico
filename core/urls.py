from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path("profesionales/", include("profesionales.urls")),
    path("clientes/", include("clientes.urls")),
    path("expedientes/", include("expedientes.urls")),
    path("turnos/", include("turnos.urls")),
    
    path("usuarios/", include("usuarios.urls")),
    
    path('admin/', admin.site.urls),
]
