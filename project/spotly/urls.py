from django.urls import path
from .views import LikedSongsView, GroupedTracksView

urlpatterns = [
    path('saved-songs/', LikedSongsView.as_view(), name='saved_songs'),
    path('saved-songs/groupby=<str:groupby>/', LikedSongsView.as_view(), name='grouped_saved_songs'),
]
