# ICMR Nutrition Planner - Backend API

A FastAPI-based REST API for personalized nutrition planning following ICMR-NIN 2020 guidelines.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Application Flow](#application-flow)
- [Database Schema](#database-schema)
- [ICMR Calculations](#icmr-calculations)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

```bash
# 1. Create project directory
mkdir backend
cd backend

# 2. Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
python main.py

# Server starts at http://localhost:8000
# API Docs at http://localhost:8000/docs
```

---

## 📁 Project Structure

```
backend/
├── main.py                    # Main FastAPI application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── icmr_nutrition.db         # SQLite database (auto-generated)
├── test_api.py               # API testing script
└── README.md                 # This file

# Recommended modular structure (future):
backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app instance
│   ├── config.py             # Configuration
│   ├── database.py           # Database connection
│   │
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── profile.py
│   │   └── calculation.py
│   │
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── profile.py
│   │   └── calculation.py
│   │
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── profile.py
│   │   └── calculation.py
│   │
│   ├── core/                 # Core logic
│   │   ├── __init__.py
│   │   ├── security.py       # Auth & hashing
│   │   └── icmr.py          # ICMR calculations
│   │
│   └── utils/               # Helper functions
│       ├── __init__.py
│       └── dependencies.py
│
├── tests/                   # Test files
│   └── test_api.py
│
├── requirements.txt
└── README.md
```

---

## ✨ Features

### Authentication & Security
- ✅ JWT token-based authentication
- ✅ Bcrypt password hashing
- ✅ Token expiration (7 days default)
- ✅ Secure route protection

### User Management
- ✅ User signup with email validation
- ✅ User login with credential verification
- ✅ Get current user endpoint

### Profile Management
- ✅ Create/update user profile
- ✅ Store age, gender, height, weight
- ✅ Lifestyle preferences (activity, diet, region)
- ✅ Health goals and medical conditions
- ✅ Allergies tracking

### ICMR 2020 Calculations
- ✅ BMI calculation (Indian standards)
- ✅ BMR calculation (adjusted for Indian population)
- ✅ Total Energy Expenditure (TEE)
- ✅ Daily calorie targets
- ✅ Protein requirements (0.83 g/kg or 1.0 g/kg for vegetarians)
- ✅ Iron requirements (gender & condition based)
- ✅ Calcium requirements
- ✅ Fiber targets
- ✅ Essential fatty acids (Omega-3 & Omega-6)

### Data Management
- ✅ Calculation history tracking
- ✅ Automatic recalculation on profile update
- ✅ SQLite database (upgradeable to PostgreSQL)

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Dependencies

Create `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic[email]==2.5.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
pyjwt==2.8.0
python-multipart==0.0.6
```

Install:
```bash
pip install -r requirements.txt
```

### Environment Setup

Create `.env` file:
```bash
SECRET_KEY=super-secret-key
DATABASE_URL=sqlite:///./nutrition.db
```

Generate secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📖 API Documentation

### Interactive Docs

Once server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

### Authentication

All protected endpoints require Bearer token:
```http
Authorization: Bearer <your_jwt_token>
```

---

## 🔄 Application Flow

### 1. User Signup Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    POST /auth/signup                        │
│  { email, password, first_name, last_name }                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Validate Email       │
         │  Check if user exists │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Hash Password        │
         │  (using bcrypt)       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Create User Record   │
         │  in Database          │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Generate JWT Token   │
         │  (expires in 7 days)  │
         └───────────┬───────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│              Return Response                               │
│  { access_token, token_type, user: {...} }                │
└────────────────────────────────────────────────────────────┘
```

### 2. User Login Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     POST /auth/login                        │
│              { email, password }                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Find User by Email   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Verify Password      │
         │  (compare hashes)     │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Generate JWT Token   │
         └───────────┬───────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│              Return Response                               │
│  { access_token, token_type, user: {...} }                │
└────────────────────────────────────────────────────────────┘
```

### 3. Profile Creation & Calculation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    POST /profile                            │
│  Headers: Authorization: Bearer <token>                     │
│  Body: { age, gender, height, weight, activity, ... }      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Decode & Verify      │
         │  JWT Token            │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Check if Profile     │
         │  Already Exists       │
         └───────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
  ┌─────────┐              ┌─────────┐
  │ Update  │              │ Create  │
  │ Profile │              │ Profile │
  └────┬────┘              └────┬────┘
       │                        │
       └────────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  ICMR CALCULATIONS    │
        │  ─────────────────    │
        │  1. Calculate BMI     │
        │  2. Calculate BMR     │
        │  3. Calculate TEE     │
        │  4. Adjust for Goal   │
        │  5. Protein Target    │
        │  6. Iron Target       │
        │  7. Calcium Target    │
        │  8. Fiber Target      │
        │  9. Fat Targets       │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Save Calculation     │
        │  to Database          │
        └───────────┬───────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────────┐
│              Return Response                               │
│  { message, calculation: {...} }                           │
└────────────────────────────────────────────────────────────┘
```

### 4. Dashboard Data Loading Flow

```
┌─────────────────────────────────────────────────────────────┐
│             Frontend: Dashboard Loads                       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌────────────────┐      ┌────────────────────┐
│  GET /profile  │      │ GET /calculations/ │
│                │      │      latest        │
└───────┬────────┘      └─────────┬──────────┘
        │                         │
        │   ┌─────────────────────┘
        │   │
        ▼   ▼
┌────────────────────────────────────┐
│     Verify JWT Token               │
└────────────┬───────────────────────┘
             │
   ┌─────────┴─────────┐
   │                   │
   ▼                   ▼
┌──────────┐    ┌──────────────┐
│ Query    │    │ Query Latest │
│ Profile  │    │ Calculation  │
└────┬─────┘    └──────┬───────┘
     │                 │
     │   ┌─────────────┘
     │   │
     ▼   ▼
┌────────────────────────────────────┐
│   Return Both Responses            │
│   Frontend displays dashboard      │
└────────────────────────────────────┘
```

### 5. Request/Response Flow with Middleware

```
┌─────────────────────────────────────────────────────────────┐
│                   Incoming Request                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  CORS Middleware      │
         │  Check origin         │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Route Matching       │
         └───────────┬───────────┘
                     │
            ┌────────┴────────┐
            │                 │
    ┌───────▼──────┐   ┌──────▼────────┐
    │ Public Route │   │ Protected     │
    │ (/auth/*)    │   │ Route         │
    └───────┬──────┘   └──────┬────────┘
            │                 │
            │                 ▼
            │      ┌──────────────────┐
            │      │ Verify JWT Token │
            │      │ (Depends)        │
            │      └──────┬───────────┘
            │             │
            │      ┌──────▼───────┐
            │      │ Get User     │
            │      │ from Token   │
            │      └──────┬───────┘
            │             │
            └─────────────┤
                          │
                          ▼
              ┌───────────────────────┐
              │  Endpoint Function    │
              │  (business logic)     │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Database Operations  │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Prepare Response     │
              └───────────┬───────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Return Response                          │
│        { status_code, headers, body }                       │
└─────────────────────────────────────────────────────────────┘
```

### 6. Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Request Received                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Try Block    │
              │ Execute      │
              └──────┬───────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   ┌─────────┐             ┌──────────┐
   │ Success │             │  Error   │
   └────┬────┘             └────┬─────┘
        │                       │
        │                       ▼
        │            ┌──────────────────┐
        │            │ Catch Exception  │
        │            └────┬─────────────┘
        │                 │
        │       ┌─────────┴─────────┐
        │       │                   │
        │       ▼                   ▼
        │  ┌─────────┐       ┌──────────┐
        │  │ HTTP    │       │ Database │
        │  │ Error   │       │ Error    │
        │  └────┬────┘       └────┬─────┘
        │       │                 │
        │       └────────┬────────┘
        │                │
        │                ▼
        │     ┌──────────────────┐
        │     │ Format Error     │
        │     │ Response         │
        │     └────┬─────────────┘
        │          │
        └──────────┤
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│              Return Response                                 │
│  Success: { data }                                           │
│  Error: { detail: "error message" }                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: Store user authentication data

**Relationships**: 
- One-to-One with `user_profiles`
- One-to-Many with `user_calculations`

### User Profiles Table

```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    age INTEGER,
    gender VARCHAR(10),              -- 'male' or 'female'
    height_cm FLOAT,
    weight_kg FLOAT,
    region VARCHAR(50),              -- 'north', 'south', 'east', 'west'
    dietary_preference VARCHAR(50),  -- 'vegetarian', 'non-vegetarian', 'vegan'
    activity_level VARCHAR(50),      -- 'sedentary', 'moderate', 'heavy'
    goal VARCHAR(50),                -- 'weight_loss', 'weight_gain', etc.
    medical_conditions TEXT,         -- JSON: ["diabetes", "hypertension"]
    allergies TEXT,                  -- JSON: ["peanuts", "gluten"]
    mood VARCHAR(50),                -- 'energetic', 'stressed', 'calm'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose**: Store user's personal and health information

### User Calculations Table

```sql
CREATE TABLE user_calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    
    -- BMI
    bmi FLOAT,
    bmi_category VARCHAR(50),        -- 'underweight', 'normal', 'overweight', 'obese'
    
    -- Energy
    bmr FLOAT,                       -- Basal Metabolic Rate
    tee FLOAT,                       -- Total Energy Expenditure
    daily_calorie_target FLOAT,      -- Adjusted for goal
    
    -- Macros & Nutrients
    protein_target_g FLOAT,
    iron_target_mg FLOAT,
    calcium_target_mg FLOAT,
    fiber_target_g FLOAT,
    
    -- Fats
    visible_fat_target_g FLOAT,      -- Cooking oil
    n6_pufa_target_g FLOAT,          -- Omega-6
    n3_pufa_target_g FLOAT,          -- Omega-3
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose**: Store calculation history for tracking

**Indexes**: 
- `user_id` for fast user queries
- `calculated_at` for chronological ordering

### Database Relationships

```
┌──────────────┐
│    users     │
│              │
│ id (PK)      │◄────┐
│ email        │     │
│ password     │     │
└──────────────┘     │
                     │
                     │ 1:1
        ┌────────────┴──────────────┐
        │                           │
┌───────▼──────────┐     ┌──────────▼────────┐
│  user_profiles   │     │ user_calculations │
│                  │     │                   │
│ id (PK)          │     │ id (PK)           │
│ user_id (FK)     │     │ user_id (FK)      │
│ age, gender, ... │     │ bmi, bmr, ...     │
└──────────────────┘     └───────────────────┘
                                1:N
```

---

## 🧮 ICMR Calculations

### 1. BMI Calculation

```python
BMI = weight (kg) / height (m)²
```

**Indian Standards (ICMR 2020):**
- Underweight: < 18.5
- Normal: 18.5 - 22.9
- Overweight: 23 - 25
- Obese: ≥ 25

### 2. BMR Calculation

```python
# ICMR 2020: 10% lower than FAO/WHO/UNU for Indian adults
# Using simplified multipliers

For Men (age ≥ 18):
BMR = weight × 32  (sedentary base)

For Women (age ≥ 18):
BMR = weight × 30  (sedentary base)
```

**Why adjusted?**
- Indian body composition has relatively more fat
- Lower muscle mass compared to Western populations
- ICMR recommends 10% reduction from WHO estimates

### 3. Total Energy Expenditure (TEE)

```python
TEE = BMR × PAL

Physical Activity Levels (PAL):
- Sedentary: 1.4
- Moderate: 1.8  
- Heavy: 2.2
```

### 4. Daily Calorie Target

```python
Base = TEE

Adjustments by Goal:
- Weight Loss: TEE - 400 kcal
- Weight Gain: TEE + 400 kcal
- Muscle Gain: TEE + 300 kcal
- Maintenance: TEE (no change)
```

### 5. Protein Requirements

```python
# ICMR 2020 RDA

Standard (high-quality protein):
Protein = 0.83 g/kg body weight

For Vegetarian (cereal-based diet):
Protein = 1.0 g/kg body weight
```

**Note**: Cereal-legume-milk ratio should be 3:1:2.5

### 6. Iron Requirements

```python
# ICMR 2020 RDA

Male: 19 mg/day
Female: 29 mg/day
Pregnancy: 35 mg/day
```

### 7. Calcium Requirements

```python
# ICMR 2020 RDA

Adults: 1000 mg/day
Pregnancy/Lactation: 1200 mg/day
```

### 8. Fiber Target

```python
Fiber = 14 g per 1000 kcal

Example:
If daily calories = 2400 kcal
Fiber = (2400 / 1000) × 14 = 33.6 g
```

### 9. Visible Fat (Cooking Oil)

```python
# ICMR 2020: 20-50g per day (4-10 teaspoons)

Reference: 27g for 2000 kcal diet

Visible Fat = (daily_calories / 2000) × 27
```

### 10. Essential Fatty Acids

```python
# ICMR 2020 Fixed amounts

Omega-6 (n-6 PUFA): 6.6 g/day
Omega-3 (n-3 PUFA): 2.2 g/day
```

**Sources**:
- n-6: Nuts, seeds, vegetable oils
- n-3: Flaxseed, walnuts, fish

### Complete Calculation Flow

```python
def calculate_targets(profile):
    # 1. BMI
    bmi = weight / (height_m ** 2)
    bmi_category = get_category(bmi)
    
    # 2. BMR (adjusted for India)
    if profile.gender == 'male':
        bmr = weight * 32
    else:
        bmr = weight * 30
    
    # 3. TEE
    pal = get_pal(profile.activity_level)  # 1.4, 1.8, or 2.2
    tee = bmr * pal
    
    # 4. Calorie target
    if profile.goal == 'weight_loss':
        calorie_target = tee - 400
    elif profile.goal == 'weight_gain':
        calorie_target = tee + 400
    else:
        calorie_target = tee
    
    # 5. Protein
    if profile.dietary_preference == 'vegetarian':
        protein = weight * 1.0
    else:
        protein = weight * 0.83
    
    # 6. Iron
    if profile.gender == 'male':
        iron = 19
    elif 'pregnancy' in profile.medical_conditions:
        iron = 35
    else:
        iron = 29  # female
    
    # 7. Calcium
    if 'pregnancy' in profile.medical_conditions or 
       'lactation' in profile.medical_conditions:
        calcium = 1200
    else:
        calcium = 1000
    
    # 8. Fiber
    fiber = (calorie_target / 1000) * 14
    
    # 9. Visible fat
    visible_fat = (calorie_target / 2000) * 27
    
    # 10. Essential fatty acids
    n6_pufa = 6.6
    n3_pufa = 2.2
    
    return {
        'bmi': bmi,
        'bmi_category': bmi_category,
        'bmr': bmr,
        'tee': tee,
        'daily_calorie_target': calorie_target,
        'protein_target_g': protein,
        'iron_target_mg': iron,
        'calcium_target_mg': calcium,
        'fiber_target_g': fiber,
        'visible_fat_target_g': visible_fat,
        'n6_pufa_target_g': n6_pufa,
        'n3_pufa_target_g': n3_pufa
    }
```

---

## 🔐 Authentication

### JWT Token Structure

```json
{
  "user_id": 1,
  "exp": 1699999999  // Expiration timestamp
}
```

### Password Hashing

```python
# Using bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", hashed)
```

### Token Generation

```python
import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

### Protected Route Pattern

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("user_id")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# Usage in endpoint
@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    # current_user is automatically injected
    return current_user.profile
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing/invalid token |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate email/resource |
| 500 | Server Error | Unexpected error |

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

### Common Error Scenarios

**1. Email Already Exists**
```json
// POST /auth/signup
Status: 400
{
  "detail": "Email already registered"
}
```

**2. Invalid Credentials**
```json
// POST /auth/login
Status: 401
{
  "detail": "Invalid email or password"
}
```

**3. Token Expired**
```json
// GET /profile (with expired token)
Status: 401
{
  "detail": "Token has expired"
}
```

**4. Profile Not Found**
```json
// GET /profile (no profile created)
Status: 404
{
  "detail": "Profile not found"
}
```

---

## 🧪 Testing

### Manual Testing with test_api.py

```bash
python test_api.py
```

**What it tests:**
1. ✅ User signup
2. ✅ User login
3. ✅ Get current user
4. ✅ Create profile
5. ✅ Get profile
6. ✅ Get latest calculation
7. ✅ Recalculate

### Testing with cURL

**Signup:**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

**Get Profile (with token):**
```bash
curl -X GET http://localhost:8000/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Testing with Swagger UI

1. Go to http://localhost:8000/docs
2. Click on endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

---

## 🚀 Deployment

### Option 1: Railway.app

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Connect Railway to GitHub repo
# 3. Add environment variables in Railway dashboard:
SECRET_KEY=your-production-secret-key
DATABASE_URL=sqlite:///./icmr_nutrition.db

# 4. Deploy automatically
```

**Railway Configuration:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 2: Render.com

```bash
# 1. Push to GitHub

# 2. Create new Web Service on Render
# 3. Connect GitHub repo
# 4. Configure:
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

# 5. Add environment variables
```

### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./icmr_nutrition.db:/app/icmr_nutrition.db
```

Run:
```bash
docker-compose up --build
```

### Production Checklist

- [ ] Change SECRET_KEY to secure random string
- [ ] Update CORS to allow only frontend domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Regular database backups
- [ ] Environment variables properly configured

---

## 🐛 Troubleshooting

### Issue: Server won't start

**Symptoms:** Port already in use, import errors

**Solution:**
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Check imports
pip list
pip install -r requirements.txt --upgrade
```

### Issue: Database errors

**Symptoms:** Table doesn't exist, column not found

**Solution:**
```bash
# Delete database and recreate
rm icmr_nutrition.db
python main.py  # Tables will be auto-created
```

### Issue: CORS errors from frontend

**Symptoms:** "Access-Control-Allow-Origin" error in browser

**Solution:**
```python
# In main.py, update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: JWT token errors

**Symptoms:** "Token has expired", "Invalid token"

**Solution:**
```python
# Check token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Verify SECRET_KEY is consistent
# Generate new secret key if needed
import secrets
print(secrets.token_urlsafe(32))
```

### Issue: Calculation values seem wrong

**Symptoms:** Unexpected BMI, calorie targets

**Solution:**
```python
# Verify input data
print(f"Weight: {weight_kg} kg")
print(f"Height: {height_cm} cm")
print(f"Age: {age} years")

# Check multipliers
# Male sedentary: weight × 32
# Female sedentary: weight × 30

# Verify PAL values
sedentary = 1.4
moderate = 1.8
heavy = 2.2
```

### Issue: Profile not found after creation

**Symptoms:** 404 error when getting profile

**Solution:**
```python
# Check if profile was actually created
# View database
sqlite3 icmr_nutrition.db
SELECT * FROM user_profiles;

# Verify user_id matches
SELECT * FROM users;
```

---

## 📊 API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/signup` | No | Create new account |
| POST | `/auth/login` | No | Login to account |
| GET | `/auth/me` | Yes | Get current user info |

### Profile Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/profile` | Yes | Create/update profile |
| GET | `/profile` | Yes | Get user profile |

### Calculation Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/calculations/latest` | Yes | Get latest calculation |
| GET | `/calculations/history` | Yes | Get calculation history |
| POST | `/calculate` | Yes | Trigger recalculation |

### Request/Response Examples

**POST /auth/signup**
```json
// Request
{
  "email": "user@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}

// Response (200)
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**POST /profile**
```json
// Request (with Authorization header)
{
  "age": 25,
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 70,
  "region": "north",
  "dietary_preference": "vegetarian",
  "activity_level": "moderate",
  "goal": "weight_loss",
  "medical_conditions": ["diabetes"],
  "allergies": ["peanuts"],
  "mood": "energetic"
}

// Response (200)
{
  "message": "Profile saved successfully",
  "calculation": {
    "id": 1,
    "user_id": 1,
    "bmi": 22.9,
    "bmi_category": "normal",
    "bmr": 2100,
    "tee": 3780,
    "daily_calorie_target": 3380,
    "protein_target_g": 70,
    "iron_target_mg": 19,
    "calcium_target_mg": 1000,
    "fiber_target_g": 47,
    "visible_fat_target_g": 46,
    "n6_pufa_target_g": 6.6,
    "n3_pufa_target_g": 2.2,
    "calculated_at": "2024-01-15T10:30:00"
  }
}
```

**GET /calculations/latest**
```json
// Response (200)
{
  "id": 1,
  "user_id": 1,
  "bmi": 22.9,
  "bmi_category": "normal",
  "bmr": 2100,
  "tee": 3780,
  "daily_calorie_target": 3380,
  "protein_target_g": 70,
  "iron_target_mg": 19,
  "calcium_target_mg": 1000,
  "fiber_target_g": 47,
  "visible_fat_target_g": 46,
  "n6_pufa_target_g": 6.6,
  "n3_pufa_target_g": 2.2,
  "calculated_at": "2024-01-15T10:30:00"
}
```

---

## 🔄 Database Migration (SQLite to PostgreSQL)

### Why Migrate?

SQLite is great for development but PostgreSQL is better for production:
- Better concurrent user handling
- More robust data integrity
- Better performance at scale
- Support for advanced features

### Migration Steps

1. **Install PostgreSQL driver:**
```bash
pip install psycopg2-binary
```

2. **Update DATABASE_URL:**
```python
# .env
DATABASE_URL=postgresql://username:password@localhost/icmr_nutrition
```

3. **Update main.py:**
```python
# Remove this line:
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Replace with:
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

4. **Export SQLite data (optional):**
```bash
sqlite3 icmr_nutrition.db .dump > backup.sql
```

5. **Create tables in PostgreSQL:**
```python
Base.metadata.create_all(bind=engine)
```

---

## 📈 Performance Optimization

### Database Indexing

```python
# Add indexes for frequently queried fields
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)  # Index for fast lookup
    
class UserCalculation(Base):
    __tablename__ = "user_calculations"
    
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # Index for joins
    calculated_at = Column(DateTime, default=datetime.utcnow, index=True)  # Index for ordering
```

### Query Optimization

```python
# Good: Select only needed columns
profile = db.query(UserProfile.age, UserProfile.gender).filter(...).first()

# Bad: Select all columns when not needed
profile = db.query(UserProfile).filter(...).first()

# Good: Use joins efficiently
result = db.query(User, UserProfile).join(UserProfile).filter(...).first()

# Good: Limit results
latest_calculations = db.query(UserCalculation).order_by(
    UserCalculation.calculated_at.desc()
).limit(10).all()
```

### Caching (Future Enhancement)

```python
# Use Redis for caching frequently accessed data
from redis import Redis

redis_client = Redis(host='localhost', port=6379)

def get_profile_cached(user_id):
    # Try cache first
    cached = redis_client.get(f"profile:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from DB
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    # Cache for 1 hour
    redis_client.setex(f"profile:{user_id}", 3600, json.dumps(profile))
    
    return profile
```

---

## 🔐 Security Best Practices

### 1. Password Security

```python
# ✅ Good: Use bcrypt with sufficient rounds
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ❌ Bad: Plain text passwords
# NEVER store passwords in plain text!
```

### 2. SQL Injection Prevention

```python
# ✅ Good: Use SQLAlchemy ORM
user = db.query(User).filter(User.email == email).first()

# ❌ Bad: Raw SQL with string formatting
# cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### 3. Token Security

```python
# ✅ Good: Use secure secret key
SECRET_KEY = secrets.token_urlsafe(32)

# ❌ Bad: Weak secret key
# SECRET_KEY = "secret"

# ✅ Good: Set reasonable expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# ❌ Bad: No expiration or too long
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # 1 year
```

### 4. Input Validation

```python
# ✅ Good: Validate with Pydantic
class UserSignup(BaseModel):
    email: EmailStr  # Validates email format
    password: str
    
    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

# ✅ Good: Sanitize inputs
def sanitize_string(s: str) -> str:
    return s.strip().lower()
```

### 5. Rate Limiting (Future Enhancement)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
def login(...):
    pass
```

---

## 📝 Logging

### Setup Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in endpoints
@app.post("/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {credentials.email}")
    
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user:
            logger.warning(f"Login failed: User not found - {credentials.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        logger.info(f"Login successful for user: {user.id}")
        return {"access_token": token}
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise
```

---

## 🎯 Future Enhancements (Phase 2 & 3)

### Phase 2: Ingredients Database

```sql
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    calories_per_100g FLOAT,
    protein_g_per_100g FLOAT,
    carbs_g_per_100g FLOAT,
    fiber_g_per_100g FLOAT,
    iron_mg_per_100g FLOAT,
    calcium_mg_per_100g FLOAT,
    sodium_mg_per_100g FLOAT,
    glycemic_index INTEGER,
    allergens TEXT,  -- JSON: ["gluten", "dairy"]
    region VARCHAR(50),
    dietary_type VARCHAR(50)
);
```

**New Endpoints:**
- `GET /ingredients` - List all ingredients
- `GET /ingredients/search?query=wheat` - Search ingredients
- `GET /ingredients/filtered` - Filter by allergies, diet type
- `POST /ingredients` - Admin: Add new ingredient

### Phase 3: Meal Recommendations

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    meal_type VARCHAR(50),  -- breakfast, lunch, dinner, snack
    cuisine VARCHAR(50),
    target_calories INTEGER,
    prep_time_min INTEGER
);

CREATE TABLE recipe_ingredients (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    ingredient_id INTEGER,
    quantity_g FLOAT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
```

**New Endpoints:**
- `GET /meals/recommend` - Get meal recommendations
- `GET /meals/plan/daily` - Get full day meal plan
- `GET /meals/plan/weekly` - Get weekly meal plan
- `POST /meals/customize` - Customize meal plan

**Recommendation Algorithm:**
```
1. Get user's calorie target (e.g., 2400 kcal/day)
2. Split by meal:
   - Breakfast: 25% (600 kcal)
   - Lunch: 35% (840 kcal)
   - Snack: 10% (240 kcal)
   - Dinner: 30% (720 kcal)
3. Filter ingredients:
   - Remove allergens
   - Apply dietary preference
   - Apply medical condition filters
   - Prefer regional ingredients
4. Select recipes matching calorie ranges
5. Validate nutrient totals
6. Return meal plan
```

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org
- **Pydantic Documentation**: https://docs.pydantic.dev
- **ICMR-NIN 2020 Guidelines**: Refer to attached PDF
- **Python Best Practices**: https://docs.python-guide.org

---

## 🤝 Contributing

When extending the backend:

1. **New Endpoint**: Follow REST conventions
2. **New Model**: Add to database models section
3. **New Calculation**: Add to ICMR calculations
4. **Documentation**: Update this README
5. **Testing**: Add test cases in test_api.py

---

## 📞 Support

For issues or questions:
- Check Troubleshooting section
- Review API documentation at `/docs`
- Check logs in `app.log`
- Verify database state with SQLite browser

---

**Built with FastAPI following ICMR-NIN 2020 Guidelines**

For frontend setup, refer to `frontend/README.md`