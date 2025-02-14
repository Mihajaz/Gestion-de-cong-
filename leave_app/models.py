from django.db import models
from viewflow.models import Process
from django.contrib.auth.models import User

# Create your models here.

#modèle employé
class Employee(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    poste = models.CharField(max_length=100, null=True, blank=True) 
    
    def __str__(self):
        return self.user_id.username if self.user_id else "Employe sans utilisateur"
    
#demander un congé
class LeaveRequest(models.Model):
    employee = models.ForeignKey('Employee', verbose_name="Employé", on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.TextField(max_length=50)
    request_status = models.CharField(max_length=20, default="En attente", choices=[("En attente", "En attente"), ("Validé", "Validé"), ("Refusé", "Refusé")])
    process = models.OneToOneField('LeaveRequestProcess', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Congé de {self.employee.user_id.username} ({self.start_date} - {self.end_date})"
   


    
    
    
    
class LeaveRequestProcess(Process):
    leave_request = models.OneToOneField(
        LeaveRequest, on_delete=models.CASCADE, related_name="leave_request_process"
    )
    
    is_manager_approved = models.BooleanField(
        help_text="Validation de la demande de congé par le manager",
        verbose_name=(" Approbation par le Manager"),
        default=False
    )
    is_director_approved = models.BooleanField(
        help_text="Validation de la demande de congé par le directeur",
        verbose_name=("Approbation par le Directeur"),
        default=False
    )
    is_finalized = models.BooleanField(
        help_text="Finalisation de la demande de congé",
        verbose_name=("Terminé"),
        default=False
       
    )
    
    def __str__(self):
        return f"Process de demande de congé {self.leave_request.employee.user_id.username}"




    
    

