from rest_framework import serializers
from .models import TrackModel, DetailedPlaylistModel, PlaylistModel


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
        fields = ['name', 'total_tracks']


class DetailedPlaylistSerializer(serializers.ModelSerializer):
    tracks = SavedTracksSerializer(many=True)

    class Meta:
        model = DetailedPlaylistModel
        fields = ['name', 'total_tracks', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks', [])
        playlist = super().create(validated_data)
        for track_data in tracks_data:
            TrackModel.objects.create(playlist=playlist, **track_data)
        return playlist

    def update(self, instance, validated_data):
        tracks_data = validated_data.pop('tracks', [])
        playlist = super().update(instance, validated_data)
        playlist.tracks.all().delete()
        for track_data in tracks_data:
            TrackModel.objects.create(playlist=playlist, **track_data)
        return playlist
