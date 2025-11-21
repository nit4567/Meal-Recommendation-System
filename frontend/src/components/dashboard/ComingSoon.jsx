// ============================================================================
// FILE: src/components/dashboard/ComingSoon.jsx
// PURPOSE: Display coming soon features section
// ============================================================================

import React from 'react';

export const ComingSoon = () => {
  const features = [
    'Regional Recipes',
    'Smart Ingredient Filtering',
    'Weekly Meal Plans',
    'Nutrition Tracking',
  ];

  return (
    <div className="mt-8 bg-white rounded-2xl shadow-md border border-gray-200 p-8 text-center">
      <h3 className="text-2xl font-bold text-gray-900 mb-4">🚀 Coming Soon</h3>
      <p className="text-gray-600 mb-4">
        Personalized meal recommendations based on your targets, preferences, and regional cuisine
      </p>
      <div className="flex flex-wrap justify-center gap-3">
        {features.map((feature) => (
          <span 
            key={feature}
            className="px-4 py-2 bg-gray-100 rounded-xl text-sm text-gray-700 border border-gray-300"
          >
            {feature}
          </span>
        ))}
      </div>
    </div>
  );  
  
};

