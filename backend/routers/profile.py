# =============================================================================
# PROFILE ROUTERS
# =============================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
from config import get_db
from models import User, UserProfile, UserCalculation
from schemas import ProfileCreate, ProfileResponse
from security import get_current_user
from calculations import calculate_targets

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("")
def create_or_update_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if profile exists
    existing_profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        # Update
        for key, value in profile_data.dict().items():
            if key in ["medical_conditions", "allergies"]:
                setattr(existing_profile, key, json.dumps(value))
            else:
                setattr(existing_profile, key, value)
        existing_profile.updated_at = datetime.utcnow()
        profile = existing_profile
    else:
        # Create
        profile = UserProfile(
            user_id=current_user.id,
            age=profile_data.age,
            gender=profile_data.gender,
            height_cm=profile_data.height_cm,
            weight_kg=profile_data.weight_kg,
            region=profile_data.region,
            dietary_preference=profile_data.dietary_preference,
            activity_level=profile_data.activity_level,
            goal=profile_data.goal,
            medical_conditions=json.dumps(profile_data.medical_conditions),
            allergies=json.dumps(profile_data.allergies),
            mood=profile_data.mood
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
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
    
    return {
        "message": "Profile saved successfully",
        "calculation": calculation
    }


@router.get("", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return ProfileResponse(
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        region=profile.region,
        dietary_preference=profile.dietary_preference,
        activity_level=profile.activity_level,
        goal=profile.goal,
        medical_conditions=json.loads(profile.medical_conditions or "[]"),
        allergies=json.loads(profile.allergies or "[]"),
        mood=profile.mood
    )

