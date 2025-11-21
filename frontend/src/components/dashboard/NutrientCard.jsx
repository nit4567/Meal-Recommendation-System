// ============================================================================
// FILE: src/components/dashboard/NutrientCard.jsx
// PURPOSE: Display individual nutrient card (Protein, Iron, Calcium)
// ============================================================================

import React from 'react';
import { User, Activity, Target } from 'lucide-react';
import { roundNumber } from '../../utils/formatters';

export const NutrientCard = ({ 
  title, 
  value, 
  unit, 
  color = 'blue', 
  note, 
  footnote 
}) => {
  const getColorClasses = () => {
    const colors = {
      blue: { bg: 'bg-blue-500/20', text: 'text-blue-300', icon: 'text-blue-300' },
      red: { bg: 'bg-red-500/20', text: 'text-red-300', icon: 'text-red-300' },
      purple: { bg: 'bg-purple-500/20', text: 'text-purple-300', icon: 'text-purple-300' },
    };
    return colors[color] || colors.blue;
  };

  const getIcon = () => {
    if (title === 'Protein') return User;
    if (title === 'Iron') return Activity;
    return Target;
  };

  const Icon = getIcon();
  const colors = getColorClasses();

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-lg font-semibold text-gray-900">{title}</h4>
        <div className={`w-12 h-12 ${colors.bg} rounded-xl flex items-center justify-center border border-gray-200`}>
          <Icon className={`w-6 h-6 ${colors.icon}`} />
        </div>
      </div>
      <p className={`text-4xl font-bold ${colors.text} mb-2`}>
        {roundNumber(value)}{unit}
      </p>
      <p className={`text-sm text-gray-600`}>
        {note}
      </p>
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          📌 {footnote}
        </p>
      </div>
    </div>
  );
};

