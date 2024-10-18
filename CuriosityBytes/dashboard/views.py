from django.shortcuts import render, redirect

# Create your views here.

from django.http import JsonResponse
# from .youtube_api import fetch_education_shorts

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

def get_education_shorts(request):
    # subject = request.GET.get('subject', 'science')
    # videos = fetch_education_shorts(subject)  # Call the function from youtube_api.py
    # return JsonResponse(videos, safe=False)
    pass

def is_loggedin(request):
    if not request.user.is_authenticated:
        return redirect('login')