from django.shortcuts import render, redirect

# Create your views here.

from django.http import JsonResponse
from .youtube_api import get_educational_shorts
from .models import UserWatchHistory, UserSearchHistory

from .user_preference import get_user_watch_history, get_user_search_history

def watch_history(request):
    user_id = request.GET.get('user_id', 'anonymous')
    history = get_user_watch_history(user_id)

    data = [{'title': item.title, 'video_id': item.video_id, 'watched_at': item.watched_at} for item in history]
    # return JsonResponse({'watch_history': data}, safe=False)
    return render(request, 'watch-history.html', {'watch_history': data})

def search_history(request):
    user_id = request.GET.get('user_id', 'anonymous')
    history = get_user_search_history(user_id)

    data = [{'search_query': item.search_query, 'searched_at': item.searched_at} for item in history]
    # return JsonResponse({'search_history': data}, safe=False)
    return render(request, 'search-history.html', {'search_history': data})
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

# def get_education_shorts(request):
#     # subject = request.GET.get('subject', 'science')
#     # videos = fetch_education_shorts(subject)  # Call the function from youtube_api.py
#     # return JsonResponse(videos, safe=False)
#     pass

def is_loggedin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
def fetch_shorts(request):
    user_id = request.GET.get('user_id', 'anonymous')  
    subject = request.GET.get('subject', 'science')  

    # Log search history
    UserSearchHistory.objects.create(user_id=user_id, search_query=subject)

    shorts = get_educational_shorts(subject)

    if 'error' in shorts:
        return JsonResponse({'error': 'Failed to fetch shorts'}, status=500)

    return JsonResponse({'shorts': shorts}, safe=False)
