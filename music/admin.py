from django.contrib import admin
from .models import Artist, Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date', 'created_at']
    list_filter = ['artist', 'release_date']
    search_fields = ['title', 'artist__name']