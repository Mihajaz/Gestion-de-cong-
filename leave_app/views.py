from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Employee, LeaveRequest

# Create your views here.

#interface d'accueil
def home(request):
    return render(request, 'home.html')

#interface du directeur et manageur
@login_required
def validation(request):
    if request.user.employee.poste not in ["Directeur", "Manageur"]:
        return redirect('employe')
    
    if request.method == "POST":
        leave_request_id = request.POST.get("leave_request_id")
        action = request.POST.get("action")  # 'valider' ou 'refuser'

        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Demande de congé introuvable.")
            return redirect('validation')

        if action == "valider":
            if request.user.employee.poste == "Manageur":
                leave_request.status = "En attente" # En attente de validation par le directeur
            else:
                leave_request.status = "Validé" # Demande validee par le directeur  
                leave_request.save()
                messages.success(request, f"Demande de congé validée")
                return redirect('validation')

        elif action == "refuser":
            leave_request.status = "Refusé"
         
        
        leave_request.save()
        messages.success(request, f"Demande de congé {action}e avec succès.")
    
    demandes = LeaveRequest.objects.filter(status="En attente")
    return render(request, 'validation.html', {'demandes': demandes})



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
    if request.method == "POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']
        
        
        if start_date and end_date and reason:
            #recupère l'Employee associe a l'utilisateur
            employee = request.user.employee
            
            #Cree et enregistre la demande de congé
            LeaveRequest.objects.create(
                employee=employee,
                start_date=start_date,
                end_date=end_date,  
                reason=reason,
                status = "En attente",
            )
         
    
            messages.success(request, "Votre demande de conge a bien ete envoyee.")
            return redirect('employe')
    # Récupérer la dernière demande de congé en attente de l'utilisateur
    employee = request.user.employee
    pending_leave_requests = LeaveRequest.objects.filter(employee=employee).order_by('-id')  
    return render(request, 'employe.html', {'pending_leave_requests': pending_leave_requests})
            
    

