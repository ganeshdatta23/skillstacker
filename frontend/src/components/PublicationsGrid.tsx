'use client';

import { useState, useEffect } from 'react';
import { dataService } from '@/services/dataService';
import { Publication } from '@/types/film';
import LoadingSpinner from './LoadingSpinner';

function PublicationsGrid() {
  const [publications, setPublications] = useState<Publication[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [pubData, statsData] = await Promise.all([
          dataService.getPublications({ 
            search: search || undefined, 
            limit: 50 
          }),
          dataService.getPublicationStats()
        ]);
        setPublications(pubData.publications || []);
        setStats(statsData);
      } catch (err) {
        console.error('Failed to fetch publications:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [search]);

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Research Publications</h1>
        
        {stats && (
          <div className="bg-blue-50 p-4 rounded-lg mb-4">
            <p className="text-blue-900">
              <strong>{stats.total_publications.toLocaleString()}</strong> total publications available
            </p>
          </div>
        )}

        <input
          type="text"
          placeholder="Search publications..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
        />

        <p className="text-gray-600">Showing {publications.length} publications</p>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {publications.map((pub) => (
            <div key={pub.id || pub._id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <h3 className="font-bold text-lg mb-2 text-gray-900">{pub.title}</h3>
              {pub.content && (
                <p className="text-gray-600 text-sm mb-2">{pub.content}</p>
              )}
              {pub.author && (
                <p className="text-gray-500 text-xs mb-2">By: {pub.author}</p>
              )}
              <div className="flex flex-wrap gap-2 mb-3">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                  {pub.type}
                </span>
                {pub.groups && pub.groups.slice(0, 2).map((group, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                    {group}
                  </span>
                ))}
              </div>
              {pub.subgroups && pub.subgroups.length > 0 && (
                <div className="text-xs text-gray-500">
                  Subgroups: {pub.subgroups.slice(0, 3).join(', ')}
                  {pub.subgroups.length > 3 && '...'}
                </div>
              )}
            </div>
          ))
        </div>
      )}

      {!loading && publications.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No publications found matching your search.</p>
        </div>
      )}
    </div>
  );
}

export default PublicationsGrid;