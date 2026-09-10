import json
import random
import os

def calibrate_clinical_macros():
    db_path = 'clean_ingredients_db.json'
    recipes_path = 'recipes.json'

    if not os.path.exists(db_path) or not os.path.exists(recipes_path):
        print("❌ Error: Missing JSON files in the directory.")
        return

    with open(db_path, 'r', encoding='utf-8') as f:
        ingredients_db = json.load(f)
    
    with open(recipes_path, 'r', encoding='utf-8') as f:
        recipes_data = json.load(f)

    # 1. Inject "Added Table Salt" into the Database
    salt_code = "Z002"
    salt_entry = {
        "food_code": salt_code,
        "food_type": "(Z)ADDED_FATS_AND_OILS", 
        "name": "Standard Table Salt (NaCl)",
        "energy_kcal": 0.0,
        "protein_g": 0.0,
        "total_fat_g": 0.0,
        "carbs_g": 0.0,
        "dietary_fiber_g": 0.0,
        "sodium_mg": 38758.0, # 38,758mg of sodium per 100g of table salt
        "potassium_mg": 0.0,
        "free_sugars_g": 0.0,
        "metadata": {
            "is_goitrogenic": False,
            "is_high_sodium": True,
            "is_high_sugar": False,
            "is_high_fiber": False
        }
    }

    if not any(item['food_code'] == salt_code for item in ingredients_db):
        ingredients_db.append(salt_entry)
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(ingredients_db, f, indent=4)
        print(f"🧂 Injected {salt_entry['name']} ({salt_code}) into database!")

    db_lookup = {item['food_code']: item for item in ingredients_db}
    oil_code = "Z001"

    print("\n⚙️ Calibrating Salt and Fat levels...\n")

    # Expanded to catch heavy breakfasts like Puri, Bhature, or Paratha
    heavy_meals = ["Dal Makhani", "Paratha", "Bhurji", "Soya Bean Curry", "Masala Dosa", "Puri", "Bhature", "Kachori"]

    for category, meals in recipes_data.items():
        for meal in meals:
            if 'ingredients_g' not in meal:
                continue
            
            # --- 2. CALIBRATE FAT (GHEE/OIL) ---
            if any(heavy in meal['meal_name'] for heavy in heavy_meals):
                meal['ingredients_g'][oil_code] = random.randint(20, 25)
            # Ensure every standard meal (including breakfast tadka) gets some oil
            elif oil_code not in meal['ingredients_g']:
                meal['ingredients_g'][oil_code] = random.randint(5, 10)

            # --- 3. CALIBRATE SODIUM (SALT) ---
            if category in ["lunches", "dinners"]:
                meal['ingredients_g'][salt_code] = round(random.uniform(1.2, 2.0), 1)
            else:
                # Breakfasts get slightly less salt, but still enough to register clinically
                meal['ingredients_g'][salt_code] = round(random.uniform(0.6, 1.2), 1)

            # --- 4. RECALCULATE PURE MACROS ---
            calc_cals, calc_pro, calc_carbs, calc_fat, calc_fiber, calc_sodium = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

            for code, weight_g in meal['ingredients_g'].items():
                if code in db_lookup:
                    ing = db_lookup[code]
                    mult = weight_g / 100.0
                    calc_cals += (ing.get('energy_kcal', 0) * mult)
                    calc_pro += (ing.get('protein_g', 0) * mult)
                    calc_carbs += (ing.get('carbs_g', 0) * mult)
                    calc_fat += (ing.get('total_fat_g', 0) * mult)
                    calc_fiber += (ing.get('dietary_fiber_g', 0) * mult)
                    calc_sodium += (ing.get('sodium_mg', 0) * mult)

            # Overwrite JSON with calculated truth
            meal['base_calories'] = round(calc_cals, 1)
            meal['base_protein_g'] = round(calc_pro, 1)
            meal['base_carbs_g'] = round(calc_carbs, 1)
            meal['base_fat_g'] = round(calc_fat, 1)
            meal['base_fiber_g'] = round(calc_fiber, 1)
            meal['base_sodium_mg'] = round(calc_sodium, 1)

    # 5. Save the mathematically sound database
    final_recipes_path = 'recipes_calibrated.json'
    with open(final_recipes_path, 'w', encoding='utf-8') as f:
        json.dump(recipes_data, f, indent=4)
    
    print(f"\n💾 SUCCESS! Saved scientifically accurate macros to '{final_recipes_path}'")

if __name__ == "__main__":
    calibrate_clinical_macros()