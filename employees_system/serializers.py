from rest_framework import serializers
from .models import User, FormField, Employee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'emp_id', 'first_name', 'last_name', 'email', 'phone',
            'address', 'role', 'designation', 'reporting_manager',
            'created_by', 'created_at', 'updated_at', 'extra_data'
        ]
        read_only_fields = ['id', 'emp_id', 'created_at', 'updated_at', 'created_by']

    def validate_email(self, value):
        queryset = Employee.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value

    def validate_phone(self, value):
        return value

    def validate_extra_data(self, value):
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("extra_data must be a valid JSON object.")
        return value