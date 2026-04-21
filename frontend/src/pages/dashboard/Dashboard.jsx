
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useProfile } from '../../hooks/useProfile';
import { useCalculation } from '../../hooks/useCalculation';
import { useFoodPlan } from '../../hooks/useFoodPlan';
import { getBMICategory, getGoalMessage } from '../../utils/icmr.calculations';
import { ROUTES } from '../../constants/routes';
import { Navbar } from '../../components/layout/Navbar';
import { PageContainer } from '../../components/layout/PageContainer';
import { Footer } from '../../components/layout/Footer';
import { Loading } from '../../components/common/Loading';
import { ErrorMessage } from '../../components/common/ErrorMessage';
import {
  BMICard,
  CalorieCard,
  NutrientCard,
  AdditionalNutrients,
  HealthAlert,
  ComingSoon,
  FoodGroupPieChart,
  LunchSuggestion,
} from '@components/dashboard';



export const Dashboard = () => {
  const navigate = useNavigate();
  const { profile, loading: profileLoading, error: profileError } = useProfile();
  const { calculation, loading: calcLoading, error: calcError } = useCalculation();
  const { foodPlan, loading: foodPlanLoading, error: foodPlanError } = useFoodPlan();


  // Redirect to profile creation if no profile found
  React.useEffect(() => {
    // console.log('profileError', profileError);
    if (profileError==="Profile not found") {
      navigate(ROUTES.PROFILE_CREATE);
    }
  }, [profileError, navigate]);

  const loading = profileLoading || calcLoading;
  const error = profileError || calcError;

  if (loading) {
    return (
      <PageContainer>
        <Loading message="Loading your nutrition plan..." />
      </PageContainer>
    );
  }

  if (error || !profile || !calculation) {
    return (
      <PageContainer>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <ErrorMessage 
            message={error || 'Failed to load data'} 
            onRetry={() => window.location.reload()}
          />
        </div>
      </PageContainer>
    );
  }

  const bmiInfo = getBMICategory(calculation.bmi);
  const goalMessage = getGoalMessage(profile.goal);


  return (
    <PageContainer withNavbar>
      {/* <Navbar /> */}

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <BMICard
          bmi={calculation.bmi}
          bmiInfo={bmiInfo}
          profile={profile}
          goalMessage={goalMessage}
        />

        <CalorieCard
          dailyCalories={calculation.daily_calorie_target}
          bmr={calculation.bmr}
          tee={calculation.tee}
          activityLevel={profile.activityLevel}
        />

        {foodPlan && <FoodGroupPieChart foodPlan={foodPlan} />}

        {foodPlan && profile && (
          <LunchSuggestion profile={profile} foodPlan={foodPlan} />
        )}

        <div className="mt-8 mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">Daily Nutrient Targets</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <NutrientCard
              title="Protein"
              value={calculation.protein_target_g}
              unit="g"
              color="blue"
              note={`${profile.dietaryPreference === 'vegetarian' ? '1.0' : '0.83'} g/kg body weight`}
              footnote={
                profile.dietaryPreference === 'vegetarian'
                  ? 'Higher target for cereal-based vegetarian diet'
                  : 'Based on ICMR 2020 RDA guidelines'
              }
            />

            <NutrientCard
              title="Iron"
              value={calculation.iron_target_mg}
              unit="mg"
              color="red"
              note={`${profile.gender === 'male' ? 'Male' : 'Female'} requirement`}
              footnote={
                profile.medicalConditions?.includes('pregnancy')
                  ? 'Increased for pregnancy (35mg)'
                  : 'Essential for oxygen transport'
              }
            />

            <NutrientCard
              title="Calcium"
              value={calculation.calcium_target_mg}
              unit="mg"
              color="purple"
              note="Bone health essential"
              footnote={
                profile.medicalConditions?.includes('pregnancy') ||
                profile.medicalConditions?.includes('lactation')
                  ? 'Increased for pregnancy/lactation'
                  : 'ICMR 2020 adult requirement'
              }
            />
          </div>
        </div>

        <AdditionalNutrients
          fiber={calculation.fiber_target_g}
          visibleFat={calculation.visible_fat_target_g}
          n6PUFA={calculation.n6_pufa_target_g}
          n3PUFA={calculation.n3_pufa_target_g}
        />

        <HealthAlert
          medicalConditions={profile.medicalConditions}
          allergies={profile.allergies}
        />

        <ComingSoon />
      </div>

      {/* <Footer /> */}
    </PageContainer>
  );
};
