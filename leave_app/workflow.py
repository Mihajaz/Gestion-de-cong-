from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .views import LeaveRequest


class LeaveRequestFlow(Flow):
    process_class = LeaveRequest

    start = (
        flow.Start(
            CreateProcessView,
            fields=[""]
        ).Permission(
            auto_create=True
        ).Next(this.manager_approval)
    )

    manager_approval = (
        flow.View( 
            
        ).Permission(
            auto_create=True
        ).Next(this.directeur_approval)
    )

    director_approval = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.end)
      
    )
    
    end = flow.End()

        