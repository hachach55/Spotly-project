from rest_framework import serializers
from .models import TrackModel, PlaylistModel


class SavedTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackModel
        fields = ['id', 'title', 'artist', 'album', 'added']


class GroupedTracksSerializer(serializers.Serializer):
    grouping_key = serializers.CharField()
    tracks = SavedTracksSerializer(many=True)


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistModel
        fields = ['id', 'name', 'total_tracks']