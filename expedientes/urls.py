from django.urls import path

from .views import ListExpediente, singleExpediente, createExpediente, updateExpediente, deleteExpediente

urlpatterns = [
    path("", ListExpediente.as_view(), name="expedientes"),
    path("expediente/<int:pk>/", singleExpediente, name='expediente'),
    path("crear-expediente/", createExpediente, name="crear-expediente"),
    path("actualizar-expediente/<int:pk>/", updateExpediente, name="actualizar-expediente"),
    path("eliminar-expediente/<int:pk>/", deleteExpediente, name="eliminar-expediente"),
]


