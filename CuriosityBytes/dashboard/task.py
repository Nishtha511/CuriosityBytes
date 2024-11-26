from googleapiclient.discovery import build
from .models import YouTubeShort
from django.conf import settings

API_KEY = settings.YOUTUBE_API_KEY
<<<<<<< HEAD
ALLOWED_CHANNELS = [
    "UCLA_DiR1FfKNvjuUpBHmylQ",
    "UCK-HHyVCfKYzhxVOJgBt73w",
    "UCBwmMxybNva6P_5VmxjzwqA",
    "UCKWe3mXbIf4KtETT2mvUBdg",
    # "UCPAtCitq_7Al95AWv5yMAwg",
]
=======
TOPICS = ['Science', 'Math', 'History']  # Predefined topics
>>>>>>> 36626852562fa62c7c370639d13c84b13b5dce16

def fetch_shorts_for_topic(topic):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        q=f"{topic} Shorts",
        part='snippet',
        type='video',
        videoDuration='short',
        maxResults=10
    )
    response = request.execute()
    return response.get('items', [])

def fetch_and_store_shorts():
    for topic in TOPICS:
        videos = fetch_shorts_for_topic(topic)
        for video in videos:
            video_id = video['id']['videoId']
            title = video['snippet']['title']
            description = video['snippet']['description']
            channel_id = video['snippet']['channelId']
            thumbnail_url = video['snippet']['thumbnails']['high']['url']
            published_at = video['snippet']['publishedAt']
            
            # Save to the database
            YouTubeShort.objects.update_or_create(
                video_id=video_id,
                defaults={
                    'title': title,
                    'description': description,
                    'channel_id': channel_id,
                    'thumbnail_url': thumbnail_url,
                    'topic': topic,
                    'published_at': published_at,
                }
            )
    return videos
