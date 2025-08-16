'use client';

import { useState } from 'react';
import DataOverview from '@/components/DataOverview';
import FilmsGrid from '@/components/FilmsGrid';
import ActorsGrid from '@/components/ActorsGrid';
import PublicationsGrid from '@/components/PublicationsGrid';

export default function DataPage() {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview', component: DataOverview },
    { id: 'films', label: 'Films (1,000)', component: FilmsGrid },
    { id: 'actors', label: 'Actors (200)', component: ActorsGrid },
    { id: 'publications', label: 'Publications (364K)', component: PublicationsGrid },
  ];

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component || DataOverview;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Tabs */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto">
        <ActiveComponent />
      </div>
    </div>
  );
}