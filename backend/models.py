# =============================================================================
# DATABASE MODELS
# =============================================================================

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from config import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    food_plan = relationship("UserFoodPlan", back_populates="user", uselist=False)

    
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    calculations = relationship("UserCalculation", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    height_cm = Column(Float)
    weight_kg = Column(Float)
    region = Column(String(50))
    dietary_preference = Column(String(50))
    activity_level = Column(String(50))
    goal = Column(String(50))
    medical_conditions = Column(Text)  # JSON
    allergies = Column(Text)  # JSON
    mood = Column(String(50))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="profile")


class UserCalculation(Base):
    __tablename__ = "user_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bmi = Column(Float)
    bmi_category = Column(String(50))
    bmr = Column(Float)
    tee = Column(Float)
    daily_calorie_target = Column(Float)
    protein_target_g = Column(Float)
    iron_target_mg = Column(Float)
    calcium_target_mg = Column(Float)
    fiber_target_g = Column(Float)
    visible_fat_target_g = Column(Float)
    n6_pufa_target_g = Column(Float)
    n3_pufa_target_g = Column(Float)
    # Condition-specific fields
    sodium_target_mg = Column(Float, nullable=True)
    potassium_target_mg = Column(Float, nullable=True)
    water_target_ml = Column(Float, nullable=True)
    medication_alert = Column(Integer, default=0)  # SQLite-safe bool
    calculated_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="calculations")


class FoodGroupReference(Base):
    __tablename__ = "food_group_reference"

    id = Column(Integer, primary_key=True)
    age_group = Column(String(50))
    gender = Column(String(10))
    category_of_work = Column(String(20))  # sedentary, moderate, etc.
    base_weight_kg = Column(Float)
    cereals_g = Column(Float)
    pulses_g = Column(Float)
    glv_g = Column(Float)
    veg_g = Column(Float)
    roots_tubers_g = Column(Float)
    fruits_g = Column(Float)
    milk_curd_ml = Column(Float)
    fats_oils_g = Column(Float)
    energy_kcal = Column(Float)
    protein_g = Column(Float)

class UserFoodPlan(Base):
    __tablename__ = "user_food_plan"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_generated = Column(DateTime, default=datetime.now(timezone.utc))
    cereals_g = Column(Float)
    pulses_g = Column(Float)
    glv_g = Column(Float)
    veg_g = Column(Float)
    roots_tubers_g = Column(Float)
    fruits_g = Column(Float)
    milk_curd_ml = Column(Float)
    fats_oils_g = Column(Float)
    total_energy_kcal = Column(Float)
    total_protein_g = Column(Float)

    user = relationship("User", back_populates="food_plan")

class UserWeeklyPlan(Base):
    __tablename__ = "user_weekly_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Store the diseases that were active when this plan was generated
    conditions_applied = Column(Text)  # JSON string e.g., '["thyroid", "hypertension"]'
    
    # Store the actual LLM output
    plan_data = Column(Text)  # JSON string of the 7-day plan
    
    user = relationship("User", backref="weekly_plans")