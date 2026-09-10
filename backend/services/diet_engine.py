import json

# =============================================================================
# CONDITION-SPECIFIC CONSTRAINT RULES
# Single source of truth. Edit these values to tune the planner.
# =============================================================================
CONDITION_RULES = {

    "baseline": {
        "target_calories": 2100,

        "min_protein_g": 70,

        "target_fiber_g": 30,
        "min_fiber_g": 22,
        "max_fiber_g": 38,

        "max_sodium_mg": 2300,

        "max_fat_g": 75,

        "ideal_carb_pct": 0.50,
    },

    "hypertension": {
    "max_sodium_mg": 1300,
    "max_calories": None,
    "min_fiber_g": 22,
    "max_fiber_g": 38,
    "max_fat_g": 55,
},

"obesity": {
    "max_calories": None,
    "max_sodium_mg": 2000,
    "min_fiber_g": 28,
    "max_fiber_g": 40,
    "max_fat_g": 45,
},

"constipation": {
    "min_fiber_g": 32,
    "max_fiber_g": 45,
    "max_sodium_mg": 2000,
    "max_fat_g": 60,
    "max_calories": None,
},

"thyroid": {
    "max_sodium_mg": 1500,
    "min_fiber_g": 22,
    "max_fiber_g": 35,
    "max_fat_g": 60,
},
}

# Condition-specific protein floors (hard minimums)
PROTEIN_FLOORS = {
    "obesity": 60,   # prevent muscle loss during calorie deficit
}

# Universal fat cap — applies even with no conditions
UNIVERSAL_MAX_FAT_G = 65

# Penalty weights — tune here if needed
HARD_VIOLATION_PENALTY = 1_000_000   # something is medically wrong → never pick this
SOFT_VIOLATION_PENALTY = 50_000      # nutritionally bad but not dangerous
PER_UNIT_CALORIE_PENALTY = 3         # per kcal off target
PER_UNIT_PROTEIN_PENALTY = 80        # per g under protein target
PER_UNIT_FIBER_PENALTY = 80          # per g under fiber minimum
PER_UNIT_SODIUM_PENALTY = 500        # per mg over sodium limit
PER_UNIT_FAT_PENALTY = 100           # per g over fat limit
DIVERSITY_BASE = 8_000               # per repeat (linear, not quadratic — see below)
PER_UNIT_EXCESS_FIBER_PENALTY = 120
TARGET_FIBER_DEVIATION_PENALTY = 10

def get_safe_menu(medical_conditions, recipes_path="recipes.json", db_path="clean_ingredients_db.json"):
    """
    Filters recipes using ingredient-level metadata flags from the IFCT DB.
    Returns only meals safe for the user's conditions.
    """
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

            for code in recipe.get("ingredients_g", {}).keys():
                if code.startswith("Z"):   # skip oils/fats (handled by fat penalty)
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
                # Per-meal hard filters — reject outlier meals regardless of condition
                # These thresholds are per-meal (not daily), so ~3x = daily total
                meal_fat    = recipe["base_fat_g"]
                meal_sodium = recipe["base_sodium_mg"]

                # Fat filter: cap at 25g per meal (~75g daily max)
                # Relaxed slightly vs the 18g suggestion to avoid emptying the menu
                if meal_fat > 25:
                    continue

                # Sodium filter: cap at 600mg per meal (~1800mg daily)
                # For hypertension the scorer will further penalize within this range
                if meal_sodium > 600:
                    continue

                safe_menu[meal_type].append({
                    "meal_name":  recipe["meal_name"],
                    "calories":   recipe["base_calories"],
                    "protein_g":  recipe["base_protein_g"],
                    "carbs_g":    recipe["base_carbs_g"],
                    "fat_g":      recipe["base_fat_g"],
                    "fiber_g":    recipe["base_fiber_g"],
                    "sodium_mg":  recipe["base_sodium_mg"],
                })
    print(f"Safe menu sizes: B={len(safe_menu['breakfasts'])} L={len(safe_menu['lunches'])} D={len(safe_menu['dinners'])}")

    return safe_menu


