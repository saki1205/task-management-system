from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from tasks.models import Task
from tasks.forms import TaskForm  # Ensure this is defined in `tasks/forms.py`
from authentication.models import CustomUser  # Add this import
import logging

logger = logging.getLogger(__name__)

# Update the User model reference
User = CustomUser  # Use CustomUser directly instead of get_user_model()

# ---------------- MANAGER TASK MANAGEMENT ----------------
@login_required
def add_task(request):
    if request.method == "POST":
        # Log all POST data for debugging
        print("Debug - Full POST data:", dict(request.POST))
        
        try:
            # Get form data with proper validation
            task_name = request.POST.get('task_name', '').strip()
            task_description = request.POST.get('task_description', '').strip()
            assigned_to_id = request.POST.get('assigned_to', '')
            deadline = request.POST.get('deadline', '')
            priority = request.POST.get('priority', '')
            
            # Validate required fields
            if not task_name:
                messages.error(request, "Task name cannot be empty.")
                return redirect('manager_dashboard')
                
            if not task_description:
                messages.error(request, "Task description cannot be empty.")
                return redirect('manager_dashboard')
                
            if not assigned_to_id:
                messages.error(request, "Please select an employee to assign the task.")
                return redirect('manager_dashboard')
                
            if not deadline:
                messages.error(request, "Deadline is required.")
                return redirect('manager_dashboard')
                
            if not priority:
                messages.error(request, "Priority is required.")
                return redirect('manager_dashboard')

            # Get the employee
            try:
                assigned_to_user = CustomUser.objects.get(id=assigned_to_id)
                print(f"Debug - Found employee: {assigned_to_user.username} (ID: {assigned_to_user.id})")
            except CustomUser.DoesNotExist:
                messages.error(request, f"Employee with ID {assigned_to_id} does not exist.")
                return redirect('manager_dashboard')

            # Create task with explicit values for all required fields
            task = Task(
                name=task_name,
                description=task_description,
                assigned_to=assigned_to_user,
                assigned_by=request.user,
                deadline=deadline,
                priority=priority,
                status="Pending",
                progress_percentage=0
            )
            
            # Save the task and verify data was saved correctly
            task.save()
            
            # Verify the task was created with the correct data
            saved_task = Task.objects.get(id=task.id)
            print(f"Debug - Created task details:")
            print(f"  ID: {saved_task.id}")
            print(f"  Name: {saved_task.name}")
            print(f"  Description: {saved_task.description}")
            print(f"  Assigned To: {saved_task.assigned_to.username} (ID: {saved_task.assigned_to_id})")
            
            messages.success(request, f"Task '{task_name}' successfully assigned to {assigned_to_user.get_full_name() or assigned_to_user.username}!")
            return redirect('manager_dashboard')
            
        except Exception as e:
            print(f"Debug - Error creating task: {str(e)}")
            messages.error(request, f"Error creating task: {str(e)}")
            return redirect('manager_dashboard')

    # Get all employees with role='employee'
    employees = CustomUser.objects.filter(role='employee')
    print(f"Debug - Number of employees found: {employees.count()}")
    
    return render(request, 'tasks/add_task.html', {
        'employees': employees,
    })

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check if user is the manager
    if request.user.role != 'manager':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            description = request.POST.get('update_description')
            deadline = request.POST.get('deadline')
            
            if description:
                task.description = description
            if deadline:
                task.deadline = deadline
            
            task.save()
            
            # Check if deadline is a string or datetime object
            deadline_formatted = task.deadline
            if hasattr(task.deadline, 'strftime'):
                deadline_formatted = task.deadline.strftime('%Y-%m-%d')
            
            return JsonResponse({
                'success': True,
                'message': 'Task updated successfully',
                'description': task.description,
                'deadline': deadline_formatted
            })
        except ValueError as e:
            logger.error(f"Invalid date format for task {task_id}: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': 'Invalid date format'
            }, status=400)
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': str(e)}
            , status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
@require_POST
def delete_task(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        # Optional: Add permission check
        if request.user.role != 'manager':
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        task.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ---------------- EMPLOYEE TASK UPDATES ----------------

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check if the user is authorized to update this task
    if request.user != task.assigned_to:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        status = request.POST.get('status')
        progress_description = request.POST.get('progress_description')
        progress_percentage = request.POST.get('progress_percentage')

        try:
            if status:
                task.status = status
            if progress_description:
                task.progress_description = progress_description
            if progress_percentage:
                task.progress_percentage = int(progress_percentage)

            task.save()
            return JsonResponse({
                'success': True,
                'message': 'Task updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return render(request, 'tasks/update_task_status.html', {'task': task})