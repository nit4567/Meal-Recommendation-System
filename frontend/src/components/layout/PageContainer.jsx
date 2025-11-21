// ============================================================================
// FILE: src/components/layout/PageContainer.jsx
// PURPOSE: Wrapper for page content with consistent styling
// ============================================================================

import React from 'react';

export const PageContainer = ({ 
  children, 
  className = '',
  withNavbar = false 
}) => {
  return (
    <div className={`min-h-screen bg-gray-50 ${className}`}>
      {withNavbar && children}
      {!withNavbar && (
        <div className="relative">
          {children}
        </div>
      )}
    </div>
  );
};
