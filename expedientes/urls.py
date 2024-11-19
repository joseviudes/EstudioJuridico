from django.urls import path
from . import views
from .views import ListExpediente, ListExpedienteInactivo, singleExpediente, createExpediente, updateExpediente, deleteExpediente, darDeAltaExpediente, darDeBajaExpediente,  ListMovimientos, createMovimiento, updateMovimiento, deleteMovimiento

urlpatterns = [
    path("", ListExpediente.as_view(), name="expedientes"),
    path("expedientes-inactivos", ListExpedienteInactivo.as_view(), name="expedientes-inactivos"),
    path("expediente/<str:numero_expediente>/", singleExpediente, name='expediente'),
    path("crear-expediente/", createExpediente, name="crear-expediente"),
    path("actualizar-expediente/<str:numero_expediente>/", updateExpediente, name="actualizar-expediente"),
    path("eliminar-expediente/<str:numero_expediente>/", deleteExpediente, name="eliminar-expediente"),
    
    path("dar-de-baja/<str:numero_expediente>/", darDeBajaExpediente, name="dar-de-baja-expediente"),
    path("dar-de-alta/<str:numero_expediente>/", darDeAltaExpediente, name="dar-de-alta-expediente"),
    
    path('<str:numero_expediente>/movimientos/', ListMovimientos, name='movimientos'),
    path('<str:numero_expediente>/movimientos/crear-movimiento', createMovimiento, name='crear-movimiento'),
    path('<int:id_mov>/movimientos/actualizar-movimiento/', updateMovimiento, name='actualizar-movimiento'),
    path('<int:id_mov>/movimientos/eliminar-movimiento/', deleteMovimiento, name='eliminar-movimiento'),

     path('generar-numero-expediente/<str:tipo_expediente>/', views.generar_numero_expediente, name='generar_numero_expediente'),

]


