from django.urls import path
from .views import loginUser, logoutUser, CreateUsuarioView, ListUsuarios

urlpatterns = [
    #path("user-profile/", userProfile, name="user-profile"),
    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),

    path("", ListUsuarios.as_view(), name="usuarios"),
    path('create-user/', CreateUsuarioView.as_view(), name="create-user"),

]
