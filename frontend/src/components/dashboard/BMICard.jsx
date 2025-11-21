// ============================================================================
// FILE: src/components/dashboard/BMICard.jsx
// PURPOSE: Display BMI information card
// ============================================================================

import React from 'react';

export const BMICard = ({ bmi, bmiInfo, profile, goalMessage }) => {
  return (
    <div className="mb-8 bg-white rounded-2xl shadow-md border border-gray-200 p-8">
      <div className="flex items-start justify-between mb-6 flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Health Profile</h2>
          <p className="text-gray-600">{goalMessage}</p>
        </div>
        <div className={`px-6 py-3 ${bmiInfo.bg} rounded-2xl border border-gray-200`}>
          <p className="text-sm text-gray-600">BMI</p>
          <p className={`text-3xl font-bold ${bmiInfo.color}`}>{bmi}</p>
          <p className={`text-sm ${bmiInfo.color} font-medium`}>{bmiInfo.category}</p>
        </div>
      </div>
      
      <div className="bg-gray-50 rounded-2xl p-6 border border-gray-200">
        <p className="text-gray-700 mb-4">💡 {bmiInfo.advice}</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Height</p>
            <p className="text-gray-900 font-semibold">{profile.height} cm</p>
          </div>
          <div>
            <p className="text-gray-500">Weight</p>
            <p className="text-gray-900 font-semibold">{profile.weight} kg</p>
          </div>
          <div>
            <p className="text-gray-500">Age</p>
            <p className="text-gray-900 font-semibold">{profile.age} years</p>
          </div>
          <div>
            <p className="text-gray-500">Activity</p>
            <p className="text-gray-900 font-semibold capitalize">{profile.activityLevel}</p>
          </div>
        </div>
      </div>
    </div>
  );
  
};

