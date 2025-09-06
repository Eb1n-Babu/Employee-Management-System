from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    profile_data = models.JSONField(default=dict)

    def __str__(self):
        return self.username

class FormField(models.Model):
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('select', 'Dropdown'),
        ('date', 'Date'),
    ])
    order = models.IntegerField(default=0)
    is_required = models.BooleanField(default=False)
    options = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Explicit fields
    first_name = models.CharField(max_length=50, default='Unknown')
    last_name = models.CharField(max_length=50, default='Unknown')
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        default='placeholder@example.com'
    )

    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        default='+0000000000'
    )

    address = models.TextField(blank=True)

    # Metadata
    role = models.CharField(max_length=100, default="Not Specified")
    designation = models.CharField(max_length=100, default="Not Specified")
    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)  # For dynamic fields

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.emp_id or 'No ID'})"

    def save(self, *args, **kwargs):
        if not self.emp_id:
            while True:
                new_emp_id = uuid.uuid4().hex[:10]
                if not Employee.objects.filter(emp_id=new_emp_id).exists():
                    self.emp_id = new_emp_id
                    break
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']