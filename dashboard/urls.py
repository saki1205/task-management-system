from django.urls import path
from .views import manager_dashboard, employee_dashboard

urlpatterns = [
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
]
