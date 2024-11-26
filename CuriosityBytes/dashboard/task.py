from googleapiclient.discovery import build
from .models import YouTubeShort
from django.conf import settings

API_KEY = settings.YOUTUBE_API_KEY
ALLOWED_CHANNELS = [
    "UCLA_DiR1FfKNvjuUpBHmylQ",
    "UCK-HHyVCfKYzhxVOJgBt73w",
    "UCBwmMxybNva6P_5VmxjzwqA",
    "UCKWe3mXbIf4KtETT2mvUBdg",
    "UCPAtCitq_7Al95AWv5yMAwg",
]

def fetch_shorts_for_channel(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,  # Restrict results to the channel
        type='video',
        videoDuration='short',  # Only fetch shorts
        maxResults=10
    )
    response = request.execute()
    return response.get('items', [])

def fetch_and_store_shorts():
    for channel_id in ALLOWED_CHANNELS:
        videos = fetch_shorts_for_channel(channel_id)
        print(videos)
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
                    'published_at': published_at,
                }
            )
    return {"status": "Success", "message": "Shorts fetched and stored successfully"}
