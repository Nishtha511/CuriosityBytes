from django.urls import path, include, re_path
from . import views
from .views import custom_404_view

urlpatterns = [
    path('auth/', include('authenticate.urls'), name='authenticate'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blogs, name='blogs'),
    path('', views.home, name='home'),
    re_path(r'^.*$', custom_404_view)
]