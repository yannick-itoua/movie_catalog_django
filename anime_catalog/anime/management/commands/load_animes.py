from django.core.management.base import BaseCommand
import requests
from anime.models import Anime

class Command(BaseCommand):
    help = "Load all anime from AniList API"

    def handle(self, *args, **kwargs):
        url = "https://graphql.anilist.co"
        query = '''
        query ($page: Int, $perPage: Int) {
          Page (page: $page, perPage: $perPage) {
            media (type: ANIME) {
              id
              title {
                romaji
                english
                native
              }
              description
              episodes
              averageScore
              coverImage {
                large
              }
            }
          }
        }
        '''

        page = 1
        total_animes = 0

        while True:
            variables = {"page": page, "perPage": 50}
            response = requests.post(url, json={"query": query, "variables": variables})
            data = response.json()

            if "errors" in data or not data.get("data"):
                self.stdout.write(self.style.ERROR("Erreur lors de la récupération des données."))
                break

            animes_data = data["data"]["Page"]["media"]
            if not animes_data:
                break  # Arrêter s'il n'y a plus d'animes

            for anime_data in animes_data:
                Anime.objects.get_or_create(
                    anilist_id=anime_data["id"],  # ✅ Correction ici
                    defaults={
                        "title": anime_data["title"]["english"] or anime_data["title"]["romaji"],
                        "synopsis": anime_data["description"],
                        "episodes": anime_data["episodes"],
                        "score": anime_data["averageScore"],
                        "image_url": anime_data["coverImage"]["large"],
                    }
                )
                total_animes += 1

            self.stdout.write(f"Page {page} importée ({len(animes_data)} animes)")
            page += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {total_animes} animes importés avec succès !"))
