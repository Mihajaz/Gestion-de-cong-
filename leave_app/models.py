from django.db import models
from viewflow.models import Process
# Create your models here.

#modèle employé
class Employee:
    nom = models.CharField(_(""), max_length=50)
    email = models.EmailField(_(""), max_length=254)
    role = models.CharField(_(""), max_length=50)

#
class LeaveRequest:
    employee = models.ForeignKey("GestionDemande.Employee", verbose_name=_("Employé"), on_delete=models.CASCADE)
    start_date = models.DateField(_(""), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_(""), auto_now=False, auto_now_add=False)
    reason = models.TextField(_(""))
    statut = models.CharField(_(""), max_length=50)
    
class Approval:
    leave_request = models.ForeignKey("gestionConge.LeaveRequest", verbose_name=_(""), on_delete=models.CASCADE)
    responsable = models.CharField(_(""), max_length=50)
    direction = models.CharField(_(""), max_length=50)
    



    
    
