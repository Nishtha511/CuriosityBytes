from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def auth_login(request):
    return render(request, 'login.html')

# def auth_signup(request):
#     return render(request, 'signup.html')

def auth_logout(request):
    logout(request)
    return redirect('home')