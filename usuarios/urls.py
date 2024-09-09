from django.urls import path
from .views import *

urlpatterns = [
    path("user-profile/", userProfile, name="user-profile"),
    
]
