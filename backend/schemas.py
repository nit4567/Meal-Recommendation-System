# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProfileCreate(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    region: str
    dietary_preference: str
    activity_level: str
    goal: str
    medical_conditions: List[str] = []
    allergies: List[str] = []
    mood: Optional[str] = None


class ProfileResponse(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    region: str
    dietary_preference: str
    activity_level: str
    goal: str
    medical_conditions: List[str]
    allergies: List[str]
    mood: Optional[str]
    
    class Config:
        from_attributes = True


class CalculationResponse(BaseModel):
    bmi: float
    bmi_category: str
    bmr: float
    tee: float
    daily_calorie_target: float
    protein_target_g: float
    iron_target_mg: float
    calcium_target_mg: float
    fiber_target_g: float
    visible_fat_target_g: float
    n6_pufa_target_g: float
    n3_pufa_target_g: float
    calculated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

