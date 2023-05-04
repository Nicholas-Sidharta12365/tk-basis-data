from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'auth.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('authentication:index')
#         else:
#             messages.info(request, 'Username atau Password salah!')
#     context = {}
#     return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('authentication:login')

# def register_user(request):
#     form = UserCreationForm()

#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your account has been successfully created!')
#             return redirect('authentication:login')
    
#     context = {'form':form}

#     context = {}

#     return render(request, 'register.html', context)