def score_meal_combination(b, l, d, targets, used_meals, conditions, multiplier=1.0):
    """
    Penalty-based objective function. Lower = better.

    Design principle:
    - HARD constraints (medical safety) → HARD_VIOLATION_PENALTY (effectively disqualifies combo)
    - SOFT constraints (nutritional quality) → scaled per-unit penalties
    - Diversity → linear penalty per repeat (not quadratic, to avoid dominating nutrition)
    """
    total_cals   = b["calories"]  + l["calories"]  + d["calories"]
    total_prot   = b["protein_g"] + l["protein_g"] + d["protein_g"]
    total_carbs  = b["carbs_g"]   + l["carbs_g"]   + d["carbs_g"]
    total_fat    = b["fat_g"]     + l["fat_g"]      + d["fat_g"]
    total_fiber  = b["fiber_g"]   + l["fiber_g"]    + d["fiber_g"]
    total_sodium = b["sodium_mg"] + l["sodium_mg"]  + d["sodium_mg"]

    penalty = 0
    conditions_lower = [c.lower() for c in conditions]

    # ------------------------------------------------------------------
    # 1. Calorie target accuracy (universal)
    # ------------------------------------------------------------------
    target_cals = targets.get("daily_calorie_target", 2000)
    cal_error = abs(target_cals - total_cals)
    penalty += cal_error * PER_UNIT_CALORIE_PENALTY

    # Hard ceiling for obesity — being over is medically bad
    if "obesity" in conditions_lower:
        # Dynamic cap: TEE - 500 kcal deficit (standard weight loss target)
        # Use scaled calories so the cap applies to what the user actually eats
        tee = targets.get("tee") or 2000
        max_cals = tee - 500
        scaled_total_cals = total_cals * multiplier
        if scaled_total_cals > max_cals:
            penalty += HARD_VIOLATION_PENALTY + (scaled_total_cals - max_cals) * PER_UNIT_CALORIE_PENALTY * 10

    # Soft penalty for being >10% off target (any condition)
    elif cal_error > target_cals * 0.10:
        penalty += SOFT_VIOLATION_PENALTY

    # ------------------------------------------------------------------
    # 2. Sodium (condition-specific hard limits)
    # ------------------------------------------------------------------
    for cond in conditions_lower:
        rules = CONDITION_RULES.get(cond, {})
        max_sodium = rules.get("max_sodium_mg")
        if max_sodium and total_sodium > max_sodium:
            overage = total_sodium - max_sodium
            # Hypertension & thyroid: hard violation
            if cond in ("hypertension", "thyroid"):
                penalty += HARD_VIOLATION_PENALTY + overage * PER_UNIT_SODIUM_PENALTY
            else:
                penalty += overage * PER_UNIT_SODIUM_PENALTY

    # ------------------------------------------------------------------
    # 3. Fiber (constipation & obesity: hard minimums)
    # ------------------------------------------------------------------
    for cond in conditions_lower:
        rules = CONDITION_RULES.get(cond, {})
        target_fiber = rules.get("target_fiber_g")
        min_fiber = rules.get("min_fiber_g")
        max_fiber = rules.get("max_fiber_g")

        if min_fiber and total_fiber < min_fiber:
            deficit = min_fiber - total_fiber
            penalty += deficit * PER_UNIT_FIBER_PENALTY

        if max_fiber and total_fiber > max_fiber:
            excess = total_fiber - max_fiber
            penalty += excess * PER_UNIT_EXCESS_FIBER_PENALTY

        # Soft preference toward target
        if target_fiber:
            deviation = abs(total_fiber - target_fiber)
            penalty += deviation * TARGET_FIBER_DEVIATION_PENALTY

    # ------------------------------------------------------------------
    # 4. Fat ceiling
    #    Fix 1: universal cap applies even for baseline (no conditions)
    #    Condition-specific caps may be stricter
    # ------------------------------------------------------------------
    effective_fat_cap = UNIVERSAL_MAX_FAT_G
    for cond in conditions_lower:
        rules = CONDITION_RULES.get(cond, {})
        cond_fat = rules.get("max_fat_g")
        if cond_fat:
            effective_fat_cap = min(effective_fat_cap, cond_fat)

    if total_fat > effective_fat_cap:
        penalty += (total_fat - effective_fat_cap) * PER_UNIT_FAT_PENALTY

    # ------------------------------------------------------------------
    # 5. Protein
    #    Fix 2: obesity gets a hard protein floor, others get soft penalty
    # ------------------------------------------------------------------
    target_prot = targets.get("protein_target_g", 50)

    if "obesity" in conditions_lower:
        hard_floor = PROTEIN_FLOORS["obesity"]
        if total_prot < hard_floor:
            penalty += HARD_VIOLATION_PENALTY + (hard_floor - total_prot) * PER_UNIT_PROTEIN_PENALTY
    elif total_prot < target_prot:
        penalty += (target_prot - total_prot) * PER_UNIT_PROTEIN_PENALTY

    # ------------------------------------------------------------------
    # 6. Carb balance (soft — 50% of calories from carbs ideally)
    # ------------------------------------------------------------------
    ideal_carbs = (target_cals * 0.50) / 4
    penalty += abs(ideal_carbs - total_carbs) * 1.5

    # ------------------------------------------------------------------
    # 7. Diversity — LINEAR penalty per repeat (not quadratic)
    #    Quadratic was dominating nutrition scoring with small recipe sets.
    #    Linear keeps it as a tiebreaker, not the primary driver.
    # ------------------------------------------------------------------
    for meal in [b, l, d]:
        freq = used_meals.get(meal["meal_name"], 0)
        penalty += freq * DIVERSITY_BASE

    return penalty


