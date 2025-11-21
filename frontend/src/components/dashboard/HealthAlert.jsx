// ============================================================================
// FILE: src/components/dashboard/HealthAlert.jsx
// PURPOSE: Display health conditions and allergies alert
// ============================================================================

import React from 'react';

export const HealthAlert = ({ medicalConditions, allergies }) => {
  if ((!medicalConditions || medicalConditions.length === 0) && 
      (!allergies || allergies.length === 0)) {
    return null;
  }

  return (
    <div className="mb-8 bg-yellow-50 rounded-2xl shadow-md border-2 border-yellow-200 p-6">
      <h3 className="text-lg font-semibold text-yellow-900 mb-4">
        ⚠️ Important Health Information
      </h3>
      
      {medicalConditions && medicalConditions.length > 0 && (
        <div className="mb-4">
          <p className="text-sm text-yellow-800 mb-2 font-medium">Medical Conditions:</p>
          <div className="flex flex-wrap gap-2">
            {medicalConditions.map((cond) => (
              <span 
                key={cond} 
                className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-lg text-sm capitalize border border-yellow-300"
              >
                {cond}
              </span>
            ))}
          </div>
          <p className="text-xs text-yellow-700 mt-2">
            💡 Your targets are adjusted for your medical conditions. Consult a healthcare provider for personalized advice.
          </p>
        </div>
      )}
      
      {allergies && allergies.length > 0 && (
        <div>
          <p className="text-sm text-yellow-800 mb-2 font-medium">Allergies:</p>
          <div className="flex flex-wrap gap-2">
            {allergies.map((allergy) => (
              <span 
                key={allergy} 
                className="px-3 py-1 bg-red-50 text-red-700 rounded-lg text-sm capitalize border border-red-200"
              >
                {allergy}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
  
};

