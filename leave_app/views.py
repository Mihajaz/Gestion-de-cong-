from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Employee, LeaveRequest,LeaveRequestProcess
from viewflow import flow 
from viewflow.flow.views import UpdateProcessView,TaskListView, CreateProcessView,DetailProcessView
from viewflow.models import Process

# Interface d'accueil
class HomeView(TemplateView):
    template_name = "home.html"


# Interface de validation pour Directeur et Manager

class CreateRequest(CreateProcessView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demandes"] = LeaveRequest.objects.filter(request_status="En attente")
        return context
    
    def get(self, request, *args, **kwargs):
        context = {
            "user": self.request.user,
            "activation": self.activation,
            
        }
        return render(request,"leave_app/templates/validation.html",context)
    def post(self, request, *args, **kwargs):
        self.get
        
  
    



#logique pour la validation et le lancement de viewflow
class RequestUpdateStatusView(UpdateProcessView):
    
    def get(self, request, *args, **kwargs):
        process = self.get_object()
        # leave_process_form = LeaveRequestProcess(instance=process)
        leave_request = process.leave_request
        activation = self.activation
        task_name = str(activation.flow_task)
        
        print('--- TASK NAME ---')
        print(task_name)
        
        context = {
            "leave_request": leave_request,
            "user": request.user,
            "activation": activation,
        }
        
        return render(request, 'leave_app/templates/validation.html', context)

    def get_process_and_task(self):
        """Retourner le processus et la tâche à partir de l'URL"""
        process_pk = self.kwargs.get('process_pk')
        task_pk = self.kwargs.get('task_pk')
        process = LeaveRequestProcess.objects.get(pk=process_pk)
        task = process.get_task(task_pk)
        return process, task

    def post(self, request, *args, **kwargs):
        leave_request_id = request.POST.get("leave_request_id")
        action = request.POST.get("action")

        if leave_request_id and action:
            try:
                #leave_request = LeaveRequest.objects.get(id=leave_request_id)
                leave_request_process = self.activation.process

                # Récupérer le processus et la tâche
                #process, task = self.get_process_and_task()

                if action == "valider_manager":
                    leave_request_process.is_manager_approved = True
                    messages.success(request, f"La demande de congé de {leave_request_process.leave_request.employee.user_id.username} a été approuvée par le manager.")
                elif action == "refuser_manager":
                    leave_request_process.is_manager_approved = False
                    messages.success(request, f"La demande de congé de {leave_request_process.leave_request.employee.user_id.username} a été refusée par le manager.")
                elif action == "valider_directeur":
                    leave_request_process.is_director_approved = True
                    messages.success(request, f"La demande de congé de {leave_request_process.leave_request.employee.user_id.username} a été approuvée par le directeur.")
                elif action == "refuser_directeur":
                    leave_request_process.is_director_approved = False
                    messages.success(request, f"La demande de congé de {leave_request_process.leave_request.employee.user_id.username} a été refusée par le directeur.")

                # Sauvegarder l'état de la demande de congé et du processus
                leave_request_process.save()
                self.activation.done()

                # Sauvegarder les modifications du processus et de la tâche
                #process.save()
                #task.save()

                # Rediriger vers la page de validation
                return redirect("manager_approval")

            except LeaveRequest.DoesNotExist:
                messages.error(request, "Demande de congé introuvable.")

        


# Inscription
class RegisterView(TemplateView):
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            username = request.POST["username"]
            poste = request.POST["poste"]
            password = request.POST["password"]
            email = request.POST["email"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur existe déjà")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                Employee.objects.create(user_id=user, poste=poste)
                messages.success(request, "Inscription réussie. Connectez-vous maintenant !")
                return redirect("login")

        return self.get(request, *args, **kwargs)


# Connexion
class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        # Vérifier si l'utilisateur a un employé associé
        if hasattr(user, "employee") and user.employee.poste in ["Directeur", "Manageur"]:
            return redirect("validation")
        return redirect("/flow/start")

# Déconnexion
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Vous avez été déconnecté.")
        return super().dispatch(request, *args, **kwargs)


# Interface employé avec demande de congé
class VacationRequestView(LoginRequiredMixin, CreateProcessView):
    template_name = "employe.html"
    
    def post(self, request, *args, **kwargs):
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        if start_date and end_date and reason:
            employee = request.user.employee
            
            leave_request = LeaveRequest.objects.create(
                employee=employee,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                request_status="En attente",
            )
            leave_request.save
            self.activation.process.leave_request = leave_request
            self.activation.process.save()
            self.activation.done()
            
        
            messages.success(request, "Votre demande de congé a bien été envoyée.")
            

        return self.get(request, *args, **kwargs)

    




