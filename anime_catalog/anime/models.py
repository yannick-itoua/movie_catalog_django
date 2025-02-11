from django.db import models

class Anime(models.Model):
    mal_id = models.IntegerField(unique=True)  # MyAnimeList ID
    title = models.CharField(max_length=255)
    synopsis = models.TextField(null=True, blank=True)
    episodes = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
