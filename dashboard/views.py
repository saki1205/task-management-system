from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from tasks.models import Task  # ✅ Import Task modelf
from authentication.models import CustomUser 

User = get_user_model()  # ✅ Get Custom User Model

@login_required
def manager_dashboard(request):
    # Get all tasks with their related assigned_to information
    tasks = Task.objects.select_related('assigned_to').all()
    # Get all employees for the dropdown
    employees = CustomUser.objects.filter(role='employee')
    
    print("Debug - Number of tasks:", tasks.count())  # Debug line
    for task in tasks:
        print(f"Task: {task.name}, Assigned to: {task.assigned_to.get_full_name()}")  # Debug line
    
    context = {
        'tasks': tasks,
        'employees': employees,
        'manager_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'dashboard/manager_dashboard.html', context)

@login_required
def employee_dashboard(request):
    """ Employee can view their assigned tasks """
    if request.user.role != "employee":
        messages.error(request, "Unauthorized Access")
        return redirect('manager_dashboard')

    # Use select_related to fetch both assigned_by and assigned_to in a single query
    tasks = Task.objects.select_related('assigned_by', 'assigned_to').filter(
        assigned_to=request.user
    ).order_by('deadline')  # Order by deadline

    context = {
        'tasks': tasks,
        'employee_name': request.user.get_full_name() or request.user.username,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='Completed').count(),
        'pending_tasks': tasks.filter(status='Pending').count(),
        'in_progress_tasks': tasks.filter(status='In Progress').count(),
    }
    
    return render(request, 'dashboard/employee_dashboard.html', context)
