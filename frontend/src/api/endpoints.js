export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    SIGNUP: '/auth/signup',
    LOGIN:  '/auth/login',
    ME:     '/auth/me',
  },

  // Profile endpoints
  PROFILE: {
    CREATE: '/profile',
    GET:    '/profile',
    UPDATE: '/profile',
  },

  // Calculation endpoints
  CALCULATION: {
    LATEST:      '/calculations/latest',
    HISTORY:     '/calculations/history',
    RECALCULATE: '/calculate',
    FOOD_PLAN:   '/calculations/food-plan',
  },

  // Weekly meal plan endpoints
  WEEKLY_PLAN: {
    GET:      '/calculations/my-weekly-plan',
    GENERATE: '/calculations/generate-ai-plan',
  },
};