from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Employee




# Create your views here.

#interface d'accueil
def home(request):
    return render(request, 'home.html')

#interface du directeur et manageur

def validation(request):
    return render(request,'validation.html')

#interface et condition de signin
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        poste = request.POST['poste']
        password = request.POST['password']
        email = request.POST['email']
    
        print("PARAMS POST")
        print(request.POST)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        
        if Employee.objects.filter(user_id=user.id).exists():
            messages.error(request,"ce nom d'utilisateur existe déja") 
        else:
            Employee.objects.create(user_id=user, poste=poste)
            messages.success(request,"Inscription reussie.Connecter-vous maintenant!")
            return redirect('login')
    
    return render(request,'register.html')
      
      
# interface et condition de login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # print(request.POST)
        # print(username)
        
        user = authenticate(request, username=username, password=password)  # Vérifie les identifiants
        
        if user is not None:
            print('logged in')
            login(request,user) 
            
            # Connecte l'utilisateur
            messages.success(request, "Connexion réussie.")

            # Redirection en fonction du poste
        
            if user.employee.poste in ["Directeur", "Manageur"]:
                return redirect('validation')
            else:
                return redirect('employe')
        
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')







#logout
def user_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('login')

#interface des employés
@login_required
def employe(request):
    return render(request,'employe.html')

