// ============================================================================
// FILE: src/components/dashboard/LunchSuggestion.jsx
// PURPOSE: Display complete regional lunch suggestions based on all food groups
// ============================================================================

import React from 'react';

export const LunchSuggestion = ({ profile, foodPlan }) => {
  if (!profile || !foodPlan) {
    return null;
  }

  // Calculate lunch portions (35% of daily intake for lunch)
  const LUNCH_PERCENTAGE = 0.35;
  const lunchCereals = Math.round(foodPlan.cereals_g * LUNCH_PERCENTAGE);
  const lunchPulses = Math.round(foodPlan.pulses_g * LUNCH_PERCENTAGE);
  const lunchGLV = Math.round(foodPlan.glv_g * LUNCH_PERCENTAGE);
  const lunchVeg = Math.round(foodPlan.veg_g * LUNCH_PERCENTAGE);
  const lunchRootsTubers = Math.round(foodPlan.roots_tubers_g * LUNCH_PERCENTAGE);
  const lunchFruits = Math.round(foodPlan.fruits_g * LUNCH_PERCENTAGE);
  const lunchMilkCurd = Math.round(foodPlan.milk_curd_ml * LUNCH_PERCENTAGE);
  const lunchFatsOils = Math.round(foodPlan.fats_oils_g * LUNCH_PERCENTAGE);

  // Regional meal preferences
  const getRegionalMeal = (region) => {
    const meals = {
      north: {
        cereal: {
          name: 'Roti (Wheat)',
          quantity: `${lunchCereals}g`,
          description: 'Whole wheat roti/chapati (2-3 pieces)',
          icon: '🍞'
        },
        pulses: {
          name: 'Dal',
          quantity: `${lunchPulses}g`,
          description: 'Yellow dal, Moong dal, or Chana dal',
          icon: '🫘'
        },
        glv: {
          name: 'Green Leafy Vegetables',
          quantity: `${lunchGLV}g`,
          description: 'Palak, Methi, or Sarson ka saag',
          icon: '🥬'
        },
        vegetables: {
          name: 'Vegetables',
          quantity: `${lunchVeg}g`,
          examples: ['Aloo Gobi', 'Baingan Bharta', 'Mix Vegetables']
        },
        rootsTubers: {
          name: 'Roots & Tubers',
          quantity: `${lunchRootsTubers}g`,
          description: 'Aloo sabzi, Aloo matar, or Sweet potato',
          icon: '🥔'
        },
        fruits: {
          name: 'Fruits',
          quantity: `${lunchFruits}g`,
          description: 'Seasonal fruits (optional with meal)',
          icon: '🍎'
        },
        milkCurd: {
          name: 'Curd/Raita',
          quantity: `${lunchMilkCurd}ml`,
          description: 'Plain curd, Raita, or Buttermilk',
          icon: '🥛'
        },
        fatsOils: {
          name: 'Fats & Oils',
          quantity: `${lunchFatsOils}g`,
          description: 'Used in cooking (ghee/oil)',
          icon: '🫒'
        },
        regionName: 'North Indian'
      },
      south: {
        cereal: {
          name: 'Rice',
          quantity: `${lunchCereals}g`,
          description: 'Steamed rice or brown rice (1-2 cups)',
          icon: '🍚'
        },
        pulses: {
          name: 'Sambar / Dal',
          quantity: `${lunchPulses}g`,
          description: 'Sambar, Rasam, or Dal curry',
          icon: '🫘'
        },
        glv: {
          name: 'Green Leafy Vegetables',
          quantity: `${lunchGLV}g`,
          description: 'Keerai, Palak, or Drumstick leaves',
          icon: '🥬'
        },
        vegetables: {
          name: 'Vegetables',
          quantity: `${lunchVeg}g`,
          examples: ['Sambar vegetables', 'Avial', 'Porial']
        },
        rootsTubers: {
          name: 'Roots & Tubers',
          quantity: `${lunchRootsTubers}g`,
          description: 'Potato curry, Yam, or Taro',
          icon: '🥔'
        },
        fruits: {
          name: 'Fruits',
          quantity: `${lunchFruits}g`,
          description: 'Seasonal fruits (optional with meal)',
          icon: '🍎'
        },
        milkCurd: {
          name: 'Curd/Buttermilk',
          quantity: `${lunchMilkCurd}ml`,
          description: 'Plain curd, Moru, or Buttermilk',
          icon: '🥛'
        },
        fatsOils: {
          name: 'Fats & Oils',
          quantity: `${lunchFatsOils}g`,
          description: 'Used in cooking (coconut oil/ghee)',
          icon: '🫒'
        },
        regionName: 'South Indian'
      },
      east: {
        cereal: {
          name: 'Rice',
          quantity: `${lunchCereals}g`,
          description: 'Steamed rice or gobindobhog rice (1-2 cups)',
          icon: '🍚'
        },
        pulses: {
          name: 'Dal',
          quantity: `${lunchPulses}g`,
          description: 'Masoor dal, Moong dal, or Cholar dal (Bengali style)',
          icon: '🫘'
        },
        glv: {
          name: 'Green Leafy Vegetables / Saag',
          quantity: `${lunchGLV}g`,
          description: 'Lau saag, Palak, or Note saag (amaranth)',
          icon: '🥬'
        },
        vegetables: {
          name: 'Vegetables',
          quantity: `${lunchVeg}g`,
          examples: ['Shukto (mixed vegetables)', 'Labra', 'Begun bhaja (eggplant)', 'Aloo posto']
        },
        rootsTubers: {
          name: 'Roots & Tubers',
          quantity: `${lunchRootsTubers}g`,
          description: 'Aloo (potato), Alu dom, or Fulkopi (cauliflower)',
          icon: '🥔'
        },
        fruits: {
          name: 'Fruits',
          quantity: `${lunchFruits}g`,
          description: 'Seasonal fruits (post-meal)',
          icon: '🍎'
        },
        milkCurd: {
          name: 'Doi (Curd)',
          quantity: `${lunchMilkCurd}ml`,
          description: 'Sweet doi, Mishti doi, or plain curd',
          icon: '🥛'
        },
        fatsOils: {
          name: 'Fats & Oils',
          quantity: `${lunchFatsOils}g`,
          description: 'Used in cooking (mustard oil preferred)',
          icon: '🫒'
        },
        regionName: 'East Indian (Bengali/Odia)'
      },
      
      west: {
        // Option 1: Make it Gujarat-specific
        cereal: {
          name: 'Rotli / Rice',
          quantity: `${lunchCereals}g`,
          description: 'Bajra rotli, wheat rotli, or rice/khichdi',
          icon: '🍞'
        },
        pulses: {
          name: 'Dal / Kadhi',
          quantity: `${lunchPulses}g`,
          description: 'Gujarati dal (sweet), Kadhi, or Toor dal',
          icon: '🫘'
        },
        glv: {
          name: 'Green Leafy Vegetables',
          quantity: `${lunchGLV}g`,
          description: 'Methi, Palak, or Suva bhaji',
          icon: '🥬'
        },
        vegetables: {
          name: 'Shaak / Sabzi',
          quantity: `${lunchVeg}g`,
          examples: ['Undhiyu', 'Ringan nu shaak (eggplant)', 'Sev tameta', 'Bhinda (okra)']
        },
        rootsTubers: {
          name: 'Roots & Tubers',
          quantity: `${lunchRootsTubers}g`,
          description: 'Bateta (potato), Suran, or Sweet potato',
          icon: '🥔'
        },
        fruits: {
          name: 'Fruits',
          quantity: `${lunchFruits}g`,
          description: 'Seasonal fruits (often served)',
          icon: '🍎'
        },
        milkCurd: {
          name: 'Dahi / Chaas',
          quantity: `${lunchMilkCurd}ml`,
          description: 'Dahi, Raita, or spiced Chaas (buttermilk)',
          icon: '🥛'
        },
        fatsOils: {
          name: 'Fats & Oils',
          quantity: `${lunchFatsOils}g`,
          description: 'Used in cooking (groundnut oil/ghee)',
          icon: '🫒'
        },
        regionName: 'West Indian (Gujarati/Maharashtrian)'
      }
    
    };

    return meals[region] || meals.north; // Default to north if region not found
  };

  const meal = getRegionalMeal(profile.region);

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all mt-8">
      <div className="flex items-center gap-3 mb-6">
        <span className="text-3xl">🍽️</span>
        <div>
          <h3 className="text-xl font-semibold text-gray-900">
            Complete Lunch Suggestion
          </h3>
          <p className="text-sm text-gray-600">
            {meal.regionName} style meal (35% of daily intake)
          </p>
        </div>
      </div>

      {/* Main Components Grid */}
      <div className="grid md:grid-cols-2 gap-4 mb-4">
        {/* Cereal Section */}
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.cereal.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.cereal.name}</h4>
              <p className="text-xs text-gray-600">{meal.cereal.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-amber-700">{meal.cereal.quantity}</span>
          </p>
        </div>

        {/* Pulses Section */}
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4 border border-green-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.pulses.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.pulses.name}</h4>
              <p className="text-xs text-gray-600">{meal.pulses.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-green-700">{meal.pulses.quantity}</span>
          </p>
        </div>

        {/* GLV Section */}
        <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-4 border border-emerald-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.glv.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.glv.name}</h4>
              <p className="text-xs text-gray-600">{meal.glv.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-emerald-700">{meal.glv.quantity}</span>
          </p>
        </div>

        {/* Vegetables Section */}
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">🥗</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.vegetables.name}</h4>
              <p className="text-xs text-gray-600">Examples: {meal.vegetables.examples.join(', ')}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-purple-700">{meal.vegetables.quantity}</span>
          </p>
        </div>

        {/* Roots & Tubers Section */}
        <div className="bg-gradient-to-br from-orange-50 to-amber-50 rounded-xl p-4 border border-orange-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.rootsTubers.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.rootsTubers.name}</h4>
              <p className="text-xs text-gray-600">{meal.rootsTubers.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-orange-700">{meal.rootsTubers.quantity}</span>
          </p>
        </div>

        {/* Milk/Curd Section */}
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-4 border border-blue-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.milkCurd.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.milkCurd.name}</h4>
              <p className="text-xs text-gray-600">{meal.milkCurd.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-blue-700">{meal.milkCurd.quantity}</span>
          </p>
        </div>

        {/* Fruits Section */}
        <div className="bg-gradient-to-br from-pink-50 to-rose-50 rounded-xl p-4 border border-pink-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.fruits.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.fruits.name}</h4>
              <p className="text-xs text-gray-600">{meal.fruits.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-pink-700">{meal.fruits.quantity}</span>
          </p>
        </div>

        {/* Fats & Oils Section */}
        <div className="bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl p-4 border border-yellow-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">{meal.fatsOils.icon}</span>
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 text-sm">{meal.fatsOils.name}</h4>
              <p className="text-xs text-gray-600">{meal.fatsOils.description}</p>
            </div>
          </div>
          <p className="text-xs text-gray-700 mt-2">
            <span className="font-bold text-yellow-700">{meal.fatsOils.quantity}</span>
          </p>
        </div>
      </div>

      {/* Meal Summary */}
      <div className="mt-6 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-4 border border-gray-200">
        <h4 className="font-semibold text-gray-900 mb-2 text-sm">📋 Complete Meal Summary</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
          <div>
            <span className="text-gray-600">Cereals:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.cereal.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">Pulses:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.pulses.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">GLV:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.glv.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">Vegetables:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.vegetables.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">Roots/Tubers:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.rootsTubers.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">Fruits:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.fruits.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">Milk/Curd:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.milkCurd.quantity}</span>
          </div>
          <div>
            <span className="text-gray-600">Fats/Oils:</span>
            <span className="font-semibold text-gray-900 ml-1">{meal.fatsOils.quantity}</span>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          💡 These suggestions are based on your regional preference and daily nutritional targets (35% of daily intake for lunch). 
          Adjust portions based on your appetite and activity level. All food groups are included for a balanced meal.
        </p>
      </div>
    </div>
  );
};

