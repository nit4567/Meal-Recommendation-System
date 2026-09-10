// ============================================================================
// FILE: src/hooks/useWeeklyPlan.js
// PURPOSE: Custom hook for fetching and generating the AI weekly meal plan
// ============================================================================

import { useState, useEffect } from 'react';
import { weeklyPlanAPI } from '../api/weeklyPlan.api';
import { calculationAPI } from '../api/calculation.api';

export const useWeeklyPlan = () => {
  const [weeklyPlan, setWeeklyPlan] = useState(null);
  const [loading, setLoading]       = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError]           = useState(null);

  const fetchPlan = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await weeklyPlanAPI.getSavedPlan();
      setWeeklyPlan(data);
    } catch (err) {
      // 404 = no plan generated yet, not a real error
      if (err.response?.status === 404) {
        setWeeklyPlan(null);
      } else {
        setError(err.response?.data?.detail || 'Failed to load meal plan');
      }
    } finally {
      setLoading(false);
    }
  };

  const generatePlan = async () => {
    try {
      setGenerating(true);
      setError(null);

      // Step 1: ensure UserCalculation row exists before generating plan
      // /calculate is idempotent — safe to call every time
      await calculationAPI.recalculate();

      // Step 2: generate the weekly plan
      await weeklyPlanAPI.generatePlan();

      // Step 3: fetch and display the saved plan
      await fetchPlan();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate meal plan');
    } finally {
      setGenerating(false);
    }
  };

  useEffect(() => {
    fetchPlan();
  }, []);

  return {
    weeklyPlan,
    loading,
    generating,
    error,
    generatePlan,
    refetch: fetchPlan,
  };
};