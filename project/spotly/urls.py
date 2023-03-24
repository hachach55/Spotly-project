from django.urls import path
from .views import LikedSongsView

urlpatterns = [
    path('liked-songs/', LikedSongsView.as_view()),
]
