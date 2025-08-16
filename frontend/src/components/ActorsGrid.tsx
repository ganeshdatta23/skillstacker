'use client';

import { useState, useEffect } from 'react';
import { dataService } from '@/services/dataService';
import { Actor } from '@/types/film';
import LoadingSpinner from './LoadingSpinner';

function ActorsGrid() {
  const [actors, setActors] = useState<Actor[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchActors = async () => {
      try {
        setLoading(true);
        const data = await dataService.getActors({
          search: search || undefined,
          limit: 200
        });
        setActors(data);
      } catch (err) {
        console.error('Failed to fetch actors:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchActors();
  }, [search]);

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Actors Directory</h1>
        
        <input
          type="text"
          placeholder="Search actors..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
        />

        <p className="text-gray-600">Showing {actors.length} actors</p>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {actors.map((actor) => (
            <div key={actor.actor_id} className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
              <h3 className="font-bold text-lg text-gray-900">
                {actor.first_name} {actor.last_name}
              </h3>
              <p className="text-sm text-gray-500">Actor ID: {actor.actor_id}</p>
            </div>
          ))}
        </div>
      )}

      {!loading && actors.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No actors found matching your search.</p>
        </div>
      )}
    </div>
  );
}

export default ActorsGrid;