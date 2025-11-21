// ============================================================================
// FILE: src/components/dashboard/CalorieCard.jsx
// PURPOSE: Display daily calorie target card
// ============================================================================

import React from 'react';
import { Target } from 'lucide-react';
import { getPAL } from '../../utils/icmr.calculations';
import { roundNumber } from '../../utils/formatters';

export const CalorieCard = ({ dailyCalories, bmr, tee, activityLevel }) => {
  return (
    <div className="mb-8 bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl shadow-md border-2 border-purple-200 p-8 text-center">
      <Target className="w-16 h-16 text-purple-600 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-gray-700 mb-2">Your Daily Calorie Target</h3>
      <p className="text-6xl font-bold text-gray-900 mb-4">{Math.round(dailyCalories)}</p>
      <p className="text-gray-600 font-medium">kcal per day</p>
      
      <div className="mt-6 grid grid-cols-3 gap-4 text-sm">
        <div className="bg-white rounded-xl p-4 border border-gray-200">
          <p className="text-gray-600">BMR</p>
          <p className="text-2xl font-bold text-gray-900">{Math.round(bmr)}</p>
          <p className="text-xs text-gray-500">Base Metabolism</p>
        </div>
        <div className="bg-white rounded-xl p-4 border border-gray-200">
          <p className="text-gray-600">TEE</p>
          <p className="text-2xl font-bold text-gray-900">{Math.round(tee)}</p>
          <p className="text-xs text-gray-500">Total Expenditure</p>
        </div>
      </div>
    </div>
  );
  
  
};

