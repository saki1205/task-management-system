from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Unique related_name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Unique related_name
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
