// ============================================================================
// FILE: src/components/dashboard/WeeklyPlanCard.jsx
// PURPOSE: Display the AI-generated 7-day meal plan with day tabs
// ============================================================================

import React, { useState } from 'react';
import { useWeeklyPlan } from '../../hooks/useWeeklyPlan';

// ── small helpers ────────────────────────────────────────────────────────────

const DAY_LABELS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const MEAL_META = {
  breakfast: { label: 'Breakfast', icon: '🌅', bg: 'from-amber-50 to-orange-50', border: 'border-amber-200', badge: 'bg-amber-100 text-amber-700' },
  lunch:     { label: 'Lunch',     icon: '☀️',  bg: 'from-green-50 to-emerald-50', border: 'border-green-200', badge: 'bg-green-100 text-green-700' },
  dinner:    { label: 'Dinner',    icon: '🌙',  bg: 'from-blue-50 to-indigo-50',   border: 'border-blue-200',  badge: 'bg-blue-100 text-blue-700'  },
};

const NUTRIENT_COLORS = {
  calories:  { label: 'Calories',  unit: 'kcal', color: 'text-orange-600' },
  protein_g: { label: 'Protein',   unit: 'g',    color: 'text-blue-600'   },
  fiber_g:   { label: 'Fiber',     unit: 'g',    color: 'text-green-600'  },
  sodium_mg: { label: 'Sodium',    unit: 'mg',   color: 'text-red-500'    },
  fat_g:     { label: 'Fat',       unit: 'g',    color: 'text-yellow-600' },
};

// ── sub-components ───────────────────────────────────────────────────────────

const MealBlock = ({ type, meal }) => {
  const meta = MEAL_META[type];
  return (
    <div className={`bg-gradient-to-br ${meta.bg} rounded-xl p-4 border ${meta.border}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">{meta.icon}</span>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${meta.badge}`}>
          {meta.label}
        </span>
      </div>
      <p className="font-semibold text-gray-900 text-sm leading-snug mb-2">
        {meal.meal_name}
      </p>
      <div className="flex flex-wrap gap-2 text-xs text-gray-600">
        <span>{meal.calories} kcal</span>
        <span>·</span>
        <span>{meal.protein_g}g protein</span>
        <span>·</span>
        <span>{meal.fiber_g}g fiber</span>
      </div>
    </div>
  );
};

const DailyTotals = ({ totals }) => {
  if (!totals) return null;
  return (
  <div className="mt-4 bg-gray-50 rounded-xl p-4 border border-gray-200">
    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
      Daily Totals
    </p>
    <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
      {Object.entries(NUTRIENT_COLORS).map(([key, meta]) => (
        <div key={key} className="text-center">
          <p className={`text-lg font-bold ${meta.color}`}>
            {totals[key] ?? '—'}
          </p>
          <p className="text-xs text-gray-500">{meta.label}</p>
          <p className="text-xs text-gray-400">{meta.unit}</p>
        </div>
      ))}
    </div>
  </div>
  );
};

const SnackBadges = ({ snacks }) => {
  if (!snacks?.length) return null;
  return (
    <div className="mt-4 flex flex-wrap gap-2 items-center">
      <span className="text-xs text-gray-500 font-medium">🍎 Snacks:</span>
      {snacks.map((s, i) => (
        <span key={i} className="text-xs bg-pink-50 border border-pink-200 text-pink-700 px-2 py-0.5 rounded-full">
          {s}
        </span>
      ))}
    </div>
  );
};

const EmptyState = ({ generating, onGenerate }) => (
  <div className="text-center py-12">
    <span className="text-5xl mb-4 block">🍽️</span>
    <h4 className="text-lg font-semibold text-gray-900 mb-2">No Meal Plan Yet</h4>
    <p className="text-sm text-gray-500 mb-6 max-w-xs mx-auto">
      Generate your personalised 7-day plan based on your health profile and medical conditions.
    </p>
    <button
      onClick={onGenerate}
      disabled={generating}
      className="inline-flex items-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-60 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
    >
      {generating ? (
        <>
          <span className="animate-spin">⏳</span> Generating…
        </>
      ) : (
        <>✨ Generate My Plan</>
      )}
    </button>
  </div>
);

