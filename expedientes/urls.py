from django.urls import path

from .views import ListExpediente, singleExpediente, createExpediente, updateExpediente, deleteExpediente

urlpatterns = [
    path("", ListExpediente.as_view(), name="expedientes"),
    path("expedientes/<int:pk>/", singleExpediente, name='expediente'),
    path("create-expediente/", createExpediente, name="create-expediente"),
    path("update-expediente/", updateExpediente, name="update-expediente"),
    path("delete-expediente/", deleteExpediente, name="delete-expediente"),
]
