// ============================================================================
// FILE: src/components/common/ErrorMessage.jsx
// PURPOSE: Error message display component
// ============================================================================

import React from 'react';

export const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="p-6 bg-red-50 border border-red-200 rounded-xl">
      <p className="text-red-700 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition-all border border-red-300"
        >
          Try Again
        </button>
      )}
    </div>
  );
};
