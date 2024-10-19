from django.db import models

from .models import UserWatchHistory, UserSearchHistory
import sqlite3

def set_user_preference(user_id, subject):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO preferences (user_id, subject) VALUES (?, ?)', (user_id, subject))
    conn.commit()
    conn.close()

def get_user_preference(user_id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT subject FROM preferences WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_user_watch_history(user_id):
    """Fetch the watch history of a user."""
    return UserWatchHistory.objects.filter(user_id=user_id).order_by('-watched_at')

def get_user_search_history(user_id):
    """Fetch the search history of a user."""
    return UserSearchHistory.objects.filter(user_id=user_id).order_by('-searched_at')


class Preference(models.Model):
    user_id = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user_id} prefers {self.subject}"
