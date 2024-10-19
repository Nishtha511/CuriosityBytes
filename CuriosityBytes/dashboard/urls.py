from django.urls import path
from . import views
from .views import fetch_shorts, watch_history, search_history
from .youtube_api import get_educational_shorts


urlpatterns = [
    path('', views.home, name='home'),
    path('education_shorts/', youtube_api.get_educational_shorts, name='get_education_shorts'),
    path('watch-history/', views.watch_history, name='watch_history'),
    path('search-history/', views.search_history, name='search_history'),

]