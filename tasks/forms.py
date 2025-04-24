from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Task

CustomUser = get_user_model()

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # Get the Employee group
        employee_group = Group.objects.filter(name="Employee").first()
        if employee_group:
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(groups=employee_group)

    assigned_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),
        label="Assign to Employee"
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'deadline', 'priority', 'status']

class TaskUpdateForm(forms.ModelForm):
    """ Form for employees to update task status & progress """
    progress_description = forms.CharField(widget=forms.Textarea, required=False, label="Progress Description")
    progress_percentage = forms.IntegerField(min_value=0, max_value=100, required=True, label="Progress (%)")

    class Meta:
        model = Task
        fields = ['status', 'progress_description', 'progress_percentage']
