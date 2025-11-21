
import axiosInstance from './axios.config';
import { API_ENDPOINTS } from './endpoints';

export const profileAPI = {
  /**
   * Create or update user profile
   * @param {Object} profileData - Profile information
   * @returns {Promise} - Created/updated profile with calculation
   */
  createProfile: async (profileData) => {
    const response = await axiosInstance.post(API_ENDPOINTS.PROFILE.CREATE, profileData);
    return response.data;
  },

  /**
   * Get user profile
   * @returns {Promise} - Profile object
   */
  getProfile: async () => {
    const response = await axiosInstance.get(API_ENDPOINTS.PROFILE.GET);
    return response.data;
  },

  /**
   * Update user profile
   * @param {Object} profileData - Updated profile information
   * @returns {Promise} - Updated profile with recalculation
   */
  updateProfile: async (profileData) => {
    const response = await axiosInstance.post(API_ENDPOINTS.PROFILE.UPDATE, profileData);
    return response.data;
  },
};