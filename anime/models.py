from django.db import models
from django.contrib.auth.models import User


class Anime(models.Model):
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=300, blank=True)
    rating = models.FloatField(default=0)
    episodes = models.IntegerField(default=0)
    synopsis = models.TextField(blank=True)

    def __str__(self):
        return self.title


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} - {self.anime.title}"


class AnimeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    score = models.IntegerField(default=3)
    rated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} rated {self.anime.title}: {self.score}/5"