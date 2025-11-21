// ============================================================================
// FILE: src/api/foodPlan.api.js
// PURPOSE: Handles API requests for user's ICMR food plan
// ============================================================================

import axiosInstance from './axios.config';
import { API_ENDPOINTS } from './endpoints';
const BASE_URL = '/api/food-plan';

export const foodPlanAPI = {
  async getUserFoodPlan() {
    
    const res = await axiosInstance.get(`${API_ENDPOINTS.CALCULATION.FOOD_PLAN}`);
    return res.data.food_plan;
  },
};
