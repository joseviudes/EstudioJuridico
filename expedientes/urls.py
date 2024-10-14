from django.urls import path

from .views import ListExpediente, singleExpediente, createExpediente, updateExpediente, deleteExpediente, ListMovimientos, createMovimiento, updateMovimiento, deleteMovimiento

urlpatterns = [
    path("", ListExpediente.as_view(), name="expedientes"),
    path("expediente/<int:pk>/", singleExpediente, name='expediente'),
    path("crear-expediente/", createExpediente, name="crear-expediente"),
    path("actualizar-expediente/<int:pk>/", updateExpediente, name="actualizar-expediente"),
    path("eliminar-expediente/<int:pk>/", deleteExpediente, name="eliminar-expediente"),
    
    path('<int:numero_expediente>/movimientos/', ListMovimientos, name='movimientos'),
    path('<int:numero_expediente>/movimientos/crear-movimiento', createMovimiento, name='crear-movimiento'),
    path('<int:id_mov>/movimientos/actualizar-movimiento/', updateMovimiento, name='actualizar-movimiento'),
    path('<int:id_mov>/movimientos/eliminar-movimiento/', deleteMovimiento, name='eliminar-movimiento'),

]


