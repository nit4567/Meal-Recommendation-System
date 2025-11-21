// PURPOSE: Custom hook for calculation data management
// ============================================================================

import { useState, useEffect } from 'react';
import { calculationAPI } from '../api/calculation.api';

export const useCalculation = () => {
  const [calculation, setCalculation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCalculation = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await calculationAPI.getLatestCalculation();
      setCalculation(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load calculation');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalculation();
  }, []);

  return {
    calculation,
    loading,
    error,
    refetch: fetchCalculation,
  };
};


