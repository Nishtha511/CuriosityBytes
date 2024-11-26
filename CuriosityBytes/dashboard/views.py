import requests
# from .youtube_api import get_educational_shorts
# from .models import UserWatchHistory, UserSearchHistory

from .user_preference import get_user_watch_history, get_user_search_history


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import YouTubeShort, WatchHistory
from .task import fetch_and_store_shorts
from django.core.paginator import Paginator
from newsapi import NewsApiClient
import datetime

def news(request):
    newsapi = NewsApiClient(api_key='693a4d6974254e0d901e46d85e304df7')
    articles = {}
    # response = requests.get("https://newsapi.org/v2/top-headlines?country=in&category=education&apiKey=693a4d6974254e0d901e46d85e304df7")
    # if response.status_code == 200:
    #     articles = response.json()['articles']
    articles = newsapi.get_everything(
                                # q='technology OR astrology OR healthcare OR plant-based-eating OR automobile-technology',
                                q='technology',
                                # sources='google-news-in,the-times-of-india',
                                language='en',
                                from_param=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                                to=(datetime.datetime.now()).strftime("%Y-%m-%d"),
                                sort_by='relevancy')['articles']
    
    return render(request, 'news.html', {'articles' : articles})
    # else:
    #     return render(request, 'error.html')

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
    # shorts = fetch_and_store_shorts()
    # return render(request, 'dashboard.html', {'shorts': shorts})
    return render(request, 'dashboard.html')

# def get_education_shorts(request):
#     # subject = request.GET.get('subject', 'science')
#     # videos = fetch_education_shorts(subject)  # Call the function from youtube_api.py
#     # return JsonResponse(videos, safe=False)
#     pass

def is_loggedin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
# def fetch_shorts(request):
#     user_id = request.GET.get('user_id', 'anonymous')  
#     subject = request.GET.get('subject', 'science')  

#     # Log search history
#     UserSearchHistory.objects.create(user_id=user_id, search_query=subject)

#     shorts = get_educational_shorts(subject)

#     if 'error' in shorts:
#         return JsonResponse({'error': 'Failed to fetch shorts'}, status=500)

#     return JsonResponse({'shorts': shorts}, safe=False)






# Fetch YouTube Shorts and store them (manual trigger)
def fetch_shorts_view(request):
    videos = fetch_and_store_shorts()  # Trigger fetching
    return JsonResponse({'status': videos})

# Display the YouTube Shorts
def shorts_list_view(request):
    shorts_list = YouTubeShort.objects.all().order_by('-published_at')
    paginator = Paginator(shorts_list, 10)  # Show 10 shorts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shorts.html', {'page_obj': page_obj})

@login_required  # Ensure only logged-in users can watch videos
def watch_video(request, video_id):
    # Fetch the video by ID
    video = get_object_or_404(YouTubeShort, video_id=video_id)

    # Record the watch history
    WatchHistory.objects.create(user=request.user, video=video)

    # Redirect to the video page or render the video template
    return render(request, 'youtube_shorts/video_detail.html', {'video': video})