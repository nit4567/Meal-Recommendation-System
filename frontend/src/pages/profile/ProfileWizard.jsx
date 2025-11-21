import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { profileAPI } from '../../api/profile.api';
import { formatProfileForAPI } from '../../utils/formatters';
import { ROUTES } from '../../constants/routes';
import {
  GENDER_OPTIONS,
  ACTIVITY_LEVELS,
  DIETARY_PREFERENCES,
  REGIONS,
  GOALS,
  MEDICAL_CONDITIONS,
  ALLERGIES,
  MOODS,
} from '../../constants/options';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Select } from '../../components/common/Select';
import { ToggleButton } from '../../components/common/ToggleButton';
import { ArrowRight, TrendingDown, TrendingUp, Minus, Plus } from 'lucide-react';

export const ProfileWizard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isEditing = location.pathname === ROUTES.PROFILE_EDIT;

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [profile, setProfile] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    activityLevel: '',
    dietaryPreference: '',
    region: '',
    goal: '',
    medicalConditions: [],
    allergies: [],
    mood: '',
  });

  const totalSteps = 3;

  const updateProfile = (field, value) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
    setError('');
  };

  const toggleArrayField = (field, value) => {
    setProfile((prev) => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter((v) => v !== value)
        : [...prev[field], value],
    }));
  };

  const canProceed = () => {
    if (step === 1) {
      return profile.age && profile.gender && profile.height && profile.weight;
    }
    if (step === 2) {
      return profile.activityLevel && profile.dietaryPreference && profile.region;
    }
    return profile.goal;
  };

  const handleNext = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      handleComplete();
    }
  };

  const handleComplete = async () => {
    setLoading(true);
    setError('');

    try {
      const formattedProfile = formatProfileForAPI(profile);
      await profileAPI.createProfile(formattedProfile);
      navigate(ROUTES.DASHBOARD);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save profile');
      setLoading(false);
    }
  };

  const goalIcons = {
    weight_loss: TrendingDown,
    weight_gain: TrendingUp,
    maintenance: Minus,
    muscle_gain: Plus,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4 flex items-center justify-center">
      <div className="w-full max-w-2xl">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-900">
                {isEditing ? 'Edit Your Profile' : 'Complete Your Profile'}
              </h2>
              <span className="text-gray-600 text-sm">
                Step {step} of {totalSteps}
              </span>
            </div>
            <div className="flex gap-2">
              {[1, 2, 3].map((s) => (
                <div
                  key={s}
                  className={`h-2 flex-1 rounded-full transition-all ${
                    s <= step
                      ? 'bg-gradient-to-r from-purple-600 to-blue-600'
                      : 'bg-gray-200'
                  }`}
                />
              ))}
            </div>
          </div>
  
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
              {error}
            </div>
          )}
  
          <div className="min-h-[400px]">
            {/* Step 1: Basic Information */}
            {step === 1 && (
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Basic Information
                </h3>
  
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Age"
                    name="age"
                    type="number"
                    value={profile.age}
                    onChange={updateProfile}
                    placeholder="25"
                    min="1"
                    max="120"
                    required
                  />
  
                  <Select
                    label="Gender"
                    name="gender"
                    value={profile.gender}
                    onChange={updateProfile}
                    options={GENDER_OPTIONS}
                    required
                  />
                </div>
  
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Height (cm)"
                    name="height"
                    type="number"
                    value={profile.height}
                    onChange={updateProfile}
                    placeholder="170"
                    min="100"
                    max="250"
                    required
                  />
  
                  <Input
                    label="Weight (kg)"
                    name="weight"
                    type="number"
                    value={profile.weight}
                    onChange={updateProfile}
                    placeholder="70"
                    min="20"
                    max="300"
                    required
                  />
                </div>
              </div>
            )}
  
            {/* Step 2: Lifestyle & Preferences */}
            {step === 2 && (
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Lifestyle & Preferences
                </h3>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Activity Level
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {ACTIVITY_LEVELS.map((level) => (
                      <ToggleButton
                        key={level.value}
                        label={level.label}
                        value={level.value}
                        isSelected={profile.activityLevel === level.value}
                        onClick={(value) => updateProfile('activityLevel', value)}
                      />
                    ))}
                  </div>
                </div>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Dietary Preference
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {DIETARY_PREFERENCES.map((diet) => (
                      <ToggleButton
                        key={diet.value}
                        label={diet.label}
                        value={diet.value}
                        isSelected={profile.dietaryPreference === diet.value}
                        onClick={(value) => updateProfile('dietaryPreference', value)}
                      />
                    ))}
                  </div>
                </div>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Region
                  </label>
                  <div className="grid grid-cols-4 gap-3">
                    {REGIONS.map((reg) => (
                      <ToggleButton
                        key={reg.value}
                        label={reg.label}
                        value={reg.value}
                        isSelected={profile.region === reg.value}
                        onClick={(value) => updateProfile('region', value)}
                      />
                    ))}
                  </div>
                </div>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Current Mood (optional)
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {MOODS.map((m) => (
                      <ToggleButton
                        key={m.value}
                        label={m.label}
                        value={m.value}
                        isSelected={profile.mood === m.value}
                        onClick={(value) =>
                          updateProfile('mood', profile.mood === value ? '' : value)
                        }
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
  
            {/* Step 3: Health & Goals */}
            {step === 3 && (
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Health & Goals
                </h3>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Your Goal
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {GOALS.map((g) => {
                      const Icon = goalIcons[g.value];
                      return (
                        <ToggleButton
                          key={g.value}
                          label={g.label}
                          value={g.value}
                          isSelected={profile.goal === g.value}
                          onClick={(value) => updateProfile('goal', value)}
                          icon={Icon}
                        />
                      );
                    })}
                  </div>
                </div>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Medical Conditions (optional)
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {MEDICAL_CONDITIONS.map((cond) => (
                      <ToggleButton
                        key={cond.value}
                        label={cond.label}
                        value={cond.value}
                        isSelected={profile.medicalConditions.includes(cond.value)}
                        onClick={(value) => toggleArrayField('medicalConditions', value)}
                      />
                    ))}
                  </div>
                </div>
  
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Allergies (optional)
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {ALLERGIES.map((allergy) => (
                      <ToggleButton
                        key={allergy.value}
                        label={allergy.label}
                        value={allergy.value}
                        isSelected={profile.allergies.includes(allergy.value)}
                        onClick={(value) => toggleArrayField('allergies', value)}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
  
          <div className="flex gap-4 mt-8">
            {step > 1 && (
              <Button variant="secondary" onClick={() => setStep(step - 1)}>
                Back
              </Button>
            )}
            <Button
              onClick={handleNext}
              disabled={!canProceed() || loading}
              loading={loading}
              fullWidth
            >
              {step === totalSteps ? 'Complete' : 'Next'}
              <ArrowRight className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
  
};