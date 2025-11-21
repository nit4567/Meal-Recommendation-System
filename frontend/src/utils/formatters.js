// PURPOSE: Data formatting utilities
// ============================================================================

/**
 * Format profile data for API (frontend → backend)
 * @param {Object} profile - Frontend profile format
 * @returns {Object} - Backend profile format
 */
export const formatProfileForAPI = (profile) => {
    return {
      age: parseInt(profile.age),
      gender: profile.gender,
      height_cm: parseFloat(profile.height),
      weight_kg: parseFloat(profile.weight),
      region: profile.region,
      dietary_preference: profile.dietaryPreference,
      activity_level: profile.activityLevel,
      goal: profile.goal,
      medical_conditions: profile.medicalConditions || [],
      allergies: profile.allergies || [],
      mood: profile.mood || null,
    };
  };
  
  /**
   * Format profile data from API (backend → frontend)
   * @param {Object} data - Backend profile format
   * @returns {Object} - Frontend profile format
   */
  export const formatProfileFromAPI = (data) => {
    return {
      age: data.age,
      gender: data.gender,
      height: data.height_cm,
      weight: data.weight_kg,
      region: data.region,
      dietaryPreference: data.dietary_preference,
      activityLevel: data.activity_level,
      goal: data.goal,
      medicalConditions: data.medical_conditions || [],
      allergies: data.allergies || [],
      mood: data.mood,
    };
  };
  
  /**
   * Format number with commas
   * @param {number} num
   * @returns {string}
   */
  export const formatNumber = (num) => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  };
  
  /**
   * Round number to specified decimals
   * @param {number} num
   * @param {number} decimals
   * @returns {number}
   */
  export const roundNumber = (num, decimals = 0) => {
    return Math.round(num * Math.pow(10, decimals)) / Math.pow(10, decimals);
  };
  