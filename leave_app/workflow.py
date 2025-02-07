from viewflow import flow
from viewflow.base import Flow, this
from django.views.generic import FormView
from .models import LeaveRequest

# Demande de congé par l'employé
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
        .Next(this.approve_by_manager)
    )

    # Validation par le manageur
    approve_by_manager = (
        flow.HandleApproved()
        .Assign(username="manageur")
        .Next(this.check_manager_approval)
    )

    # Vérification de la validation par le manager
    check_manager_approval = (
        flow.Condition(lambda process: process.leave_request.status == "Validé")
        .Next(this.approve_by_director)  # Si validé par le manager, le directeur peut valider
        .Else(this.reject_leave)  # Sinon, le congé est refusé
    )

    # Validation par le directeur
    approve_by_director = (
        flow.HandleApproved()
        .Assign(username="directeur")
        .Next(this.finalize_leave)
    )

    # Vérification de la validation par le directeur
    finalize_leave = (
        flow.Condition(lambda process: process.leave_request.status == "Validé")
        .Next(this.send_notification)  # Si validé par le directeur, envoi de notification
        .Else(this.reject_leave)  # Si refusé par le directeur, congé refusé
    )

    # Refus du congé (si le manager ou le directeur ne valident pas)
    reject_leave = (
        flow.Action(lambda process: process.leave_request.update(status="Refusé"))
        .Next(this.end)
    )

    # Envoi de la notification
    send_notification = (
        flow.Action(lambda process: process.send_leave_notification())
        .Next(this.end)
    )

    # Fin du processus
    end = flow.End()

    def send_leave_notification(self, process):
        """Envoi la notification à l'employé."""
        leave_request = process.leave_request
        employee = leave_request.employee
        if leave_request.status == "Validé":
            message = f"Votre demande de congé du {leave_request.start_date} au {leave_request.end_date} a été validée."
        else:
            message = f"Votre demande de congé a été refusée."
        # Logique pour envoyer la notification, ici on peut imaginer un email ou autre méthode
        print(f"Notification à {employee.user_id.email}: {message}")
