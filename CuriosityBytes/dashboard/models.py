from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User  # Use the Django User model
class UserWatchHistory(models.Model):
    user_id = models.CharField(max_length=100)  # Identify user
    video_id = models.CharField(max_length=50)  # YouTube video ID
    title = models.CharField(max_length=255)  # Video title
    watched_at = models.DateTimeField(default=now)  # Timestamp of when watched

    def __str__(self):
        return f"{self.user_id} watched {self.title} on {self.watched_at}"

class UserSearchHistory(models.Model):
    user_id = models.CharField(max_length=100)  # Identify user
    search_query = models.CharField(max_length=255)  # Search query entered
    searched_at = models.DateTimeField(default=now)  # Timestamp of search

    def __str__(self):
        return f"{self.user_id} searched '{self.search_query}' on {self.searched_at}"


class YouTubeShort(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    channel_id = models.CharField(max_length=255)
    thumbnail_url = models.URLField()
    topic = models.CharField(max_length=50)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_history")
    video = models.ForeignKey(YouTubeShort, on_delete=models.CASCADE, related_name="watched_by")
    watched_at = models.DateTimeField(auto_now_add=True)  # Stores when the video was watched

    def __str__(self):
        return f"{self.user.username} watched {self.video.title}"