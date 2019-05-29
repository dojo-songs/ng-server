from django.urls import path
from . import views

urlpatterns = [
    path('show/<int:user_id>/', views.show),
    path('create/', views.create),
    path('login/', views.login),
    path('songs/',views.addSong)
]