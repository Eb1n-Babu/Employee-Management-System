from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('analyst', 'Analyst'),
    ]

    DESIGNATION_CHOICES = [
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('director', 'Director'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'border rounded p-2 w-full'
    }))

    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES, widget=forms.Select(attrs={
        'class': 'border rounded p-2 w-full'
    }))

    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'role',
            'designation',
            'reporting_manager'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded p-2 w-full'}),
            'phone': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'address': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 3}),
            'reporting_manager': forms.Select(attrs={'class': 'border rounded p-2 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prevent self-assignment in reporting_manager
        if self.instance and self.instance.pk:
            self.fields['reporting_manager'].queryset = Employee.objects.exclude(pk=self.instance.pk)
        else:
            self.fields['reporting_manager'].queryset = Employee.objects.all()