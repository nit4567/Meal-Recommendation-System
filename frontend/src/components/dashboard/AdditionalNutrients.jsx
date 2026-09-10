// ============================================================================
// FILE: src/components/dashboard/AdditionalNutrients.jsx
// PURPOSE: Display additional nutrients (Fiber, Fats, Omega-3/6)
// ============================================================================

import React from 'react';
import { roundNumber } from '../../utils/formatters';

export const AdditionalNutrients = ({ fiber, visibleFat, n6PUFA, n3PUFA, sodium, water }) => {
  return (
    <div className="mb-8">
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Additional Targets</h3>
      <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
            <p className="text-sm text-gray-600 mb-2">Dietary Fiber</p>
            <p className="text-3xl font-bold text-gray-900 mb-1">{roundNumber(fiber)}g</p>
            <p className="text-xs text-gray-500">14g per 1000 kcal</p>
          </div>

          <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
            <p className="text-sm text-gray-600 mb-2">Visible Fat (Oil)</p>
            <p className="text-3xl font-bold text-gray-900 mb-1">{roundNumber(visibleFat)}g</p>
            <p className="text-xs text-gray-500">~{roundNumber(visibleFat / 5)} teaspoons/day</p>
          </div>

          <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
            <p className="text-sm text-gray-600 mb-2">Essential Fatty Acids</p>
            <p className="text-3xl font-bold text-gray-900 mb-1">{n6PUFA}g / {n3PUFA}g</p>
            <p className="text-xs text-gray-500">Omega-6 / Omega-3</p>
          </div>

          {sodium != null && (
            <div className="text-center p-4 bg-orange-50 rounded-xl border border-orange-200">
              <p className="text-sm text-orange-700 mb-2">Sodium Limit</p>
              <p className="text-3xl font-bold text-orange-900 mb-1">{sodium}mg</p>
              <p className="text-xs text-orange-600">DASH protocol target</p>
            </div>
          )}

          {water != null && (
            <div className="text-center p-4 bg-blue-50 rounded-xl border border-blue-200">
              <p className="text-sm text-blue-700 mb-2">Water Intake</p>
              <p className="text-3xl font-bold text-blue-900 mb-1">{water / 1000}L</p>
              <p className="text-xs text-blue-600">Minimum for fiber absorption</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

