from django.db import models
from viewflow.models import Process
# Create your models here.

#modèle employé
class Employee(models.Model):
    nom = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=50)

#
class LeaveRequest(models.Model):
    employee = models.ForeignKey('Employee', verbose_name="Employé", on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.TextField()
    statut = models.CharField(max_length=50)
    
class Approval(models.Model):
    leave_request = models.ForeignKey('LeaveRequest', verbose_name=("Demande de congé"), on_delete=models.CASCADE)
    responsable = models.CharField(max_length=50)
    direction = models.CharField(max_length=50)
    



    
    
