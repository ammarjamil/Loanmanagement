from django.urls import path
from . import views

# app_name = 'Authentication'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('loan/request/', views.LoanrequestView.as_view(), name='loan_request'),
    path('loan/process/', views.ProcessLoanrequestView.as_view(), name='process'),


]