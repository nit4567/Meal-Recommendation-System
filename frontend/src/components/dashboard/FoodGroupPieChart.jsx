// ============================================================================
// FILE: src/components/dashboard/FoodGroupPieChart.jsx
// PURPOSE: Display user's daily food group distribution (ICMR-based)
// ============================================================================
import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const FoodGroupPieChart = ({ foodPlan }) => {
  if (!foodPlan) return <p className="text-gray-500">No food plan available.</p>;

  // Prepare data for chart
  const data = [
    { name: 'Cereals', value: foodPlan.cereals_g },
    { name: 'Pulses', value: foodPlan.pulses_g },
    { name: 'GLV', value: foodPlan.glv_g },
    { name: 'Vegetables', value: foodPlan.veg_g },
    { name: 'Roots/Tubers', value: foodPlan.roots_tubers_g },
    { name: 'Fruits', value: foodPlan.fruits_g },
    { name: 'Milk/Curd', value: foodPlan.milk_curd_ml },
    { name: 'Fats/Oils', value: foodPlan.fats_oils_g },
  ];

  // Tailwind-friendly muted but distinctive colors
  const COLORS = [
    '#60A5FA', // blue-400
    '#34D399', // green-400
    '#FBBF24', // yellow-400
    '#F87171', // red-400
    '#A78BFA', // purple-400
    '#F472B6', // pink-400
    '#93C5FD', // blue-300
    '#FCD34D', // amber-300
  ];

  const total = data.reduce((sum, d) => sum + d.value, 0);

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-all">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        🍽️ Daily Food Group Distribution
      </h3>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }) =>
                `${name}: ${(percent * 100).toFixed(1)}%`
              }
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip formatter={(val) => `${val} g/ml`} />
            <Legend layout="vertical" align="right" verticalAlign="middle" />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          Total daily intake: <span className="font-semibold">{total.toFixed(0)} g/ml</span>
        </p>
        <p className="text-xs text-gray-500">
          Based on ICMR 2020 food group proportions scaled to your calorie needs.
        </p>
      </div>
    </div>
  );
};
