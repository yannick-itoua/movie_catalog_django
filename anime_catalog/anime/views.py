import requests
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Anime
from .serializers import AnimeSerializer

from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.decorators import api_view


@api_view(["GET"])
def anime_list(request):
    search = request.GET.get("search", "")
    min_score = request.GET.get("min_score", 0)
    max_episodes = request.GET.get("max_episodes", 1000)
    page = request.GET.get("page", 1)

    animes = Anime.objects.filter(
        Q(title__icontains=search) &
        Q(score__gte=min_score) &
        Q(episodes__lte=max_episodes)
    ).order_by("-score")

    paginator = Paginator(animes, 12)
    paginated_animes = paginator.get_page(page)

    return Response({
        "results": AnimeSerializer(paginated_animes, many=True).data,
        "total_pages": paginator.num_pages,
    })

def fetch_anime_from_anilist(page=1, per_page=50):
    """ Récupère une liste d'animes depuis AniList en paginant """
    
    query = '''
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(type: ANIME) {
          id
          title {
            romaji
            english
          }
          description
          episodes
          averageScore
          coverImage {
            medium
          }
        }
      }
    }
    '''

    variables = {
        "page": page,
        "perPage": per_page
    }

    url = "https://graphql.anilist.co"
    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json().get("data", {}).get("Page", {}).get("media", [])
        animes = []
        for item in data:
            animes.append({
                "mal_id": item["id"],  # On utilise l'ID AniList comme mal_id
                "title": item["title"].get("english") or item["title"].get("romaji"),
                "synopsis": item.get("description", "No description available."),
                "episodes": item.get("episodes", 0),
                "score": item.get("averageScore", 0) / 10,  # Score sur 10
                "image_url": item["coverImage"]["medium"],
            })
        return animes
    return None


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all().order_by("-score")
    serializer_class = AnimeSerializer

    def create(self, request, *args, **kwargs):
        """ Ajouter plusieurs animes en base de données """
        page = request.data.get("page", 1)  # Par défaut, commence à la page 1
        animes_data = fetch_anime_from_anilist(page=page)

        if not animes_data:
            return Response({"error": "No anime found"}, status=404)

        created_animes = []
        for anime_data in animes_data:
            anime, created = Anime.objects.get_or_create(
                mal_id=anime_data["mal_id"],
                defaults=anime_data
            )
            created_animes.append(anime)

        serializer = AnimeSerializer(created_animes, many=True)
        return Response(serializer.data, status=201)
