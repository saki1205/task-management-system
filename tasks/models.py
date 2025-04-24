from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=False,
        blank=False
    )
    priority = models.CharField(
        max_length=10,
        choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')],
        null=False,
        blank=False
    )
    deadline = models.DateField()
    progress_percentage = models.IntegerField(default=0)
    progress_description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )
    assigned_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.name} - Assigned to {self.assigned_to.get_full_name()}"