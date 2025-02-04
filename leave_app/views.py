from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout




# Create your views here.

#interface d'accueil
def home(request):
    return render(request, 'home.html')

#interface du directeur et manageur
@login_required
def validation(request):
    return render(request,'validation.html')

#interface et condition de signin
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        #verification des utilisateurs si il existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request,"ce nom d'utilisateur existe déja") 
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request,"Inscription reussie.Connecter-vous maintenant!")
            return redirect('login')
    
    return render(request,'register.html')
      
      #interface et condition de login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('home')  # Redirige vers la page d'accueil
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')
            

#interface de login
def login(request):
    return render(request,'login.html')
#logout
def user_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('login')

#interface des employés
@login_required
def employe(request):
    return render(request,'employe.html')

