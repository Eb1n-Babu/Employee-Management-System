from django.db import models
from django.contrib.auth.models import AbstractUser
import jsonfield
import uuid


# Create your models here.

class User(AbstractUser):
    profile_data = jsonfield.JSONField(default=dict)

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
    options = models.JSONField(null=True, blank=True)  # For dropdown options

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:10])
    data = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )

    def __str__(self):
        return f"{self.data.get('name', 'Unnamed')} ({self.emp_id})"