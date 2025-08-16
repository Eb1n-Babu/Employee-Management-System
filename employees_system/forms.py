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

    def __init__(self, *args, extra_fields=None, heading=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.heading = heading if heading else "Employee Information Form"

        # Prevent self-assignment in reporting_manager
        if self.instance and self.instance.pk:
            self.fields['reporting_manager'].queryset = Employee.objects.exclude(pk=self.instance.pk)
        else:
            self.fields['reporting_manager'].queryset = Employee.objects.all()

        # Add dynamic fields if provided
        if extra_fields:
            for field_name, field_config in extra_fields.items():
                field_type = field_config.get('type', 'text')
                if field_type == 'text':
                    self.fields[field_name] = forms.CharField(
                        label=field_config.get('label', field_name.capitalize()),
                        required=field_config.get('required', False),
                        widget=forms.TextInput(attrs={'class': 'border rounded p-2 w-full'})
                    )
                elif field_type == 'email':
                    self.fields[field_name] = forms.EmailField(
                        label=field_config.get('label', field_name.capitalize()),
                        required=field_config.get('required', False),
                        widget=forms.EmailInput(attrs={'class': 'border rounded p-2 w-full'})
                    )
                elif field_type == 'textarea':
                    self.fields[field_name] = forms.CharField(
                        label=field_config.get('label', field_name.capitalize()),
                        required=field_config.get('required', False),
                        widget=forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 3})
                    )
                elif field_type == 'number':
                    self.fields[field_name] = forms.FloatField(
                        label=field_config.get('label', field_name.capitalize()),
                        required=field_config.get('required', False),
                        widget=forms.NumberInput(attrs={'class': 'border rounded p-2 w-full'})
                    )