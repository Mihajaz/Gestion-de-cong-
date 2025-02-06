from viewflow import flow, frontend
from viewflow.base import Flow, this
from django.views.generic import FormView
from .models import LeaveRequest

#Demande de congé par l'employé 
class LeaveRequestFlow(Flow):
    process_class = LeaveRequest
    
    # Soumission de la demande de congé par l'employé
    start = (
        flow.start(
            FormView,
            fields=["start_date", "end_date", "reason"],
            template_name="leave_app/validation.html",
        )
        .permission(auto_create=True)
        .Next(this.approve_by_director)
    )
    
    # Validation par le directeur
    approve_by_director = (
        flow.HandleApproved()
        .Assign(username="directeur")
        .Next(this.approve_by_manager)
    )
    
    # Validation par le manageur
    approve_by_manager = (
        flow.HandleApproved()
        .Assign(username="manageur")
        .Next(this.end)
    )

    # Fin du processus
    end = flow.End()

    
    
    

