from django import forms
from django.db.models import Q
from django.shortcuts import render , redirect
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User, FormField, Employee
from django.contrib.auth import authenticate, login, logout
import re
from django.core.exceptions import ValidationError
from .serializers import EmployeeSerializer, FormFieldSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import EmployeeForm
from .models import Employee
import json

# Create your views here.

def Home(request):
    return render(request, 'home.html')

def Welcome(request):
    return render(request, 'welcome.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')  # Redirect to employee_list_view
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        data = request.POST

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'Username already exists'
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email already exists'
            }, status=400)


        if password != confirm_password:
            return JsonResponse({
                'success': False,
                'error': 'Passwords do not match'
            }, status=400)

        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(password_pattern, password):
            return JsonResponse({
                'success': False,
                'error': 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*?&)'
            }, status=400)

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Log in the user
            login(request, user)

            return JsonResponse({
                'success': True,
                'message': 'Registration successful'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return render(request, 'register.html')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        data = request.POST

        # Extract form data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        # Validate old password
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({
                'success': False,
                'error': 'Old password is incorrect'
            }, status=400)

        # Check if new passwords match
        if new_password != confirm_new_password:
            return JsonResponse({
                'success': False,
                'error': 'New passwords do not match'
            }, status=400)

        # Password validation regex
        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(password_pattern, new_password):
            return JsonResponse({
                'success': False,
                'error': 'New password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*?&)'
            }, status=400)

        try:
            user.set_password(new_password)
            user.save()

            return JsonResponse({
                'success': True,
                'message': 'Password changed successfully'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return render(request, 'change_password.html')


@login_required
def profile_view(request):
    ALLOWED_FIELDS = {'first_name', 'last_name', 'email', 'bio', 'phone_number', 'address'}

    if request.method == 'POST':
        try:
            # Get POST data
            data = request.POST.dict()

            # Remove CSRF token from data
            data.pop('csrfmiddlewaretoken', None)

            # Validate input fields
            profile_data = {}
            for key, value in data.items():
                if key not in ALLOWED_FIELDS:
                    return JsonResponse({
                        'success': False,
                        'error': f'Invalid field: {key}'
                    }, status=400)

                # Basic validation for each field
                if key == 'email' and value:
                    # Simple email format validation
                    if '@' not in value or '.' not in value:
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid email format'
                        }, status=400)
                elif key == 'phone_number' and value:
                    # Simple phone number validation (can be enhanced)
                    if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid phone number format'
                        }, status=400)

                # Clean and store the value
                profile_data[key] = value.strip() if value else ''

            # Update user profile
            request.user.profile_data.update(profile_data)

            # Update core user fields if present
            if 'first_name' in profile_data:
                request.user.first_name = profile_data['first_name']
            if 'last_name' in profile_data:
                request.user.last_name = profile_data['last_name']
            if 'email' in profile_data:
                request.user.email = profile_data['email']

            # Save user
            request.user.save()

            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully',
                'updated_fields': list(profile_data.keys())
            })

        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred'
            }, status=500)

    # GET request - render profile form
    context = {
        'profile': request.user.profile_data,
        'user': {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username
        }
    }
    return render(request, 'profile.html', context)


@login_required
def employee_create_view(request, pk=None):
    """
    View to create or update an employee using the standard EmployeeForm.
    Requires user to be logged in.
    """
    employee = get_object_or_404(Employee, pk=pk) if pk else None

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            emp = form.save(commit=False)
            if not pk:  # New employee
                emp.created_by = request.user
            emp.save()
            return JsonResponse({
                'success': True,
                'message': 'Employee saved successfully',
                'employee_id': emp.pk
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

    form = EmployeeForm(instance=employee)
    return render(request, 'employee_create.html', {
        'form': form,
        'employee': employee,
        'form_heading': form.heading
    })


@login_required
def employee_list_view(request):
    employees = Employee.objects.all()
    search = request.GET.get('search')

    if search:
        search = search.lower()
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(role__icontains=search) |
            Q(designation__icontains=search) |
            Q(emp_id__icontains=search) |
            Q(reporting_manager__first_name__icontains=search) |
            Q(reporting_manager__last_name__icontains=search)
        )

    return render(request, 'employee_list.html', {
        'employees': employees,
        'search': search
    })

@login_required
def employee_detail_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

@login_required
def employee_delete_view(request, pk):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def form_design_view(request):
    """
    View to handle dynamic form creation with custom fields and heading.
    GET: Renders the form designer template.
    POST: Saves form data via JSON.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            extra_fields = data.get('extra_fields', {})
            heading = data.get('heading', 'Employee Information Form')
            form_data = data.get('form_data', {})

            form = EmployeeForm(
                data=form_data,
                extra_fields=extra_fields,
                heading=heading
            )

            if form.is_valid():
                employee = form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Employee created successfully',
                    'data': {
                        'id': employee.pk,
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                        'email': employee.email,
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)

    elif request.method == 'GET':
        # Example extra fields for the form designer
        extra_fields = {
        }
        heading = "Custom Employee Form"
        form = EmployeeForm(extra_fields=extra_fields, heading=heading)
        form_fields = [
            {
                'name': field_name,
                'label': field.label,
                'type': field.widget.input_type if hasattr(field.widget, 'input_type') else 'textarea' if isinstance(field.widget, forms.Textarea) else 'select' if isinstance(field.widget, forms.Select) else 'text',
                'required': field.required
            } for field_name, field in form.fields.items()
        ]

        return render(request, 'form_design.html', {
            'form': form,
            'form_heading': form.heading,
            'form_fields': form_fields
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

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
        serializer = EmployeeSerializer(employee, data={'data': request.data}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    def delete(self, request, pk):
        Employee.objects.get(pk=pk).delete()
        return Response(status=204)

class UserAPI(APIView):
    def post(self, request):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', request.data['password']):
            return Response({'error': 'Password must be 8+ chars with 1 uppercase and 1 number'}, status=400)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        return Response(serializer.errors, status=400)