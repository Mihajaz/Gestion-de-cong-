from django.urls import path, include
from viewflow.flow.viewset import FlowViewSet
from django.urls import path
from .views import HomeView, ValidationView, RegisterView, CustomLoginView, CustomLogoutView, VacationView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("validation/", ValidationView.as_view(), name="validation"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("employe/", VacationView.as_view(), name="employe"),
]






