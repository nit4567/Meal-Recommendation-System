# =============================================================================
# CALCULATION ROUTERS
# =============================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config import get_db
from models import User, UserProfile, UserCalculation, FoodGroupReference, UserWeeklyPlan
from schemas import CalculationResponse
from security import get_current_user
from calculations import calculate_targets, generate_food_plan
from datetime import datetime, timezone

router = APIRouter(prefix="/calculations", tags=["calculations"])

# Standalone calculate endpoint (without prefix)
calculate_router = APIRouter(tags=["calculations"])

def get_clinical_snacks(conditions):
    """Provides fixed, safe snacks based on the user's primary medical condition."""
    conditions_lower = [c.lower() for c in conditions]
    
    if "constipation" in conditions_lower:
        return ["Ripe Papaya Bowl (High Fiber)", "Soaked Chia Seeds in Water (Hydration & Fiber)"]
    if "hypertension" in conditions_lower:
        return ["Banana (High Potassium)", "Coconut Water (No added salt)"]
    if "obesity" in conditions_lower:
        return ["Cucumber & Carrot Sticks", "Green Tea (Unsweetened)"]
    if "thyroid" in conditions_lower:
        return ["Roasted Pumpkin Seeds (Selenium)", "Apple"]
        
    # Default for healthy users
    return ["Mixed Nuts (Almonds & Walnuts)", "Seasonal Fresh Fruit"]


@calculate_router.post("/calculate", response_model=CalculationResponse)
def recalculate(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Recalculate targets based on current profile"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please complete your profile first.")
    
    # Calculate targets
    targets = calculate_targets(profile)
    
    # Save calculation
    calculation = UserCalculation(
        user_id=current_user.id,
        **targets
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    
    return calculation


@router.get("/latest", response_model=CalculationResponse)
def get_latest_calculation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    calculation = db.query(UserCalculation).filter(
        UserCalculation.user_id == current_user.id
    ).order_by(UserCalculation.calculated_at.desc()).first()
    
    if not calculation:
        raise HTTPException(status_code=404, detail="No calculations found")
    
    return calculation


@router.get("/history", response_model=List[CalculationResponse])
def get_calculation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    calculations = db.query(UserCalculation).filter(
        UserCalculation.user_id == current_user.id
    ).order_by(UserCalculation.calculated_at.desc()).limit(limit).all()
    
    return calculations

@router.get("/food-plan")
def get_food_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    profile = db.query(UserProfile).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    # Fetch ICMR reference for same gender + activity
    ref = db.query(FoodGroupReference).filter_by(
        gender=profile.gender,
        category_of_work=profile.activity_level
    ).first()

    if not ref:
        raise HTTPException(status_code=404, detail="Food group reference not found")

    plan = generate_food_plan(profile, ref)

    return {
        "user_id": user_id,
        "food_plan": plan
    }

from services.diet_engine import  generate_weekly_plan , get_safe_menu
import json


@router.post("/generate-ai-plan")
def create_ai_weekly_plan(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # 1. Fetch User Profile & Medical Conditions
    profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    conditions = json.loads(profile.medical_conditions or "[]")
    
    # 2. Fetch Latest Calorie/Protein Targets
    calc = db.query(UserCalculation).filter_by(user_id=current_user.id).order_by(UserCalculation.calculated_at.desc()).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Please calculate targets first")
        
    # ICMR approximate calorie densities for side items not in recipes
    MILK_KCAL_PER_ML  = 0.67   # whole milk ~67 kcal/100ml
    FRUIT_KCAL_PER_G  = 0.50   # mixed fruit ~50 kcal/100g
    SUGAR_KCAL_PER_G  = 4.0    # for chai/tea sugar allowance
    
    # Fetch ICMR food group reference for this user (same query as food-plan endpoint)
    ref = db.query(FoodGroupReference).filter_by(
        gender=profile.gender,
        category_of_work=profile.activity_level
    ).first()
    
    # Calculate calories that come from side items OUTSIDE the 3 main meals
    # These are already accounted for in the ICMR daily_calorie_target
    # but won't appear in recipes.json
    side_item_kcal = 0
    if ref:
        side_item_kcal += (ref.milk_curd_ml or 0) * MILK_KCAL_PER_ML
        side_item_kcal += (ref.fruits_g    or 0) * FRUIT_KCAL_PER_G
        side_item_kcal += 20 * SUGAR_KCAL_PER_G  # ~20g sugar in daily tea/chai
    
    side_item_kcal = round(side_item_kcal)
    
    # Meal target = total target minus what comes from side items
    # Also reserve ~200 kcal for the clinical snacks already in the plan
    meal_calorie_target = calc.daily_calorie_target - side_item_kcal - 200
    
    targets = {
        "daily_calorie_target": max(calc.daily_calorie_target - side_item_kcal - 200, 1000),  # floor at 1000 for safety
        "protein_target_g":     calc.protein_target_g,
        "fiber_target_g":       getattr(calc, 'fiber_target_g', 30),
        "sodium_target_mg":     getattr(calc, 'sodium_target_mg', 2300),
        "conditions":           conditions,
        # Pass TEE for dynamic obesity cap (Fix 2)
        "tee":                  calc.tee,
    }

    # 3. Apply Medical Constraints & Generate Plan
    #safe_basket = get_safe_basket(conditions)
    safe_menu = get_safe_menu(conditions) # <-- Updated function name
    weekly_plan_json = generate_weekly_plan(safe_menu, targets)
    
    if not weekly_plan_json:
        raise HTTPException(status_code=500, detail="AI failed to generate plan")
    
    weekly_plan_json["daily_snacks"] = get_clinical_snacks(conditions)

    # 4. Save to Database
    new_plan = UserWeeklyPlan(
        user_id=current_user.id,
        generated_at=datetime.now(timezone.utc),
        conditions_applied=json.dumps(conditions),
        plan_data=json.dumps(weekly_plan_json)
    )
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return {
        "message": "AI Weekly Plan generated and saved successfully",
        "plan_id": new_plan.id,
        "conditions_applied": conditions,
        "plan": weekly_plan_json
    }



@router.get("/my-weekly-plan")
def get_saved_plan(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Fetch the most recently generated plan for this user
    latest_plan = db.query(UserWeeklyPlan).filter_by(
        user_id=current_user.id
    ).order_by(UserWeeklyPlan.generated_at.desc()).first()
    
    if not latest_plan:
        raise HTTPException(status_code=404, detail="No meal plan found. Generate one first.")
        
    return {
        "plan_id": latest_plan.id,
        "generated_at": latest_plan.generated_at,
        "conditions_applied": json.loads(latest_plan.conditions_applied),
        "plan": json.loads(latest_plan.plan_data)
    }

