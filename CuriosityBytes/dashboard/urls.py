from django.urls import path
from . import views
from .views import watch_history, search_history
# from .youtube_api import get_educational_shorts


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('get_educational_shorts/', get_educational_shorts, name='get_educational_shorts'),
    path('watch-history/', views.watch_history, name='watch_history'),
    path('search-history/', views.search_history, name='search_history'),
    path('news/', views.news, name='news'),
]
