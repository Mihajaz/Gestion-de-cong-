from django.urls import path
from . import views


urlpatterns = [
    path('', views.home , name='home'),
    path('validation/', views.validation , name='validation'),
    path('register/', views.register , name='register'),
    path('employe/', views.employe, name = 'employe'),
    path('login/', views.login, name = 'login'),
     path('logout/', views.user_logout, name='logout'),
]  





