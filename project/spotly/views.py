from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import TrackModel
from .serializers import SavedTracksSerializer, GroupedTracksSerializer, PlaylistSerializer
from .utils import *

class LikedSongsView(generics.ListAPIView):
    serializer_class = SavedTracksSerializer
    def get_queryset(self):
        groupby = self.request.query_params.get('groupby', None)
        if groupby in ['artist', 'album']:
            pass

        else:
            saved_tracks = get_all_saved_tracks()
            queryset = TrackModel.objects.filter(id__in=[t.id for t in saved_tracks])
            serializer = SavedTracksSerializer(queryset, many=True)
            return serializer.data


class GroupedTracksView(generics.ListAPIView):
    serializer_class = GroupedTracksSerializer
    def get_queryset(self):
        groupby = self.kwargs.get('groupby', None)
        if groupby in ['artist', 'album']:
            if groupby == 'artist':
                grouped_tracks = get_saved_tracks_grouped_by_artist()
                grouped_tracks = dict(sorted(grouped_tracks.items(), key=lambda x: len(x[1]), reverse=True))

            elif groupby == 'album':
                grouped_tracks = get_saved_tracks_grouped_by_album()
                grouped_tracks = dict(sorted(grouped_tracks.items(), key=lambda x: len(x[1]), reverse=True))

            queryset = TrackModel.objects.none()
            for _, tracks in grouped_tracks.items():
                queryset |= TrackModel.objects.filter(id__in=[t.id for t in tracks])

            serializer = GroupedTracksSerializer(
                [{'grouping_key': getattr(tracks[0], groupby), 'tracks': tracks} for _, tracks in grouped_tracks.items()], many=True)
            return serializer.data


class PlaylistsView(generics.ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        playlists = get_user_playlists()
        queryset = PlaylistModel.objects.filter(id__in=[t.id for t in playlists])
        serializer = PlaylistSerializer(queryset, many=True)
        return serializer.data

