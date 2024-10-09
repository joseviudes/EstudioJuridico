from django.urls import path
from .views import loginUser, logoutUser, registerUser

urlpatterns = [
    #path("user-profile/", userProfile, name="user-profile"),
    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),
    
    path('register/', registerUser, name="register"),

]
