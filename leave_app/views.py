from django.shortcuts import render




# Create your views here.

#interface d'accueil
def home(request):
    return render(request, 'home.html')

#interface du directeur et manageur
def validation(request):
    return render(request,'validation.html')

#interface de login
def register(request):
    return render(request,'register.html')

def employe(request):
    return render(request,'employe.html')

