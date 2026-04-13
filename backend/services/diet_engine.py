import os
import json
from groq import Groq
import random

# Ensure you have GROQ_API_KEY in your .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

def generate_weekly_plan(safe_basket, targets):
    mini_pantry = get_smart_pantry_subset(safe_basket, max_items=60)
    basket_str = json.dumps(mini_pantry)
    
    system_prompt = """
    You are an expert Indian Clinical Nutritionist and Chef powering the VegitaMeal app.
    Your job is to generate a 7-day, strictly vegetarian Indian meal plan.
    
    CRITICAL RULES:
    1. RECIPE NAMES, NOT RAW INGREDIENTS: Users want to see meals (e.g., "Ragi Dosa with Sambar", "Palak Paneer with Roti"). Do NOT just list raw ingredients.
    2. SAFE INGREDIENTS ONLY: You must build these recipes using ONLY the ingredients provided in the 'SAFE INGREDIENT BASKET'. 
    3. NO TEXT: Output MUST be strictly valid JSON. 
    
    REQUIRED JSON SCHEMA:
    {
      "day_1": {
        "breakfast": {
            "meal_name": "Ragi Porridge with Buffalo Milk",
            "key_ingredients_used": ["Ragi (Eleusine coracana)", "Milk, whole, Buffalo"],
            "approx_calories": 400
        },
        "lunch": {
            "meal_name": "Yellow Dal with Bajra Roti and Brinjal Sabzi",
            "key_ingredients_used": ["Lentil whole, yellowish", "Bajra", "Brinjal-4"],
            "approx_calories": 650
        },
        "dinner": { ... }
      },
      ... up to day_7
    }
    """
    
    user_prompt = f"""
    USER TARGETS:
    Daily Calories: {targets.get('daily_calorie_target', 2000)} kcal
    Daily Protein: {targets.get('protein_target_g', 50)} g
    
    SAFE INGREDIENT BASKET:
    {basket_str}
    INSTRUCTIONS BASED ON CONDITIONS:
    If 'obesity' is listed, strictly avoid pairing high-carb items together.
    If 'constipation' is listed, you MUST prioritize items from the basket that are high in dietary fiber.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2, 
            max_tokens=4000, 
        )
        
        raw_output = response.choices[0].message.content.strip()
        
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:-3].strip()
            
        return json.loads(raw_output)
        
    except Exception as e:
        print(f"LLM Generation Error: {e}")
        return None