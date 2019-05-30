from django.urls import path
from . import views

urlpatterns = [
    path('show/<int:user_id>/', views.show),
    path('create/', views.create),
    path('login/', views.login),
    path('all_songs/create/', views.create_song),
    path('all_songs/list/', views.get_songs),
    path('users/songs/add/', views.user_add_song),
]