from django.db import models
from django.contrib.auth.models import AbstractUser
import jsonfield


# Create your models here.

class User(AbstractUser):
    profile_data = jsonfield.JSONField(default=dict)

class FormField(models.Model):
    label = models.CharField(max_length=255)
    input_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'), ('number', 'Number'), ('date', 'Date'), ('password', 'Password')
    ])
    order = models.IntegerField(default=0)

class Employee(models.Model):
    data = jsonfield.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)