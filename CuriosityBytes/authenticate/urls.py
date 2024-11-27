from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.auth_login, name='login'),
    # path('signup/', views.auth_signup, name='signup'),
    path('logout/', views.auth_logout, name='logout'),
]