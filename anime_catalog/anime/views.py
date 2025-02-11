import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Anime
from .serializers import AnimeSerializer

class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def list(self, request, *args, **kwargs):
        """ Charger automatiquement des animes au démarrage """
        if not Anime.objects.exists():
            self.load_anime_from_jikan()
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Ajouter un anime en le récupérant depuis l'API Jikan """
        title = request.data.get("title")
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f"https://api.jikan.moe/v4/anime?q={title}&limit=1")
        if response.status_code != 200:
            return Response({"error": "Jikan API request failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json().get("data", [])[0]

        anime, created = Anime.objects.get_or_create(
            mal_id=data["mal_id"],
            defaults={
                "title": data["title"],
                "synopsis": data.get("synopsis", ""),
                "episodes": data.get("episodes", 0),
                "score": data.get("score", 0.0),
                "image_url": data["images"]["jpg"]["image_url"],
            },
        )
        serializer = AnimeSerializer(anime)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """ Modifier un anime """
        anime = self.get_object()
        serializer = AnimeSerializer(anime, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Supprimer un anime """
        anime = self.get_object()
        anime.delete()
        return Response({"message": "Anime deleted"}, status=status.HTTP_204_NO_CONTENT)

    def load_anime_from_jikan(self):
        """ Charger des animes populaires au démarrage """
        response = requests.get("https://api.jikan.moe/v4/top/anime")
        if response.status_code == 200:
            anime_list = response.json().get("data", [])
            for data in anime_list[:10]:  # Charger les 10 premiers animes
                Anime.objects.get_or_create(
                    mal_id=data["mal_id"],
                    defaults={
                        "title": data["title"],
                        "synopsis": data.get("synopsis", ""),
                        "episodes": data.get("episodes", 0),
                        "score": data.get("score", 0.0),
                        "image_url": data["images"]["jpg"]["image_url"],
                    },
                )
