'use client';

import { useState, useEffect } from 'react';
import { dataService } from '@/services/dataService';
import { Film } from '@/types/film';
import LoadingSpinner from './LoadingSpinner';

function FilmsGrid() {
  const [films, setFilms] = useState<Film[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedRating, setSelectedRating] = useState('');

  useEffect(() => {
    const fetchFilms = async () => {
      try {
        setLoading(true);
        const data = await dataService.getFilms({
          search: search || undefined,
          rating: selectedRating || undefined,
          limit: 100
        });
        setFilms(data);
      } catch (err) {
        console.error('Failed to fetch films:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFilms();
  }, [search, selectedRating]);

  const ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17'];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Films Library</h1>
        
        {/* Filters */}
        <div className="flex gap-4 mb-4">
          <input
            type="text"
            placeholder="Search films..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <select
            value={selectedRating}
            onChange={(e) => setSelectedRating(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Ratings</option>
            {ratings.map(rating => (
              <option key={rating} value={rating}>{rating}</option>
            ))}
          </select>
        </div>

        <div className="flex justify-between items-center">
          <p className="text-gray-600">Showing {films.length} films</p>
          <div className="text-sm text-gray-500">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {films.map((film) => (
            <div key={film.film_id} className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
              <h3 className="font-bold text-lg mb-2 text-gray-900">{film.title}</h3>
              <p className="text-gray-600 text-sm mb-3 line-clamp-3">{film.description}</p>
              <div className="flex justify-between items-center text-sm">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {film.rating || 'NR'}
                </span>
                <span className="text-green-600 font-semibold">
                  ${film.rental_rate}
                </span>
              </div>
              <div className="mt-2 text-xs text-gray-500">
                {film.release_year && <span>Year: {film.release_year}</span>}
                {film.length && <span className="ml-2">Length: {film.length}min</span>}
                <div className="mt-1">
                  <span className="bg-gray-100 text-gray-600 px-1 py-0.5 rounded text-xs">ID: {film.film_id}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && films.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No films found matching your criteria.</p>
        </div>
      )}
    </div>
  );
}

export default FilmsGrid;