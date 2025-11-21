// ============================================================================
// FILE: src/components/common/Loading.jsx
// PURPOSE: Loading spinner component
// ============================================================================

import React from 'react';

export const Loading = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mb-4"></div>
      <p className="text-gray-700 text-lg">{message}</p>
    </div>
  );
};
