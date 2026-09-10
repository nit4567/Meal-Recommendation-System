// ============================================================================
// FILE: src/api/weeklyPlan.api.js
// PURPOSE: API calls for AI weekly meal plan
// ============================================================================

import axiosInstance from './axios.config';
import { API_ENDPOINTS } from './endpoints';

export const weeklyPlanAPI = {
  getSavedPlan: async () => {
    const response = await axiosInstance.get(API_ENDPOINTS.WEEKLY_PLAN.GET);
    return response.data;
  },

  generatePlan: async () => {
    const response = await axiosInstance.post(API_ENDPOINTS.WEEKLY_PLAN.GENERATE);
    return response.data;
  },
};