// ── main component ───────────────────────────────────────────────────────────

export const WeeklyPlanCard = () => {
  const { weeklyPlan, loading, generating, error, generatePlan } = useWeeklyPlan();
  const [activeDay, setActiveDay] = useState(0); // 0-indexed

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 mt-8">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3" />
          <div className="h-4 bg-gray-100 rounded w-1/2" />
          <div className="grid grid-cols-3 gap-4 mt-4">
            {[1,2,3].map(i => <div key={i} className="h-28 bg-gray-100 rounded-xl" />)}
          </div>
        </div>
      </div>
    );
  }

  // Build ordered days array from plan object
  const days = weeklyPlan?.plan
    ? Object.entries(weeklyPlan.plan)
        .filter(([k]) => k.startsWith('day_'))
        .sort(([a], [b]) => Number(a.split('_')[1]) - Number(b.split('_')[1]))
    : [];

  const currentDay = days[activeDay]?.[1];

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 mt-8 hover:shadow-lg transition-all">
      {/* Header */}
      <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
        <div className="flex items-center gap-3">
          <span className="text-3xl">📅</span>
          <div>
            <h3 className="text-xl font-semibold text-gray-900">Your 7-Day Meal Plan</h3>
            {weeklyPlan?.conditions_applied?.length > 0 && (
              <p className="text-sm text-gray-500">
                Personalised for: {weeklyPlan.conditions_applied.join(', ')}
              </p>
            )}
          </div>
        </div>

        {/* Regenerate button — only shown when plan exists */}
        {weeklyPlan && (
          <button
            onClick={generatePlan}
            disabled={generating}
            className="text-sm text-purple-600 hover:text-purple-800 border border-purple-200 hover:border-purple-400 px-4 py-1.5 rounded-lg transition-colors disabled:opacity-50"
          >
            {generating ? '⏳ Regenerating…' : '🔄 Regenerate'}
          </button>
        )}
      </div>

      {error && (
        <p className="text-sm text-red-500 mb-4">⚠️ {error}</p>
      )}

      {/* Empty state */}
      {!weeklyPlan && (
        <EmptyState generating={generating} onGenerate={generatePlan} />
      )}

      {/* Plan view */}
      {weeklyPlan && days.length > 0 && (
        <>
          {/* Day tabs */}
          <div className="flex gap-2 overflow-x-auto pb-2 mb-6">
            {days.map(([dayKey], idx) => {
              const label = DAY_LABELS[idx] ?? `Day ${idx + 1}`;
              const isActive = idx === activeDay;
              return (
                <button
                  key={dayKey}
                  onClick={() => setActiveDay(idx)}
                  className={`flex-shrink-0 px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-purple-600 text-white shadow-sm'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {label}
                </button>
              );
            })}
          </div>

          {/* Meals grid */}
          {currentDay && (
            <>
              <div className="grid md:grid-cols-3 gap-4">
                <MealBlock type="breakfast" meal={currentDay.breakfast} />
                <MealBlock type="lunch"     meal={currentDay.lunch}     />
                <MealBlock type="dinner"    meal={currentDay.dinner}    />
              </div>

              <DailyTotals totals={currentDay.daily_totals} />

              <SnackBadges snacks={weeklyPlan?.plan?.daily_snacks} />
            </>
          )}

          {/* Footer */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-400">
              💡 Plan generated using ICMR food group guidelines with ingredient-level medical filtering.
              {weeklyPlan.generated_at && (
                <> Last updated: {new Date(weeklyPlan.generated_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</>
              )}
            </p>
          </div>
        </>
      )}
    </div>
  );
};