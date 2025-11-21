// ============================================================================
// FILE: src/components/common/ToggleButton.jsx
// PURPOSE: Toggle button for multi-select options
// ============================================================================

import React from 'react';

export const ToggleButton = ({ 
  label, 
  value, 
  isSelected, 
  onClick,
  icon: Icon,
  className = '' 
}) => {
  return (
    <button
      type="button"
      onClick={() => onClick(value)}
      className={`py-3 rounded-xl font-medium capitalize transition-all flex items-center justify-center gap-2 ${
        isSelected
          ? 'bg-purple-500 text-white shadow-lg'
          : 'bg-white/10 text-purple-200 hover:bg-white/20'
      } ${className}`}
    >
      {Icon && <Icon className="w-5 h-5" />}
      {label}
    </button>
  );
};
