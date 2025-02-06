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
    
    
class Approval(models.Model):
    leave_request = models.ForeignKey('LeaveRequest', verbose_name=("Demande de congé"), on_delete=models.CASCADE)
    responsable = models.CharField(max_length=50)
    direction = models.CharField(max_length=50)
    



    
    
