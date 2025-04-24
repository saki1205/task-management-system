# Task Management System

A Django-based task management system with role-based access control for managers and employees.

## Demo Credentials

### Managers
1. **Rahul Sharma**
   - Username: rahul_sharma
   - Password: managerpass
   - Role: Manager

2. **Priya Verma**
   - Username: priya_verma
   - Password: managerpass
   - Role: Manager

3. **Arjun Mehta**
   - Username: arjun_mehta
   - Password: managerpass
   - Role: Manager

### Employees
1. **Rohit Kumar**
   - Username: rohit_kumar
   - Password: employeepass
   - Role: Employee

2. **Neha Rana**
   - Username: neha_rana
   - Password: employeepass
   - Role: Employee

3. **Amit Patel**
   - Username: amit_patel
   - Password: employeepass
   - Role: Employee

## Creating Test Users

Run the following management command to create test users:

```python
from authentication.models import CustomUser

# Create Managers
managers = [
    {
        'username': 'rahul_sharma',
        'password': 'managerpass',
        'first_name': 'Rahul',
        'last_name': 'Sharma',
        'role': 'manager'
    },
    {
        'username': 'priya_verma',
        'password': 'managerpass',
        'first_name': 'Priya',
        'last_name': 'Verma',
        'role': 'manager'
    },
    {
        'username': 'arjun_mehta',
        'password': 'managerpass',
        'first_name': 'Arjun',
        'last_name': 'Mehta',
        'role': 'manager'
    }
]

# Create Employees
employees = [
    {
        'username': 'rohit_kumar',
        'password': 'employeepass',
        'first_name': 'Rohit',
        'last_name': 'Kumar',
        'role': 'employee'
    },
    {
        'username': 'neha_rana',
        'password': 'employeepass',
        'first_name': 'Neha',
        'last_name': 'Rana',
        'role': 'employee'
    },
    {
        'username': 'amit_patel',
        'password': 'employeepass',
        'first_name': 'Amit',
        'last_name': 'Patel',
        'role': 'employee'
    }
]

# Create users
for manager in managers:
    CustomUser.objects.create_user(**manager)

for employee in employees:
    CustomUser.objects.create_user(**employee)

print("Test users created successfully!")