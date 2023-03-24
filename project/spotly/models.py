from django.db import models


class SongsLibrary(models.Model):
    id = models.AutoField(primary_key=True)
    # created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    artist = models.CharField(max_length=100, blank=True, default='')
    added = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.title
