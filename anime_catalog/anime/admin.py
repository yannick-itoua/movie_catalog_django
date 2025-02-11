from django.contrib import admin
from .models import Anime

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'episodes')  # Columns in the list view
    search_fields = ('title',)  # Search bar for titles
    list_filter = ('score',)  # Filter by score
