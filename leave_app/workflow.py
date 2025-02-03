from viewflow import flow, frontend
from viewflow.base import Flow, this
from django.views.generic import FormView
from .models import Leaverequest

#Demande de congé par l'employé 
class LeaveRequestFlow(Flow):
    process_class = LeaveRequest
    #soumission de demande de congé par l'employé
    start = (
        flow.start(
            FormView,
            fields = ["start_date","end_date","reason"]
            template_name="leave_app/validation.html",#template html que je dois creer plus tard 
    
        )
        .permission(auto_create = True)
        .Next(this.approve_by_manager)
    )
    
    #Validation par le responsable
    approve_by_manager = (
        flow.HandleApproved()
        .Assign(username="manager")
        .Next(this.approve_by_director)
           
    )
    
    #Validation par le directeur
    approve_by_director = (
        flow.HandleApproved()
        .Assign(username="director")
        .Next(this.end)
        
    )
    
    end = flow.End()
    
    
    
    

