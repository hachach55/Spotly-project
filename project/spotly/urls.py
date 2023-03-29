from django.urls import path, re_path
from .views import LikedSongsView, GroupedTracksView, PlaylistsView

urlpatterns = [
    path('saved-songs/', LikedSongsView.as_view(), name='saved_songs'),
    re_path(r'^saved-songs/groupby=(?P<groupby>\w+)/$', GroupedTracksView.as_view(), name='grouped_saved_songs'),
    path('playlists', PlaylistsView.as_view(), name='user_playlists')
]