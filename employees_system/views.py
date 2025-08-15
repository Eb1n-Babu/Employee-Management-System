from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import re
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        data = request.POST
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', data['password']):
            return JsonResponse({'success': False, 'error': 'Password must be 8+ chars with 1 uppercase and 1 number'}, status=400)
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        login(request, user)
        return JsonResponse({'success': True})
    return render(request, 'register.html')

def change_password_view(request):
    if request.method == 'POST':
        data = request.POST
        user = request.user
        if not user.check_password(data['old_password']):
            return JsonResponse({'success': False, 'error': 'Old password incorrect'}, status=400)
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', data['new_password']):
            return JsonResponse({'success': False, 'error': 'New password must be 8+ chars with 1 uppercase and 1 number'}, status=400)
        user.set_password(data['new_password'])
        user.save()
        return JsonResponse({'success': True})
    return render(request, 'change_password.html')

def profile_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        request.user.profile_data.update(data)
        request.user.save()
        return JsonResponse({'success': True})
    return render(request, 'profile.html', {'profile': request.user.profile_data})


@csrf_exempt
def form_design_view(request):
    if request.method == 'GET':
        fields = FormField.objects.all().order_by('order')
        return render(request, 'form_design.html', {'fields': fields})
    elif request.method == 'POST':
        data = request.POST.getlist('fields[]')
        FormField.objects.all().delete()
        for idx, field in enumerate(data):
            label, input_type = field.split(',')
            FormField.objects.create(label=label, input_type=input_type, order=idx)
        return JsonResponse({'success': True})