def generate_weekly_plan(safe_menu, targets):
    """
    Exhaustive search over all (breakfast, lunch, dinner) combos per day.

    Diversity strategy:
    - HARD: no meal repeats until all meals in that slot have been used once (round-robin pool)
    - If pool is exhausted (day 8+ or tiny recipe set), allow repeats but score penalizes them
    - This guarantees variety WITHOUT letting diversity fight medical constraints
    """
    weekly_plan = {}
    conditions  = targets.get("conditions", [])

    if not safe_menu["breakfasts"] or not safe_menu["lunches"] or not safe_menu["dinners"]:
        print("CRITICAL: One of your safe menus is entirely empty! Check recipe filtering.")
        return None

    # Serving multiplier: scale recipes up if target exceeds max possible combo
    # Cap at 1.8x to keep portions realistic; disease cases capped at 1.3x
    target_cals  = targets.get("daily_calorie_target", 2000)
    max_possible = (
        max(m["calories"] for m in safe_menu["breakfasts"]) +
        max(m["calories"] for m in safe_menu["lunches"])    +
        max(m["calories"] for m in safe_menu["dinners"])
    )
    has_condition = len(conditions) > 0

    if has_condition:
        # Disease users: no scaling — hard constraints are already managing their targets
        # Scaling fights the penalty system (e.g. hypertension sodium cap)
        multiplier = 1.0
    else:
        # Baseline users: scale up to hit calorie target, cap at 1.8x
        raw_multiplier = target_cals / max_possible if max_possible > 0 else 1.0
        multiplier     = min(raw_multiplier, 1.8)
        multiplier     = max(multiplier, 1.0)  # never scale down

    def scale(meal):
        calorie_scale = multiplier

        protein_scale = min(multiplier, 1.35)
        carb_scale    = multiplier
        fat_scale     = min(multiplier, 1.15)
        fiber_scale   = min(multiplier, 1.20)
        sodium_scale  = min(multiplier, 1.05)

        return {
            "meal_name": meal["meal_name"],

            "calories": round(meal["calories"] * calorie_scale),

            "protein_g": round(meal["protein_g"] * protein_scale, 1),

            "carbs_g": round(meal["carbs_g"] * carb_scale, 1),

            "fat_g": round(meal["fat_g"] * fat_scale, 1),

            "fiber_g": round(meal["fiber_g"] * fiber_scale, 1),

            "sodium_mg": round(meal["sodium_mg"] * sodium_scale),

            "serving_multiplier": round(multiplier, 2),
        }

    # Round-robin pools — each meal slot gets its own "available" list
    # Once a meal is used, it's removed from the pool until all are exhausted, then reset
    pools = {
        "breakfasts": list(safe_menu["breakfasts"]),
        "lunches":    list(safe_menu["lunches"]),
        "dinners":    list(safe_menu["dinners"]),
    }
    used_meals = {}  # still tracked for scoring tiebreakers

    def get_pool(slot):
        """Return current pool; reset if exhausted."""
        if not pools[slot]:
            pools[slot] = list(safe_menu[slot])
        return pools[slot]

    for day in range(1, 8):
        best_combo = None
        best_score = float("inf")

        b_pool = get_pool("breakfasts")
        l_pool = get_pool("lunches")
        d_pool = get_pool("dinners")

        for b in b_pool:
            for l in l_pool:
                for d in d_pool:
                    # Hard rule: no two slots on the same day can share a meal name
                    if len({b["meal_name"], l["meal_name"], d["meal_name"]}) < 3:
                        continue
                    score = score_meal_combination(b, l, d, targets, used_meals, conditions, multiplier)
                    if score < best_score:
                        best_score = score
                        best_combo = (b, l, d)

        # Fallback (should never fire with 15 recipes per slot)
        if best_combo is None:
            best_combo = (b_pool[0], l_pool[0], d_pool[0])

        b_best, l_best, d_best = best_combo

        # Apply serving multiplier to chosen meals
        b_best = scale(b_best)
        l_best = scale(l_best)
        d_best = scale(d_best)

        # Update global used tracker
        for meal in [b_best, l_best, d_best]:
            used_meals[meal["meal_name"]] = used_meals.get(meal["meal_name"], 0) + 1

        # Remove used meal names from ALL slot pools — prevents the same meal
        # appearing in different slots on future days (cross-slot repeat bug)
        used_names = set(used_meals.keys())
        for slot in pools:
            pools[slot] = [m for m in pools[slot] if m["meal_name"] not in used_names]

        daily_totals = {
            "calories":   round(b_best["calories"]  + l_best["calories"]  + d_best["calories"]),
            "protein_g":  round(b_best["protein_g"] + l_best["protein_g"] + d_best["protein_g"], 1),
            "carbs_g":    round(b_best["carbs_g"]   + l_best["carbs_g"]   + d_best["carbs_g"],   1),
            "fat_g":      round(b_best["fat_g"]      + l_best["fat_g"]     + d_best["fat_g"],     1),
            "fiber_g":    round(b_best["fiber_g"]   + l_best["fiber_g"]   + d_best["fiber_g"],   1),
            "sodium_mg":  round(b_best["sodium_mg"] + l_best["sodium_mg"] + d_best["sodium_mg"]),
        }

        weekly_plan[f"day_{day}"] = {
            "breakfast":    b_best,
            "lunch":        l_best,
            "dinner":       d_best,
            "daily_totals": daily_totals,
        }

    return weekly_plan