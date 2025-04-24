from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login')  # Redirect to login page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  # Task management URLs
    path('auth/', include('authentication.urls')),  # User authentication
    path('', home_redirect, name='home'),  # Default redirect to login
    path('dashboard/', include('dashboard.urls')),  # ✅ Manager & Employee Dashboards
    path('tasks/', include('tasks.urls')),  # ✅ Task management URLs (CRUD)
]
