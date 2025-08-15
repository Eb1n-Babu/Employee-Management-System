import re
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
        fields = '__all__'

# ems_app/views.py (add API views)
class FormFieldAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        fields = FormField.objects.all().order_by('order')
        return Response(FormFieldSerializer(fields, many=True).data)
    def post(self, request):
        FormField.objects.all().delete()
        for idx, field in enumerate(request.data):
            field['order'] = idx
            FormFieldSerializer(data=field).is_valid(raise_exception=True)
            FormField.objects.create(**field)
        return Response({'success': True})

class EmployeeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            return Response(EmployeeSerializer(Employee.objects.get(pk=pk)).data)
        employees = Employee.objects.all()
        search = request.query_params.get('search')
        if search:
            employees = [e for e in employees if any(search.lower() in str(v).lower() for v in e.data.values())]
        return Response(EmployeeSerializer(employees, many=True).data)
    def post(self, request):
        serializer = EmployeeSerializer(data={'data': request.data, 'created_by': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    def put(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        employee.data = request.data
        employee.save()
        return Response(EmployeeSerializer(employee).data)
    def delete(self, request, pk):
        Employee.objects.get(pk=pk).delete()
        return Response(status=204)

class UserAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', request.data['password']):
            return Response({'error': 'Password must be 8+ chars with 1 uppercase and 1 number'}, status=400)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        return Response(serializer.errors, status=400)