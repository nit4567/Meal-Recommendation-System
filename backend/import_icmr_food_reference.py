# =============================================================================
# One-time CSV Import Script for ICMR Food Group Reference Table
# =============================================================================

import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FoodGroupReference  # make sure model is defined
from config import SQLALCHEMY_DATABASE_URL        # e.g. "sqlite:///icmr.db" or your DB URI

# -------------------------------------------------------------------------
# 1. Setup DB connection
# -------------------------------------------------------------------------
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# -------------------------------------------------------------------------
# 2. Path to your CSV file
# -------------------------------------------------------------------------
CSV_FILE = "temp.csv"

# -------------------------------------------------------------------------
# 3. Insert records from CSV
# -------------------------------------------------------------------------
with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    records = []
    for row in reader:
        record = FoodGroupReference(
            age_group=row["age_group"],
            gender=row["gender"],
            category_of_work=row["category_of_work"],
            base_weight_kg=float(row["base_weight_kg"]),
            cereals_g=float(row["cereals_g"]),
            pulses_g=float(row["pulses_g"]),
            glv_g=float(row["glv_g"]),
            veg_g=float(row["veg_g"]),
            roots_tubers_g=float(row["roots_tubers_g"]),
            fruits_g=float(row["fruits_g"]),
            milk_curd_ml=float(row["milk_curd_ml"]),
            fats_oils_g=float(row["fats_oils_g"]),
            energy_kcal=float(row["energy_kcal"]),
            protein_g=float(row["protein_g"]),
        )
        records.append(record)

session.bulk_save_objects(records)
session.commit()
print(f"✅ Imported {len(records)} records into FoodGroupReference table.")
session.close()
