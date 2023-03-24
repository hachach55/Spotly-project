from rest_framework import serializers
from .models import SongsLibrary


class SavedTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongsLibrary
        fields = ['id', 'title', 'artist', 'added']
