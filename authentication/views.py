from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.middleware.csrf import get_token  # Ensure CSRF token is generated
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                print("Session data after login:", request.session)  # Debugging line to log session data

                # Redirect based on role
                if user.role == "manager":
                    return redirect('manager_dashboard')
                elif user.role == "employee":
                    return redirect('employee_dashboard')
                else:
                    messages.error(request, "Role not set for this user.")
                    return redirect('login')
            else:
                messages.error(request, 'Invalid credentials')

        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
            messages.error(request, 'Invalid form submission')

    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout