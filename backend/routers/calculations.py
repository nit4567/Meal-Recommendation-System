# =============================================================================
# CALCULATION ROUTERS
# =============================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config import get_db
from models import User, UserProfile, UserCalculation, FoodGroupReference
from schemas import CalculationResponse
from security import get_current_user
from calculations import calculate_targets, generate_food_plan

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
