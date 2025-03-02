"use client";

import { useState, useEffect } from "react";
import axios from "axios";

interface Anime {
  id: number;
  title: string;
  synopsis: string;
  episodes: number;
  score: number;
  image_url: string;
}

export default function Home() {
  const [animes, setAnimes] = useState<Anime[]>([]);
  const [filteredAnimes, setFilteredAnimes] = useState<Anime[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchAnimes();
  }, [page]); // Ne recharge que lors du changement de page

  useEffect(() => {
    if (search.trim() === "") {
      setFilteredAnimes(animes); // Affiche tous les animes si aucun filtre
    } else {
      const filtered = animes.filter((anime) =>
        anime.title.toLowerCase().startsWith(search.toLowerCase())
      );
      setFilteredAnimes(filtered); // Met à jour l'affichage avec les résultats filtrés
    }
  }, [search, animes]); // Se met à jour à chaque changement de recherche ou de données

  const fetchAnimes = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/anime/?page=${page}`);
      setAnimes(response.data.results || []);
      setTotalPages(Math.ceil(response.data.count / 10) || 1);
      setFilteredAnimes(response.data.results || []); // Initialise la liste filtrée
    } catch (error) {
      console.error("Error fetching animes:", error);
      setAnimes([]);
      setFilteredAnimes([]);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/anime/${id}/`);
      fetchAnimes();
    } catch (error) {
      console.error("Error deleting anime:", error);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Search Bar */}
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          placeholder="Search anime..."
          className="flex-1 p-2 border rounded"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Anime List */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {filteredAnimes.length > 0 ? (
          filteredAnimes.map((anime) => (
            <div key={anime.id} className="border p-4 rounded-lg shadow-md">
              <img
                src={anime.image_url}
                alt={anime.title}
                className="w-full h-40 object-cover rounded"
              />
              <h2 className="text-lg font-bold mt-2">{anime.title}</h2>
              <p className="text-sm">{anime.synopsis.slice(0, 100)}...</p>
              <p className="text-sm">Episodes: {anime.episodes}</p>
              <p className="text-sm">Score: {anime.score}</p>
              <button
                onClick={() => handleDelete(anime.id)}
                className="mt-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          ))
        ) : (
          <p className="text-center col-span-3 text-gray-500">No anime found on this page.</p>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-6 flex justify-center gap-4">
          <button
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
            disabled={page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
            disabled={page === totalPages}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
