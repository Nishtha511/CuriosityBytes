from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from .youtube_api import fetch_education_shorts

def home(request):
    return render(request, 'home.html')

def get_education_shorts(request):
    subject = request.GET.get('subject', 'science')
    videos = fetch_education_shorts(subject)  # Call the function from youtube_api.py
    return JsonResponse(videos, safe=False)

