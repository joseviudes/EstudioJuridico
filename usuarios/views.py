from django.shortcuts import render

# Create your views here.

def userProfile(request):
    
    
    return render(request, "usuarios/user-profile.html")