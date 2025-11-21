# =============================================================================
# ICMR CALCULATION ENGINE
# =============================================================================

import json
from models import UserProfile, FoodGroupReference

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m * height_m)


def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    elif bmi < 23:
        return "normal"
    elif bmi < 25:
        return "overweight"
    else:
        return "obese"


def calculate_bmr(weight_kg: float, gender: str, age: int) -> float:
    """Calculate BMR using ICMR 2020 adjusted multipliers (10% lower than WHO)"""
    if gender == "male":
        if age >= 18:
            multiplier = 32  # Sedentary base
        elif age >= 16:
            multiplier = 52
        elif age >= 13:
            multiplier = 57
        elif age >= 10:
            multiplier = 64
        else:
            multiplier = 67
    else:  # female
        if age >= 18:
            multiplier = 30  # Sedentary base
        elif age >= 16:
            multiplier = 45
        elif age >= 13:
            multiplier = 49
        elif age >= 10:
            multiplier = 57
        else:
            multiplier = 67
    
    return weight_kg * multiplier


def get_pal(activity_level: str) -> float:
    """Get Physical Activity Level multiplier"""
    pals = {
        "sedentary": 1.05,
        "moderate": 1.3,
        "heavy": 1.7
    }
    return pals.get(activity_level, 1.4)


def calculate_targets(profile: UserProfile) -> dict:
    """Calculate all nutritional targets based on ICMR 2020 guidelines"""
    
    # BMI
    bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
    bmi_category = get_bmi_category(bmi)
    
    # Energy
    bmr = calculate_bmr(profile.weight_kg, profile.gender, profile.age)
    pal = get_pal(profile.activity_level)
    #The total energy requirement or the total energy expenditure (TEE) is calculated based on a 
    #multiplication of basal metabolic rate (BMR) to physical activity level (PAL): TEE = BMR X PAL. 
    tee = bmr * pal
    
    # Adjust for goal
    calorie_target = tee
    if profile.goal == "weight_loss":
        calorie_target -= 400
    elif profile.goal == "weight_gain":
        calorie_target += 400
    elif profile.goal == "muscle_gain":
        calorie_target += 300
    
    # Protein - ICMR 2020: 0.83 g/kg/day (RDA) or 1.0 for vegetarian
    protein_multiplier = 1.0 if profile.dietary_preference == "vegetarian" else 0.83
    protein_target = profile.weight_kg * protein_multiplier
    
    # Iron - ICMR 2020
    medical_conditions = json.loads(profile.medical_conditions or "[]")
    iron_target = 19 if profile.gender == "male" else 29
    if "pregnancy" in medical_conditions:
        iron_target = 35
    
    # Calcium - ICMR 2020
    calcium_target = 1000
    if "pregnancy" in medical_conditions or "lactation" in medical_conditions:
        calcium_target = 1200
    
    # Fiber - 14g per 1000 kcal
    fiber_target = (calorie_target / 1000) * 14
    
    # Visible fat - 27g for 2000 kcal diet
    visible_fat_target = (calorie_target / 2000) * 27
    
    # Essential fatty acids - ICMR 2020
    n6_pufa = 6.6
    n3_pufa = 2.2
    
    return {
        "bmi": round(bmi, 1),
        "bmi_category": bmi_category,
        "bmr": round(bmr),
        "tee": round(tee),
        "daily_calorie_target": round(calorie_target),
        "protein_target_g": round(protein_target),
        "iron_target_mg": iron_target,
        "calcium_target_mg": calcium_target,
        "fiber_target_g": round(fiber_target),
        "visible_fat_target_g": round(visible_fat_target),
        "n6_pufa_target_g": n6_pufa,
        "n3_pufa_target_g": n3_pufa
    }

def generate_food_plan(profile: UserProfile, ref: FoodGroupReference):
    """
    Generate a scaled food plan from the ICMR reference row and user profile.
    Pure function — no DB queries here.
    """
    if not ref:
        return None

    # Calculate scaling factor based on user's calorie needs
    targets = calculate_targets(profile)
    factor = targets["daily_calorie_target"] / ref.energy_kcal

    return {
        "cereals_g": round(ref.cereals_g * factor, 1),
        "pulses_g": round(ref.pulses_g * factor, 1),
        "glv_g": round(ref.glv_g * factor, 1),
        "veg_g": round(ref.veg_g * factor, 1),
        "roots_tubers_g": round(ref.roots_tubers_g * factor, 1),
        "fruits_g": round(ref.fruits_g * factor, 1),
        "milk_curd_ml": round(ref.milk_curd_ml * factor, 1),
        "fats_oils_g": round(ref.fats_oils_g * factor, 1),
        "total_energy_kcal": round(targets["daily_calorie_target"]),
        "total_protein_g": round(ref.protein_g * factor, 1)
    }
