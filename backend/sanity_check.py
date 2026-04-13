import json

def run_sanity_check():
    # 1. Load your actual ingredient database
    try:
        with open('clean_ingredients_db.json', 'r', encoding='utf-8') as f:
            ingredients_db = json.load(f)
    except FileNotFoundError:
        print("Error: Could not find 'clean_ingredients_db.json'.")
        return

    # 2. Load the recipes you generated
    try:
        with open('recipe.json', 'r', encoding='utf-8') as f:
            recipes_data = json.load(f)
    except FileNotFoundError:
        print("Error: Could not find 'recipe.json'.")
        return

    # Create a quick lookup dictionary from your IFCT database
    # { "A001": "Amaranth seed, black", ... }
    code_to_name = {item['food_code']: item['name'] for item in ingredients_db}

    print("="*60)
    print("🥘 VEGITAMEAL SANITY CHECK: DB MAPPING VALIDATION")
    print("="*60)

    # Process each meal type (breakfasts, lunches, dinners)
    for meal_type, meals in recipes_data.items():
        print(f"\n>>> CATEGORY: {meal_type.upper()}")
        
        for meal in meals:
            print(f"\nMeal: {meal.get('meal_name', 'Unnamed Meal')}")
            print("-" * 30)
            
            codes = meal.get('ifct_ingredients_used', [])
            if not codes:
                print("  [!] No ingredients listed for this meal.")
                continue

            for code in codes:
                # This check pulls the real name from your clean_ingredients_db.json
                ingredient_name = code_to_name.get(code, "❌ ERROR: CODE NOT FOUND IN YOUR DB!")
                print(f"  [{code}] -> {ingredient_name}")

if __name__ == "__main__":
    run_sanity_check()