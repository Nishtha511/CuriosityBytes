from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('education_shorts/', views.get_education_shorts, name='get_education_shorts'),
]