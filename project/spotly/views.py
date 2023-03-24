from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import TrackModel
from .serializers import SavedTracksSerializer, GroupedTracksSerializer
from .utils import get_all_saved_tracks, get_saved_tracks_grouped_by_artist, get_saved_tracks_grouped_by_album


class LikedSongsView(generics.ListAPIView):
    serializer_class = SavedTracksSerializer

    def get_queryset(self):
        groupby = self.request.query_params.get('groupby', None)
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
                [{'grouping_key': groupby, 'tracks': tracks} for _, tracks in grouped_tracks.items()], many=True)
            return Response(serializer.data)

        else:
            saved_tracks = get_all_saved_tracks()
            serializer = SavedTracksSerializer(saved_tracks, many=True)
            queryset = TrackModel.objects.filter(id__in=[t.id for t in saved_tracks])
            return queryset


class GroupedTracksView(APIView):
    def get(self, request):
        grouped_tracks = get_saved_tracks_grouped_by_artist()
        grouped_tracks = dict(sorted(grouped_tracks.items(), key=lambda x: len(x[1]), reverse=True))
        # Serialize the grouped tracks
        serializer = GroupedTracksSerializer(
            [{'grouping_key': artist, 'tracks': tracks} for artist, tracks in grouped_tracks.items()], many=True)

        return Response(serializer.data)
