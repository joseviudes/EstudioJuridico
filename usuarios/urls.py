from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    #path("user-profile/", userProfile, name="user-profile"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),

]
