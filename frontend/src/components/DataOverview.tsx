'use client';

import { useState, useEffect } from 'react';
import { dataService } from '@/services/dataService';
import { DataOverview } from '@/types/film';
import LoadingSpinner from './LoadingSpinner';

function DataOverviewComponent() {
  const [stats, setStats] = useState<any>(null);
  const [films, setFilms] = useState<any[]>([]);
  const [actors, setActors] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [filmStats, actorStats, categoryStats, sampleFilms, sampleActors, allCategories] = await Promise.all([
          dataService.getFilmStats(),
          dataService.getActorStats(),
          dataService.getCategoryStats(),
          dataService.getFilms({ limit: 5 }),
          dataService.getActors({ limit: 5 }),
          dataService.getAllCategories()
        ]);
        setStats({ filmStats, actorStats, categoryStats });
        setFilms(sampleFilms);
        setActors(sampleActors);
        setCategories(allCategories);
      } catch (err) {
        setError('Failed to fetch data overview');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 p-4">{error}</div>;
  if (!stats) return <div className="p-4">No data available</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Data Overview</h1>
      
      {/* Dynamic Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-900">Films</h3>
          <p className="text-2xl font-bold text-blue-600">{stats?.filmStats?.total_films || 'Loading...'}</p>
          <p className="text-sm text-blue-700">Ratings: {Object.keys(stats?.filmStats?.ratings || {}).join(', ')}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-900">Actors</h3>
          <p className="text-2xl font-bold text-green-600">{stats?.actorStats?.total_actors || 'Loading...'}</p>
          <p className="text-sm text-green-700">Sample loaded: {actors.length}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-purple-900">Categories</h3>
          <p className="text-2xl font-bold text-purple-600">{categories.length}</p>
          <p className="text-sm text-purple-700">All categories loaded</p>
        </div>
      </div>

      {/* Dynamic Content from Database */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Latest Films</h2>
          <div className="space-y-3">
            {films.map((film, index) => (
              <div key={film.film_id} className="border-l-4 border-blue-500 pl-4">
                <h3 className="font-semibold text-gray-900">{film.title}</h3>
                <p className="text-sm text-gray-600">{film.description?.substring(0, 100)}...</p>
                <div className="flex gap-2 mt-1">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">{film.rating}</span>
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">${film.rental_rate}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Featured Actors</h2>
          <div className="space-y-3">
            {actors.map((actor) => (
              <div key={actor.actor_id} className="border-l-4 border-green-500 pl-4">
                <h3 className="font-semibold text-gray-900">{actor.first_name} {actor.last_name}</h3>
                <p className="text-sm text-gray-600">Actor ID: {actor.actor_id}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">All Categories</h2>
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <span key={category.category_id} className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">
              {category.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DataOverviewComponent;