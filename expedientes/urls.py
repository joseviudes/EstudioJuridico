from django.urls import path

from .views import ListExpediente, singleExpediente, createExpediente, updateExpediente, deleteExpediente, ListMovimientos, createMovimiento, updateMovimiento, deleteMovimiento

urlpatterns = [
    path("", ListExpediente.as_view(), name="expedientes"),
    path("expediente/<str:numero_expediente>/", singleExpediente, name='expediente'),
    path("crear-expediente/", createExpediente, name="crear-expediente"),
    path("actualizar-expediente/<str:numero_expediente>/", updateExpediente, name="actualizar-expediente"),
    path("eliminar-expediente/<str:numero_expediente>/", deleteExpediente, name="eliminar-expediente"),
    
    path('<str:numero_expediente>/movimientos/', ListMovimientos, name='movimientos'),
    path('<str:numero_expediente>/movimientos/crear-movimiento', createMovimiento, name='crear-movimiento'),
    path('<int:id_mov>/movimientos/actualizar-movimiento/', updateMovimiento, name='actualizar-movimiento'),
    path('<int:id_mov>/movimientos/eliminar-movimiento/', deleteMovimiento, name='eliminar-movimiento'),

]


