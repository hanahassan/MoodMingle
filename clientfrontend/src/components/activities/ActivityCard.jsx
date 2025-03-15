// src/components/activities/ActivityCard.jsx
import React, { useState } from 'react';
import { MapPin, Sun, Heart } from 'lucide-react';
import { useSavedActivities } from '../../context/SavedActivitiesContext';
import ActivityDetailsModal from './ActivityDetailsModal';

const ActivityCard = ({ activity }) => {
  const { title, category, location, weather, description } = activity;
  const { saveActivity, removeActivity, isActivitySaved } = useSavedActivities();
  const isSaved = isActivitySaved(title);
  const [showDetails, setShowDetails] = useState(false);

  const handleSaveToggle = () => {
    if (isSaved) {
      removeActivity(title);
    } else {
      saveActivity(activity);
    }
  };

  const handleViewDetails = () => {
    setShowDetails(true);
  };

  const handleCloseDetails = () => {
    setShowDetails(false);
  };

  return (
    <>
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <div className="p-6">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
              <p className="text-sm text-gray-500">{category}</p>
            </div>
            <button 
              onClick={handleSaveToggle}
              className={`text-gray-400 hover:text-red-500 transition-colors ${
                isSaved ? 'text-red-500' : ''
              }`}
              aria-label={isSaved ? "Remove from saved" : "Save activity"}
            >
              <Heart 
                size={20} 
                fill={isSaved ? "currentColor" : "none"}
              />
            </button>
          </div>
          <div className="mt-4 space-y-2">
            <div className="flex items-center text-sm text-gray-500">
              <MapPin size={16} className="mr-2" />
              {location}
            </div>
            <div className="flex items-center text-sm text-gray-500">
              <Sun size={16} className="mr-2" />
              {weather}
            </div>
            <p className="text-sm text-gray-600 mt-2">{description}</p>
          </div>
          <button 
            className="mt-4 w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors"
            onClick={handleViewDetails}
            aria-label="View activity details"
          >
            View Details
          </button>
        </div>
      </div>

      {/* Activity Details Modal */}
      {showDetails && (
        <ActivityDetailsModal 
          activity={activity} 
          onClose={handleCloseDetails} 
        />
      )}
    </>
  );
};

export default ActivityCard;