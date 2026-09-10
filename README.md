# Personalized Meal Recommendation System

A clinically aware, constraint-based meal planning engine and full-stack web application calibrated to **ICMR-NIN 2020** physiological guidelines and **IFCT 2017** Indian food composition tables.

---

## 📌 Overview

Most commercial dietary platforms rely on international metabolic equations (such as FAO/WHO) that overestimate the Basal Metabolic Rate (BMR) of Indian individuals by **10–12%** due to lower average skeletal muscle mass. Furthermore, generic meal recommenders rarely account for chronic lifestyle diseases, often recommending high-sodium dishes to hypertensive patients or goitrogenic ingredients to individuals with thyroid disorders, while suffering from severe "menu fatigue" (repeating identical meals daily).

**Personalized Meal Recommendation System** resolves these challenges by providing:
1. **Physiologically Grounded Baselines:** BMR, PAL, and TEE calculations tailored to Indian anthropometrics.
2. **Clinical Safety Invariants:** Strict ingredient-level safety filters and hard disqualification penalties for medical contraindications.
3. **Temporal Variety Heuristics:** Round-robin candidate pool tracking across 7 days to ensure diverse, non-repetitive meal schedules.
4. **Differential Portion Scaling:** Non-linear macronutrient scaling logic that preserves nutritional balance without spiking sodium or fat.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, Requests
- **Frontend:** React 19, Vite, TailwindCSS v4, Recharts, Lucide Icons, Axios
- **Data & Standards:** ICMR-NIN 2020 Dietary Guidelines, Indian Food Composition Tables (IFCT 2017)

---

## 🚀 Key Features

### 1. Constraint-Based Planning Engine
The core planner (`diet_engine.py`) models meal selection as a multi-objective penalty minimization problem. For each day, candidate triples $(Breakfast, Lunch, Dinner)$ are evaluated across a 7-component objective function:

$$P = P_{cal} + P_{sodium} + P_{fibre} + P_{fat} + P_{protein} + P_{carb} + P_{diversity}$$

- **Hard Bounds ($1\text{e}6$ penalty):** Disqualifies any meal combination that violates strict clinical limits (e.g. sodium $> 1300\text{ mg}$ for hypertension, calories $> TEE - 500$ for obesity).
- **Soft Targets:** Graded penalties penalize deviations from caloric targets ($\lambda = 3/\text{kcal}$), protein shortfalls, fiber windows, and a 50% carbohydrate energy ratio.

### 2. Multi-Disease Support
The engine enforces condition-specific nutritional rules:

| Condition | Max Sodium | Fat Ceiling | Fibre Target | Calorie Cap | Hard Ingredient Exclusions |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hypertension** | $1,300\text{ mg}$ | $55\text{ g}$ | $22\text{--}38\text{ g}$ | Standard Target | High-sodium ingredients |
| **Obesity** | $2,000\text{ mg}$ | $45\text{ g}$ | $28\text{--}40\text{ g}$ | $TEE - 500\text{ kcal}$ | High-sugar ingredients (Protein $\ge 60\text{g}$) |
| **Thyroid** | $1,500\text{ mg}$ | $60\text{ g}$ | $22\text{--}35\text{ g}$ | Standard Target | Goitrogens (cabbage, cauliflower, etc.) |
| **Constipation** | $2,000\text{ mg}$ | $60\text{ g}$ | $32\text{--}45\text{ g}$ | Standard Target | None (Elevated dietary fiber floor) |
| **Healthy Baseline** | $2,300\text{ mg}$ | $65\text{ g}$ | $22\text{--}38\text{ g}$ | Standard Target | Universal fat & sodium filters |

### 3. Round-Robin Recipe Pooling (Variety Assurance)
To eliminate repetitive menu fatigue, each meal slot manages an active pool of eligible dishes. Once a recipe is scheduled, it is temporarily popped from the candidate pool for subsequent days, resetting only when the pool is exhausted. A linear repeat penalty further discourages premature duplicates.

### 4. Differential Portion Scaling
Scaling entire meals uniformly causes sodium and saturated fat to spike. The engine decouples nutrient scaling:
- Calories and Carbohydrates scale with the target multiplier (capped at $1.8\times$).
- Sensitive nutrients are heavily clamped: Protein ($\le 1.35\times$), Fat ($\le 1.15\times$), and Sodium ($\le 1.05\times$).
- For users with active medical conditions, the serving multiplier is fixed at $1.0\times$, satisfying energy targets through meal selection rather than portion inflation.

