"use client";
import { useEffect, useState } from "react";
import AnimeCard from "./AnimeCard";
import { api } from "@/utils/api";

interface Anime {
  id: number;
  title: string;
  image_url: string;
  score: number;
}

export default function AnimeList() {
  const [animeList, setAnimeList] = useState<Anime[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/anime/")
      .then(response => setAnimeList(response.data))
      .catch(error => console.error("Failed to fetch anime:", error))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-center">Loading...</p>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {animeList.map(anime => (
        <AnimeCard key={anime.id} title={anime.title} imageUrl={anime.image_url} score={anime.score} />
      ))}
    </div>
  );
}
