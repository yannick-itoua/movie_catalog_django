from django.contrib import admin
from .models import Anime

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'episodes')
    search_fields = ('title',)
    list_filter = ('score',)
