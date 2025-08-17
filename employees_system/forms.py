from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from employees_system.models import Employee

User = get_user_model()

class EmployeeForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('analyst', 'Analyst'),
        ('designer', 'Designer'),
    ]
    DESIGNATION_CHOICES = [
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('intern', 'Intern'),
    ]

    def __init__(self, *args, form_fields=None, heading='Employee Information Form', **kwargs):
        super().__init__(*args, **kwargs)
        self.heading = heading
        self.fields['role'].choices = self.ROLE_CHOICES
        self.fields['designation'].choices = self.DESIGNATION_CHOICES
        self.fields['reporting_manager'].queryset = User.objects.all()
        if form_fields:
            for field in form_fields:
                self.fields[field.label.lower().replace(' ', '_')] = self.create_field(field)

    def create_field(self, field):
        field_type = field.field_type
        if field_type == 'select':
            return forms.ChoiceField(
                label=field.label,
                choices=[(opt, opt) for opt in field.options],
                required=field.is_required
            )
        elif field_type == 'textarea':
            return forms.CharField(
                label=field.label,
                widget=forms.Textarea,
                required=field.is_required
            )
        elif field_type == 'date':
            return forms.DateField(
                label=field.label,
                widget=forms.DateInput(attrs={'type': 'date'}),
                required=field.is_required
            )
        else:
            widget = getattr(forms.widgets, f"{field_type.capitalize()}Input", forms.TextInput)()
            return forms.CharField(
                label=field.label,
                widget=widget,
                required=field.is_required
            )

    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'role', 'designation', 'reporting_manager'
        ]
        widgets = {
            'role': forms.Select(),
            'designation': forms.Select(),
            'reporting_manager': forms.Select(),
            'address': forms.Textarea(),
        }