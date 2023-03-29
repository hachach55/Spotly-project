from django.db import models


class TrackModel(models.Model):
    id = models.AutoField(primary_key=True)
    # created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    artist = models.CharField(max_length=100, blank=True, default='')
    album = models.CharField(max_length=100, blank=True, default='')
    added = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return str(self.title) + '-' + str(self.artist)


class PlaylistModel(models.Model):
    playlist_id = models.CharField(max_length=100, blank=True, default='')
    name = models.CharField(max_length=100, blank=True, default='')
    total_tracks = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return str(self.name)