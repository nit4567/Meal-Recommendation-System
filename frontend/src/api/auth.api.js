
import axiosInstance from './axios.config';
import { API_ENDPOINTS } from './endpoints';

export const authAPI = {
  /**
   * Sign up a new user
   * @param {Object} data - { email, password, first_name, last_name }
   * @returns {Promise} - { access_token, user }
   */
  signup: async (data) => {
    const response = await axiosInstance.post(API_ENDPOINTS.AUTH.SIGNUP, data);
    return response.data;
  },

  /**
   * Login existing user
   * @param {Object} credentials - { email, password }
   * @returns {Promise} - { access_token, user }
   */
  login: async (credentials) => {
    const response = await axiosInstance.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
    return response.data;
  },

  /**
   * Get current logged-in user
   * @returns {Promise} - User object
   */
  getCurrentUser: async () => {
    const response = await axiosInstance.get(API_ENDPOINTS.AUTH.ME);
    return response.data;
  },
};