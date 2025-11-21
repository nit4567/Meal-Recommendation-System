
/**
 * Validate email format
 * @param {string} email
 * @returns {boolean}
 */
export const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };
  
  /**
   * Validate password strength
   * @param {string} password
   * @returns {boolean}
   */
  export const isValidPassword = (password) => {
    return password.length >= 6;
  };
  
  /**
   * Validate required field
   * @param {any} value
   * @returns {boolean}
   */
  export const isRequired = (value) => {
    if (typeof value === 'string') {
      return value.trim().length > 0;
    }
    return value !== null && value !== undefined;
  };
  
  /**
   * Validate number range
   * @param {number} value
   * @param {number} min
   * @param {number} max
   * @returns {boolean}
   */
  export const isInRange = (value, min, max) => {
    const num = parseFloat(value);
    return !isNaN(num) && num >= min && num <= max;
  };