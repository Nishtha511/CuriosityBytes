from django.db import models
from django.utils.timezone import now

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
