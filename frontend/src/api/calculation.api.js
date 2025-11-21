import axiosInstance from './axios.config';
import { API_ENDPOINTS } from './endpoints';

export const calculationAPI = {
  /**
   * Get latest calculation
   * @returns {Promise} - Latest calculation object
   */
  getLatestCalculation: async () => {
    const response = await axiosInstance.get(API_ENDPOINTS.CALCULATION.LATEST);
    return response.data;
  },

  /**
   * Get calculation history
   * @param {number} limit - Number of records to fetch (default: 10)
   * @returns {Promise} - Array of calculation objects
   */
  getCalculationHistory: async (limit = 10) => {
    const response = await axiosInstance.get(
      `${API_ENDPOINTS.CALCULATION.HISTORY}?limit=${limit}`
    );
    return response.data;
  },

  /**
   * Trigger recalculation based on current profile
   * @returns {Promise} - New calculation object
   */
  recalculate: async () => {
    const response = await axiosInstance.post(API_ENDPOINTS.CALCULATION.RECALCULATE);
    return response.data;
  },
};