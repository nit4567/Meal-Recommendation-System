# =============================================================================
# ICMR Food Group Auto-Scaling Script
# Generates missing 'moderate' and 'heavy' activity rows from existing sedentary ones
# =============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FoodGroupReference
from config import SQLALCHEMY_DATABASE_URL

# Scaling factors
MODERATE_FACTOR = 1.28
HEAVY_FACTOR = 1.3  # relative to moderate

# Setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def scaled_value(val, factor):
    try:
        return round(float(val) * factor, 1)
    except:
        return None


def create_scaled_row(base_row, category, factor):
    """Clone and scale a FoodGroupReference row."""
    return FoodGroupReference(
        age_group=base_row.age_group,
        gender=base_row.gender,
        category_of_work=category,
        base_weight_kg=base_row.base_weight_kg,
        cereals_g=scaled_value(base_row.cereals_g, factor),
        pulses_g=scaled_value(base_row.pulses_g, factor),
        glv_g=scaled_value(base_row.glv_g, factor),
        veg_g=scaled_value(base_row.veg_g, factor),
        roots_tubers_g=scaled_value(base_row.roots_tubers_g, factor),
        fruits_g=scaled_value(base_row.fruits_g, factor),
        milk_curd_ml=scaled_value(base_row.milk_curd_ml, factor),
        fats_oils_g=scaled_value(base_row.fats_oils_g, factor),
        energy_kcal=scaled_value(base_row.energy_kcal, factor),
        protein_g=scaled_value(base_row.protein_g, factor),
    )


def expand_food_groups():
    sedentary_rows = session.query(FoodGroupReference).filter_by(category_of_work="sedentary").all()
    total_added = 0

    for base in sedentary_rows:
        # Check if moderate already exists
        has_moderate = session.query(FoodGroupReference).filter_by(
            age_group=base.age_group,
            gender=base.gender,
            category_of_work="moderate"
        ).first()

        # Generate moderate if missing
        if not has_moderate:
            moderate_row = create_scaled_row(base, "moderate", MODERATE_FACTOR)
            session.add(moderate_row)
            total_added += 1

        # Check if heavy already exists
        has_heavy = session.query(FoodGroupReference).filter_by(
            age_group=base.age_group,
            gender=base.gender,
            category_of_work="heavy"
        ).first()

        # Use either the moderate factor or compound scaling
        if not has_heavy:
            heavy_factor = MODERATE_FACTOR * HEAVY_FACTOR  # ~1.664x sedentary
            heavy_row = create_scaled_row(base, "heavy", heavy_factor)
            session.add(heavy_row)
            total_added += 1

    session.commit()
    print(f"✅ Added {total_added} new rows (moderate/heavy).")


if __name__ == "__main__":
    expand_food_groups()
    session.close()
