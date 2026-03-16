"""
Voices URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_voice_view, name='create_voice'),
    path('list/', views.voice_list_view, name='voice_list'),
    path('delete/<int:voice_id>/', views.delete_voice_view, name='delete_voice'),
    path('download/<int:voice_id>/', views.download_voice_view, name='download_voice'),
    path('profiles/', views.profile_list_view, name='profile_list'),
    path('profiles/create/', views.create_profile_view, name='create_profile'),
]
