from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import LeaveRequestProcess
from .views import RequestUpdateStatusView,VacationRequestView


class LeaveRequestFlow(Flow):
    process_class = LeaveRequestProcess

    start = (
        flow.Start(
            VacationRequestView,
            ).Permission(
            auto_create=True
        ).Next(this.manager_approval)
    )

    manager_approval = (
        flow.View(
            RequestUpdateStatusView,
            fields=["is_manager_approved"]
        ).Permission(
            auto_create=True
        ).Next(this.director_approval)
    )

    director_approval = (
        flow.View(
            RequestUpdateStatusView,
            fields=["is_director_approved"]
        ).Permission(
            auto_create=True
        ).Next(this.finalization)
    )
    
    finalization=(
        flow.View(
            RequestUpdateStatusView,
            fields=["is_finalized"] 
        ).Permission(
            auto_create=True
        ).Next(this.end)
    )

    end = flow.End()

    def on_process_completed(self, process):
        leave_request = process.get_instance()
        if leave_request.approved_by_manager and leave_request.approved_by_director:
            leave_request.request_status = "Validé"
            leave_request.save()
            self.send_notification(leave_request.employee.user_id, "Votre demande de congé a été validée.")
        else:
            leave_request.request_status = "Refusé"
            leave_request.save()
            self.send_notification(leave_request.employee.user_id, "Votre demande de congé a été refusée.")

    def send_notification(self, user, message):
        # Logic to send notification (e.g., email or notification in app)
        # Example for notification
        print(f"Notification to {user.username}: {message}")
