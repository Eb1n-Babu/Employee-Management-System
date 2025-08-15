from .models import Employee
from django import forms

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['role', 'designation', 'reporting_manager']
        widgets = {
            'role': forms.Select(choices=[
                ('developer', 'Developer'),
                ('manager', 'Manager'),
                ('hr', 'HR'),
                ('analyst', 'Analyst'),
            ]),
            'designation': forms.Select(choices=[
                ('junior', 'Junior'),
                ('senior', 'Senior'),
                ('lead', 'Lead'),
                ('director', 'Director'),
            ]),
            'reporting_manager': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reporting_manager'].queryset = Employee.objects.all()