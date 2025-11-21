
/**
 * Calculate BMI
 * @param {number} weight - Weight in kg
 * @param {number} height - Height in cm
 * @returns {number} BMI rounded to 1 decimal
 */
export const calculateBMI = (weight, height) => {
    const heightM = height / 100;
    return parseFloat((weight / (heightM * heightM)).toFixed(1));
  };
  
  /**
   * Get BMI category based on Indian standards
   * @param {number} bmi
   * @returns {Object} - { category, color, bg, advice }
   */
  export const getBMICategory = (bmi) => {
    const bmiNum = parseFloat(bmi);
    
    if (bmiNum < 18.5) {
      return {
        category: 'Underweight',
        color: 'text-blue-400',
        bg: 'bg-blue-500/20',
        advice: 'Consider increasing caloric intake to reach healthy weight',
      };
    }
    
    if (bmiNum < 23) {
      return {
        category: 'Normal',
        color: 'text-green-400',
        bg: 'bg-green-500/20',
        advice: 'Maintain your healthy weight with balanced nutrition',
      };
    }
    
    if (bmiNum < 25) {
      return {
        category: 'Overweight',
        color: 'text-yellow-400',
        bg: 'bg-yellow-500/20',
        advice: 'Focus on gradual weight loss through balanced diet',
      };
    }
    
    return {
      category: 'Obese',
      color: 'text-red-400',
      bg: 'bg-red-500/20',
      advice: 'Consult a healthcare provider for personalized weight management',
    };
  };
  
  /**
   * Get goal message based on user's goal
   * @param {string} goal
   * @returns {string}
   */
  export const getGoalMessage = (goal) => {
    const messages = {
      weight_loss: 'Focus on a calorie deficit with adequate protein',
      weight_gain: 'Increase caloric intake with balanced macros',
      maintenance: 'Maintain current weight with balanced nutrition',
      muscle_gain: 'High protein intake with caloric surplus',
    };
    return messages[goal] || 'Maintain balanced nutrition';
  };
  
  /**
   * Get PAL (Physical Activity Level) value
   * @param {string} activityLevel
   * @returns {number}
   */
  export const getPAL = (activityLevel) => {
    const pals = {
      sedentary: 1.4,
      moderate: 1.8,
      heavy: 2.2,
    };
    return pals[activityLevel] || 1.4;
  };
  
  