from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexView

urlpatterns = [

    path("profesionales/", include("profesionales.urls")),
    path("clientes/", include("clientes.urls")),
    path("expedientes/", include("expedientes.urls")),
    path("turnos/", include("turnos.urls")),
    
    path("usuarios/", include("usuarios.urls")),

    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

