from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('authenticate.urls'), name='authenticate'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
]