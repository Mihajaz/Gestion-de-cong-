from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Employee, LeaveRequest


# Interface d'accueil
class HomeView(TemplateView):
    template_name = "home.html"


# Interface de validation pour Directeur et Manager
class ValidationView(LoginRequiredMixin, TemplateView):
    template_name = "validation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demandes"] = LeaveRequest.objects.filter(status="En attente")
        return context


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
        return redirect("employe")

# Déconnexion
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Vous avez été déconnecté.")
        return super().dispatch(request, *args, **kwargs)


# Interface employé avec demande de congé
class VacationView(LoginRequiredMixin, TemplateView):
    template_name = "employe.html"
    success_url = reverse_lazy("employe")

    def post(self, request, *args, **kwargs):
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        if start_date and end_date and reason:
            employee = request.user.employee
            LeaveRequest.objects.create(
                employee=employee,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                status="En attente",
            )
            messages.success(request, "Votre demande de congé a bien été envoyée.")
            return redirect("employe")

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.request.user.employee
        context["pending_leave_requests"] = LeaveRequest.objects.filter(employee=employee).order_by("-id")
        return context




