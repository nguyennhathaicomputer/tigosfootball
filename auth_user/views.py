import re

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import User
import json
# Create your views here.

# @csrf_exempt
def login_view(request):

    if request.method =='POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        if not username or not password:
            return JsonResponse({'error': 'Missing fields'}, status=400)
        try:

            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        if user.check_password(password):
            authenticate(request, username=username, password=password)
            login(request, user)
            return JsonResponse({'success': True}, status=200)
        
        
    if request.method =='GET':
        return render(request, 'auth/login.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('app:home')

def register(request):

    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            password2 = data.get('password2')
        
        except:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        if not username or not password or not password2:
            return JsonResponse({'error': 'Missing fields'}, status=400)
        if password != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        user = User(username=username)
        user.set_password(password)
        user.save()
        return JsonResponse({'success': True})
    if request.method == 'GET':
        return render(request, 'auth/register.html')