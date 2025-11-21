// ============================================================================
// FILE: src/components/common/Card.jsx
// PURPOSE: Reusable card container
// ============================================================================

import React from 'react';

export const Card = ({ 
  children, 
  className = '',
  hover = false,
  ...props 
}) => {
  const hoverClass = hover ? 'hover:scale-105 transition-transform' : '';
  
  return (
    <div 
      className={`bg-white rounded-2xl shadow-md border border-gray-200 p-6 ${hoverClass} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
