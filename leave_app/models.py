from django.db import models
from viewflow.models import Process
# Create your models here.

#modèle employé
class Employee(models.Model):
    username = models.CharField(max_length=50, default="username")
    email = models.EmailField(max_length=254, default="email")
    password = models.CharField(max_length=100, default="password")
    poste = models.CharField(max_length=100, default="poste")
    
    def __str__(self):
        return self.username
    
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
    



    
    
