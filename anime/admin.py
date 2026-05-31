from django.contrib import admin
from .models import Anime, WatchlistItem, AnimeRating


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'genres', 'rating', 'episodes')
    search_fields = ('title', 'genres')


@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'added_at')
    search_fields = ('user__username', 'anime__title')


@admin.register(AnimeRating)
class AnimeRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'score', 'rated_at')
    search_fields = ('user__username', 'anime__title')