### 5. Automated Validation Pipeline
An end-to-end clinical validation suite (`test_pipeline.py`) programmatically simulates 5 distinct disease cohorts over full 7-day cycles, asserting 100% ($35/35$ days) compliance on hard medical constraints.

---

## 📁 Repository Structure

```
meal_reco_system/
├── backend/
│   ├── main.py                        # FastAPI entry point & CORS configuration
│   ├── config.py                      # Database configuration & session factory
│   ├── models.py                      # SQLAlchemy models (User, Profile, Calculation, WeeklyPlan)
│   ├── schemas.py                     # Pydantic request/response schemas
│   ├── security.py                    # JWT authentication & password hashing
│   ├── calculations.py                # ICMR-NIN metabolic formulas (BMR, PAL, TEE)
│   ├── services/
│   │   └── diet_engine.py             # Planning engine, penalty function, pooling & scaling
│   ├── routers/
│   │   ├── auth.py                    # Authentication endpoints (/signup, /login)
│   │   ├── profile.py                 # User anthropometric & clinical profile CRUD
│   │   └── calculations.py            # Plan generation & retrieval endpoints
│   ├── recipes.json                   # Curated recipe catalog with macronutrients
│   ├── clean_ingredients_db.json      # Ingredient metadata flags (safety filters)
│   ├── test_pipeline.py               # Automated 5-cohort clinical test suite
│   ├── test_outputs/                  # Output JSON plans from validation runs
│   └── requirements.txt               # Python package dependencies
│
├── frontend/
│   ├── src/
│   │   ├── pages/dashboard/
│   │   │   └── Dashboard.jsx          # Main dashboard view
│   │   ├── components/dashboard/
│   │   │   ├── WeeklyPlanCard.jsx     # Interactive 7-day meal plan card (Mon-Sun)
│   │   │   ├── FoodGroupPieChart.jsx  # Recharts nutritional distribution
│   │   │   └── HealthAlert.jsx        # Clinical warning banners
│   │   ├── hooks/
│   │   │   └── useWeeklyPlan.js       # Plan state management & API hooks
│   │   └── api/                       # API integration modules
│   ├── package.json                   # Frontend dependencies & build scripts
│   └── vite.config.js                 # Vite bundler configuration
│
├── start_back.bat                     # Windows helper script to launch backend
├── start_front.bat                    # Windows helper script to launch frontend
└── README.md                          # Project documentation
```

---

## ⚡ Quick Start

### Prerequisites
- **Python:** Version 3.10 or higher
- **Node.js:** Version 18.0 or higher (with npm)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate a virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate
# macOS / Linux:
# python3 -m venv venv
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment configuration
cp .env.example .env

# Start the development server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
* Interactive API documentation (Swagger UI) is available at: **`http://127.0.0.1:8000/docs`**

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
* The web application will launch at: **`http://localhost:5173`**

### 3. Windows One-Click Launchers
Alternatively, on Windows systems, use the included batch scripts from the project root:
- `start_back.bat` (starts FastAPI backend)
- `start_front.bat` (starts Vite React frontend)

---

## 🧪 Running the Clinical Validation Suite

To run the automated test pipeline across all 5 disease cohorts:

```bash
cd backend
python test_pipeline.py
```

The script will:
1. Register standardized test users for Baseline, Hypertension, Thyroid, Obesity, and Constipation cohorts.
2. Trigger the plan generation pipeline for each test case.
3. Output the generated 7-day nutritional plans into `backend/test_outputs/` for constraint and compliance auditing.

---

## 📜 Academic Context & Acknowledgments

This project was developed as a **Bachelor of Technology Project Thesis** in the **Department of Agricultural and Food Engineering, Indian Institute of Technology Kharagpur**

Nutritional benchmarks and food composition metrics are derived from:
- **ICMR-National Institute of Nutrition (2020):** *Nutrient Requirements for Indians*.
- **Longvah, et al. (2017):** *Indian Food Composition Tables (IFCT)*, National Institute of Nutrition.
