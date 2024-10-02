from django.urls import path
from .views import loginUser, logoutUser, RegisterView

urlpatterns = [
    #path("user-profile/", userProfile, name="user-profile"),
    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),
    
    path('register/', RegisterView.as_view(), name="register"),

]
