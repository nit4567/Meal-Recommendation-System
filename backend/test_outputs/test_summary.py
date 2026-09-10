import json
import numpy as np
import pandas as pd


def load_plan(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data["plan"]


def extract_metrics(plan):
    # Dynamically detect metrics
    sample_day = next(iter(plan.values()))
    sample_meal = sample_day["breakfast"]

    return [k for k in sample_meal.keys() if k != "meal_name"]


def compute_stats(plan):
    metrics = extract_metrics(plan)
    meals = ["breakfast", "lunch", "dinner"]

    rows = []

    for meal in meals:
        for metric in metrics:
            values = []

            for day_name, day in plan.items():
                if not day_name.startswith("day_"):
                    continue

                values.append(day[meal][metric])

            mean = np.mean(values)
            std = np.std(values)
            cv = std / mean if mean != 0 else 0

            rows.append({
                "Meal": meal,
                "Metric": metric,
                "Mean": round(mean, 2),
                "Std Dev": round(std, 2),
                "CV": round(cv, 3)
            })

    return pd.DataFrame(rows)

def flag_issues(df):
    """
    Flags problematic metrics:
    - High variability (CV > 0.25)
    - High sodium mean (> 600 per meal)
    - High calories mean (> 700 per meal)
    """

    conditions = []

    for _, row in df.iterrows():
        issues = []

        if row["CV"] > 0.25:
            issues.append("HIGH_VAR")

        if row["Metric"] == "sodium_mg" and row["Mean"] > 600:
            issues.append("HIGH_SODIUM")

        if row["Metric"] == "calories" and row["Mean"] > 700:
            issues.append("HIGH_CAL")

        conditions.append(", ".join(issues) if issues else "")

    df["Flags"] = conditions
    return df


def summarize_file(file_path):
    print(f"\n📊 FILE: {file_path}")

    plan = load_plan(file_path)
    df = compute_stats(plan)
    df = flag_issues(df)

    print(df.to_string(index=False))


def compare_files(file_list):
    all_results = []

    for file in file_list:
        plan = load_plan(file)
        df = compute_stats(plan)
        df["File"] = file
        all_results.append(df)

    combined = pd.concat(all_results)

    print("\n📊 COMBINED COMPARISON")
    print(combined.to_string(index=False))


if __name__ == "__main__":
    files = [
        "./test_outputs/test_1_baseline.json",
        "./test_outputs/test_2_hypertension.json",
        "./test_outputs/test_3_thyroid.json",
        "./test_outputs/test_4_obesity.json",
        "./test_outputs/test_5_constipation.json"
    ]

    # Individual summaries
    for file in files:
        summarize_file(file)

    # Uncomment if you want cross-file comparison
    # compare_files(files)