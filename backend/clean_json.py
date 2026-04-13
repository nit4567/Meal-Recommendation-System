import json

INPUT_FILE = "raw_ingredients_db.json"
OUTPUT_FILE = "clean_ingredients_db.json"

# --- Disease Tagging Thresholds & Lists ---
HIGH_SODIUM_THRESHOLD = 400.0 
HIGH_SUGAR_THRESHOLD = 15.0

# Known goitrogenic foods
GOITROGEN_KEYWORDS = [
    "cabbage", "cauliflower", "broccoli", "brussels sprout", 
    "kale", "radish", "turnip", "soy", "soyabean", "mustard", "spinach"
]

def prune_and_tag(food_items):
    clean_db = []
    
    for item in food_items:
        slim_item = {
            "food_code": item.get("food_code"),
            "food_type": item.get("food_type"),
            "name": item.get("name"),
        }
        
        # Extract Macros using the new Table 1 exact keys
        # Convert IFCT Energy (kJ) to standard Energy (kcal) by dividing by 4.184
        raw_energy_kj = item.get("energy_mean", 0.0)
        slim_item["energy_kcal"] = round(raw_energy_kj / 4.184, 2)
        
        slim_item["protein_g"] = item.get("protein_mean", 0.0)
        slim_item["total_fat_g"] = item.get("total_fat_mean", 0.0)
        # Prefer total carbohydrate from Table 1, fallback to available cho
        slim_item["carbs_g"] = item.get("carbohydrate_mean", item.get("available_cho_mean", 0.0))
        # The exact fiber key from Table 1
        slim_item["dietary_fiber_g"] = item.get("dietary_fibre_-_total_mean", 0.0)
        
        # Micronutrients
        slim_item["sodium_mg"] = item.get("na_mean", 0.0)
        slim_item["potassium_mg"] = item.get("k_mean", 0.0)
        slim_item["free_sugars_g"] = item.get("total_free_sugars_mean", 0.0)

        # --- Apply Disease Constraint Flags ---
        name_lower = str(slim_item["name"]).lower()
        
        is_goitrogenic = any(keyword in name_lower for keyword in GOITROGEN_KEYWORDS)
        is_high_sodium = slim_item["sodium_mg"] >= HIGH_SODIUM_THRESHOLD
        is_high_sugar = slim_item["free_sugars_g"] >= HIGH_SUGAR_THRESHOLD
        is_high_fiber = slim_item["dietary_fiber_g"] >= 5.0
        
        # Group binary tags into a metadata object
        slim_item["metadata"] = {
            "is_goitrogenic": is_goitrogenic,
            "is_high_sodium": is_high_sodium,
            "is_high_sugar": is_high_sugar,
            "is_high_fiber": is_high_fiber
        }
        
        clean_db.append(slim_item)
        
    return clean_db

# Execute the pruning
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    cleaned_data = prune_and_tag(raw_data)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=4)
        
    print(f"Successfully pruned database! Cleaned {len(cleaned_data)} items.")
    print(f"Saved to {OUTPUT_FILE}")
except Exception as e:
    print(f"Error processing JSON: {e}")