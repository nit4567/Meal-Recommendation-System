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

from services.diet_engine import get_safe_basket, generate_weekly_plan 
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
        
    targets = {
        "daily_calorie_target": calc.daily_calorie_target,
        "protein_target_g": calc.protein_target_g,
        "conditions": conditions if conditions else None
    }

    # 3. Apply Medical Constraints & Generate Plan
    safe_basket = get_safe_basket(conditions)
    weekly_plan_json = generate_weekly_plan(safe_basket, targets)
    
    if not weekly_plan_json:
        raise HTTPException(status_code=500, detail="AI failed to generate plan")

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