// ============================================================================
// FILE: src/hooks/useFoodPlan.js
// PURPOSE: Custom hook for fetching and managing user's food plan
// ============================================================================

import { useState, useEffect } from 'react';
import { foodPlanAPI } from '@api/foodPlan.api';

export const useFoodPlan = () => {
  const [foodPlan, setFoodPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchFoodPlan = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await foodPlanAPI.getUserFoodPlan();
      setFoodPlan(data);
    } catch (err) {
      console.error('Food plan fetch error:', err);
      setError(err.response?.data?.detail || 'Failed to load food plan');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFoodPlan();
  }, []);
  

  return {
    foodPlan,
    loading,
    error,
    refetch: fetchFoodPlan,
  };
};
