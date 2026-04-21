import os
import json
from groq import Groq
import random

# Ensure you have GROQ_API_KEY in your .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_safe_menu(medical_conditions, recipes_path="recipes.json", db_path="clean_ingredients_db.json"):
    with open(recipes_path, "r", encoding="utf-8") as f:
        master_recipes = json.load(f)
        
    with open(db_path, "r", encoding="utf-8") as f:
        ingredient_db = json.load(f)
        
    ing_flags = {item["food_code"]: item.get("metadata", {}) for item in ingredient_db}
    conditions = [c.lower() for c in medical_conditions]
    
    safe_menu = {"breakfasts": [], "lunches": [], "dinners": []}
    
    for meal_type in ["breakfasts", "lunches", "dinners"]:
        if meal_type not in master_recipes:
            continue 
            
        for recipe in master_recipes[meal_type]:
            is_safe = True
            
            # Look at the keys of the new ingredients_g dictionary
            for code in recipe.get("ingredients_g", {}).keys():
                # Skip the Z category (oils) from strict clinical IFCT filtering, 
                # as oils are usually safe unless tracking pure fat/calories.
                if code.startswith("Z"):
                    continue
                    
                meta = ing_flags.get(code, {})
                
                if "hypertension" in conditions and meta.get("is_high_sodium", False):
                    is_safe = False
                    break 
                if "thyroid" in conditions and meta.get("is_goitrogenic", False):
                    is_safe = False
                    break
                if "obesity" in conditions and meta.get("is_high_sugar", False):
                    is_safe = False
                    break
                    
            if is_safe:
                # Pass ALL the new macros to the LLM
                safe_menu[meal_type].append({
                    "meal_name": recipe["meal_name"],
                    "calories": recipe["base_calories"],
                    "protein_g": recipe["base_protein_g"],
                    "carbs_g": recipe["base_carbs_g"],
                    "fat_g": recipe["base_fat_g"],
                    "fiber_g": recipe["base_fiber_g"],
                    "sodium_mg": recipe["base_sodium_mg"]
                })
                
    return safe_menu




def get_smart_pantry_subset(safe_basket, max_items=60):
    """
    Groups the 500+ safe ingredients by category and picks a random subset.
    This keeps the LLM prompt under 2,000 tokens while ensuring dietary variety.
    """
    categories = {}
    for item in safe_basket:
        cat = item.get("type", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
        
    mini_pantry = []
    
    # Pull up to 5 random items from every food category
    for cat, items in categories.items():
        random.shuffle(items)
        mini_pantry.extend(items[:5]) 
        
    # Give it one final shuffle and hard-cap the list
    random.shuffle(mini_pantry)
    return mini_pantry[:max_items]

def get_safe_basket(medical_conditions, db_path="clean_ingredients_db.json"):
    with open(db_path, "r", encoding="utf-8") as f:
        master_db = json.load(f)
        
    conditions = [c.lower() for c in medical_conditions]
    safe_basket = []
    
    # Keywords to catch all meat, poultry, fish, and eggs
    NON_VEG_KEYWORDS = ["MEAT", "POULTRY", "FISH", "EGG", "SHELLFISH", "MOLLUSKS"]
    
    for item in master_db:
        food_type = item.get("food_type", "").upper()
        
        # 1. VEGETARIAN CHECK: Skip entirely if it falls into a non-veg category
        if any(keyword in food_type for keyword in NON_VEG_KEYWORDS):
            continue
            
        meta = item.get("metadata", {})
        is_safe = True
        
        # 2. Clinical Constraints
        if "hypertension" in conditions and meta.get("is_high_sodium", False):
            is_safe = False
        if "thyroid" in conditions and meta.get("is_goitrogenic", False):
            is_safe = False
        if "obesity" in conditions and meta.get("is_high_sugar", False):
            is_safe = False
            
        if is_safe:
            safe_basket.append({
                "name": item["name"],
                "type": item["food_type"],
                "kcal": item["energy_kcal"],
                "protein_g": item["protein_g"]
            })
            
    return safe_basket


def generate_weekly_plan(safe_menu, targets):
    # Cap choices to save LLM tokens and ensure variety
    for meal_type in safe_menu:
        random.shuffle(safe_menu[meal_type])
        safe_menu[meal_type] = safe_menu[meal_type][:10] 
        
    menu_str = json.dumps(safe_menu)
    
    system_prompt = """
    You are an elite Indian Clinical Dietitian. Schedule a 7-day meal plan ONLY using the exact meals from the 'SAFE MENU'.
    
    CRITICAL RULES:
    1. STRICT MENU COMPLIANCE: Use the exact 'meal_name' and base macros provided. Do not invent meals.
    2. SERVINGS MATH: You must select 1 Breakfast, 1 Lunch, and 1 Dinner per day. Adjust the "servings" multiplier (e.g., 0.8, 1.0, 1.5) to hit the User Targets.
    3. MACRO BALANCING: 
       - Carbs should be roughly 45-55% of total calories.
       - Ensure daily Sodium is strictly below the target limit.
       - Ensure daily Fiber meets or exceeds the target.
    4. OUTPUT FORMAT: Strictly raw JSON. No markdown blocks.
    
    REQUIRED JSON SCHEMA:
    {
      "day_1": {
        "breakfast": {"meal_name": "Menu Name", "servings": 1.0, "calories": 387, "protein_g": 9.3, "fiber_g": 5.7, "sodium_mg": 5.5},
        "lunch": {...},
        "dinner": {...},
        "daily_totals": {
          "calories": 1500, "protein_g": 55, "carbs_g": 180, "fat_g": 45, "fiber_g": 32, "sodium_mg": 1200
        }
      },
      ... up to day_7
    }
    """
    
    user_prompt = f"""
    USER TARGETS:
    Calories: {targets.get('daily_calorie_target')} kcal
    Protein: {targets.get('protein_target_g')} g
    Fiber: {targets.get('fiber_target_g')} g minimum
    Sodium Limit: {targets.get('sodium_target_mg')} mg maximum
    Medical Conditions: {', '.join(targets.get('conditions', ['None']))}
    
    SAFE MENU:
    {menu_str}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1, 
            max_tokens=5000,
        )
        
        raw_output = response.choices[0].message.content.strip()
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:-3].strip()
            
        return json.loads(raw_output)
        
    except Exception as e:
        print(f"LLM Generation Error: {e}")
        return None