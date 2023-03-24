from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SongsLibrary
from .serializers import SavedTracksSerializer
from .utils import get_all_saved_tracks


class LikedSongsView(APIView):

    def get(self, request):
        saved_tracks = get_all_saved_tracks()
        serializer = SavedTracksSerializer(saved_tracks, many=True)
        return Response(serializer.data)
