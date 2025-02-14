from django.urls import path, include
from viewflow.flow.viewset import FlowViewSet
from django.urls import path
from .views import HomeView, RegisterView, CustomLoginView, CustomLogoutView, VacationRequestView,RequestUpdateStatusView
from .workflow import LeaveRequestFlow


url_flow = [
    
]

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    #path("validation/", ValidationView.as_view(), name="validation"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    #path("employe/", VacationRequestView.as_view(), name="employe"),
    #path("update_status",RequestUpdateStatusView.as_view(), name="update_status")
    #path('update-status/<int:process_pk>/<int:task_pk>/', RequestUpdateStatusView.as_view(), name='update_status'),
    path("flow/", include(FlowViewSet(LeaveRequestFlow).urls))
    


    
]






