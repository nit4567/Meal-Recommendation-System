# ICMR Nutrition Planner - Frontend

A clean, modular React application for personalized nutrition planning based on ICMR-NIN 2020 guidelines.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Scripts](#available-scripts)
- [Architecture](#architecture)
- [Components Overview](#components-overview)
- [API Integration](#api-integration)
- [Styling](#styling)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

```bash
# 1. Create React app
npx create-react-app frontend
cd frontend

# 2. Install dependencies
npm install react-router-dom axios lucide-react
npm install -D tailwindcss postcss autoprefixer

# 3. Initialize Tailwind
npx tailwindcss init -p

# 4. Create directory structure
mkdir -p src/api src/auth src/components/common src/components/layout src/components/dashboard
mkdir -p src/pages/auth src/pages/profile src/pages/dashboard
mkdir -p src/hooks src/utils src/constants

# 5. Copy all files from artifacts to respective locations

# 6. Configure Tailwind (see Configuration section)

# 7. Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# 8. Start development server
npm start
```

---

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html
│
├── src/
│   ├── api/                          # API Layer (Backend Communication)
│   │   ├── axios.config.js          # Axios instance with interceptors
│   │   ├── endpoints.js             # API endpoint URLs
│   │   ├── auth.api.js              # Authentication API calls
│   │   ├── profile.api.js           # Profile API calls
│   │   └── calculation.api.js       # Calculation API calls
│   │
│   ├── auth/                         # Authentication Layer
│   │   ├── AuthContext.jsx          # React context for auth
│   │   ├── AuthProvider.jsx         # Auth state management
│   │   ├── useAuth.js               # Custom auth hook
│   │   ├── PrivateRoute.jsx         # Protected route wrapper
│   │   └── PublicRoute.jsx          # Public route wrapper
│   │
│   ├── components/
│   │   ├── common/                  # Reusable Components
│   │   │   ├── Button.jsx           # Button with variants
│   │   │   ├── Input.jsx            # Input with validation
│   │   │   ├── Select.jsx           # Select dropdown
│   │   │   ├── Card.jsx             # Card container
│   │   │   ├── Loading.jsx          # Loading spinner
│   │   │   ├── ErrorMessage.jsx     # Error display
│   │   │   └── ToggleButton.jsx     # Toggle selection button
│   │   │
│   │   ├── layout/                  # Layout Components
│   │   │   ├── Navbar.jsx           # Top navigation
│   │   │   ├── PageContainer.jsx    # Page wrapper
│   │   │   └── Footer.jsx           # Footer
│   │   │
│   │   └── dashboard/               # Dashboard Components
│   │       ├── BMICard.jsx          # BMI display card
│   │       ├── CalorieCard.jsx      # Calorie target card
│   │       ├── NutrientCard.jsx     # Individual nutrient card
│   │       ├── AdditionalNutrients.jsx  # Additional nutrients
│   │       ├── HealthAlert.jsx      # Health warnings
│   │       └── ComingSoon.jsx       # Coming soon section
│   │
│   ├── pages/                        # Page Components
│   │   ├── auth/
│   │   │   ├── LoginPage.jsx        # Login page
│   │   │   └── SignupPage.jsx       # Signup page
│   │   ├── profile/
│   │   │   └── ProfileWizard.jsx    # Profile creation/editing
│   │   └── dashboard/
│   │       └── Dashboard.jsx        # Main dashboard
│   │
│   ├── hooks/                        # Custom React Hooks
│   │   ├── useProfile.js            # Profile data hook
│   │   ├── useCalculation.js        # Calculation data hook
│   │   └── useForm.js               # Form state management
│   │
│   ├── utils/                        # Helper Functions
│   │   ├── icmr.calculations.js     # ICMR calculation logic
│   │   ├── formatters.js            # Data formatters
│   │   └── validation.js            # Validation helpers
│   │
│   ├── constants/                    # Constants
│   │   ├── routes.js                # Route paths
│   │   ├── options.js               # Dropdown options
│   │   └── messages.js              # UI messages
│   │
│   ├── App.jsx                       # Main app component
│   ├── routes.jsx                    # Route configuration
│   ├── index.js                      # Entry point
│   └── index.css                     # Global styles
│
├── .env                              # Environment variables
├── .gitignore
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

---

## ✨ Features

### Authentication
- ✅ JWT-based authentication
- ✅ Login and signup flows
- ✅ Protected and public routes
- ✅ Automatic token management
- ✅ Persistent sessions

### Profile Management
- ✅ 3-step profile wizard
- ✅ Basic info (age, gender, height, weight)
- ✅ Lifestyle preferences (activity, diet, region)
- ✅ Health goals and medical conditions
- ✅ Profile editing capability

### Nutrition Dashboard
- ✅ BMI calculation with Indian standards
- ✅ Daily calorie targets (BMR × PAL)
- ✅ Protein, Iron, Calcium targets
- ✅ Fiber and essential fatty acids
- ✅ Health condition adjustments
- ✅ ICMR 2020 compliant calculations

### UI/UX
- ✅ Clean white theme with purple accents
- ✅ Responsive design (mobile-friendly)
- ✅ Loading states
- ✅ Error handling
- ✅ Form validation

---

## 📦 Installation

### Prerequisites
- Node.js 14+ and npm
- Backend API running on port 8000

### Step-by-Step

1. **Install Dependencies**
```bash
npm install react-router-dom axios lucide-react
npm install -D tailwindcss postcss autoprefixer
```

2. **Configure Tailwind CSS**

Update `tailwind.config.js`:
```javascript
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Create `postcss.config.js`:
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

3. **Update `src/index.css`**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
}

::-webkit-scrollbar-thumb {
  background: rgba(168, 85, 247, 0.5);
  border-radius: 4px;
}

input[type='number']::-webkit-inner-spin-button,
input[type='number']::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type='number'] {
  -moz-appearance: textfield;
}
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in root:
```bash
REACT_APP_API_URL=http://localhost:8000
```

**For Production:**
```bash
REACT_APP_API_URL=https://your-backend-api.com
```

---

## 📜 Available Scripts

```bash
# Start development server (localhost:3000)
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject from create-react-app (irreversible)
npm run eject
```

---

## 🏗️ Architecture

### Layer Separation

```
┌─────────────────────────────────────────┐
│           Pages (Routes)                │
│  LoginPage, Dashboard, ProfileWizard    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Components (UI)                 │
│  Navbar, Cards, Buttons, Forms          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Custom Hooks (Logic)               │
│  useProfile, useCalculation, useAuth    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         API Layer (Backend)             │
│  axios, endpoints, API functions        │
└─────────────────────────────────────────┘
```

### Data Flow

```
User Action
    ↓
Page Component
    ↓
Custom Hook (useProfile, useCalculation)
    ↓
API Function (profileAPI.get, calculationAPI.getLatest)
    ↓
Axios Instance (with auth token)
    ↓
Backend API
    ↓
Response
    ↓
Format Data (formatters.js)
    ↓
Update State
    ↓
Re-render UI
```

---

## 🧩 Components Overview

### Common Components

| Component | Purpose | Props |
|-----------|---------|-------|
| `Button` | Reusable button | variant, size, loading, fullWidth |
| `Input` | Form input with validation | label, type, error, onChange |
| `Select` | Dropdown select | options, value, onChange |
| `Card` | Container card | hover, className |
| `Loading` | Loading spinner | message |
| `ErrorMessage` | Error display | message, onRetry |
| `ToggleButton` | Selection button | isSelected, onClick, icon |

### Dashboard Components

| Component | Purpose | Data Required |
|-----------|---------|---------------|
| `BMICard` | Display BMI info | bmi, profile, goal |
| `CalorieCard` | Show calorie target | dailyCalories, bmr, tee |
| `NutrientCard` | Individual nutrient | title, value, unit, color |
| `AdditionalNutrients` | Fiber, fats | fiber, visibleFat, omega-3/6 |
| `HealthAlert` | Medical warnings | medicalConditions, allergies |

---

## 🔌 API Integration

### API Structure

All API calls are in `src/api/`:

```javascript
// Example: Get profile
import { profileAPI } from '../api/profile.api';

const data = await profileAPI.getProfile();
```

### Available APIs

**Authentication:**
```javascript
authAPI.signup(data)
authAPI.login(credentials)
authAPI.getCurrentUser()
```

**Profile:**
```javascript
profileAPI.createProfile(profileData)
profileAPI.getProfile()
profileAPI.updateProfile(profileData)
```

**Calculations:**
```javascript
calculationAPI.getLatestCalculation()
calculationAPI.getCalculationHistory(limit)
calculationAPI.recalculate()
```

### Axios Configuration

All requests automatically include:
- ✅ JWT token in Authorization header
- ✅ Content-Type: application/json
- ✅ 10-second timeout
- ✅ Auto-redirect on 401 (token expired)

---

## 🎨 Styling

### Theme

**Color Palette:**
- **Primary**: Purple-Blue gradient (`from-purple-600 to-blue-600`)
- **Background**: White / Light gray (`bg-white`, `bg-gray-50`)
- **Text**: Gray scale (`text-gray-900`, `text-gray-600`)
- **Borders**: `border-gray-200`
- **Accents**: Purple/Blue for highlights

**Typography:**
- Font: System fonts (Apple, Segoe UI, Roboto)
- Headings: `text-2xl font-bold`
- Body: `text-base`
- Small: `text-sm`

### Responsive Design

```css
/* Mobile first approach */
grid-cols-1          /* Mobile */
md:grid-cols-2       /* Tablet */
lg:grid-cols-3       /* Desktop */
```

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output will be in `build/` directory.

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable in Vercel dashboard
REACT_APP_API_URL=https://your-backend.com
```

### Deploy to Netlify

```bash
# Build
npm run build

# Deploy build/ directory to Netlify

# Set environment variable in Netlify settings
REACT_APP_API_URL=https://your-backend.com
```

### Important: CORS

Make sure backend allows your frontend domain:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Issue: Cannot connect to backend

**Symptoms:** Network error, requests failing

**Solution:**
1. Check backend is running: `http://localhost:8000`
2. Verify `.env` file exists with correct URL
3. Check CORS is enabled in backend
4. Clear browser cache and restart dev server

### Issue: Token expired / 401 errors

**Symptoms:** Automatic logout, 401 responses

**Solution:**
```javascript
// Clear localStorage and login again
localStorage.clear();
// Then login again
```

### Issue: Styles not applying

**Symptoms:** No styling, plain HTML

**Solution:**
1. Verify Tailwind is installed: `npm list tailwindcss`
2. Check `tailwind.config.js` content paths
3. Ensure `index.css` has `@tailwind` directives
4. Restart dev server: `npm start`

### Issue: Component not found

**Symptoms:** Module not found error

**Solution:**
1. Check file path (case-sensitive)
2. Verify file has correct export
3. Check import statement matches file location

### Issue: Profile not loading

**Symptoms:** Redirected to profile wizard, "Profile not found"

**Solution:**
1. Complete profile wizard first
2. Check backend has `user_profiles` table
3. Verify API token is valid

---

## 📚 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `react` | ^18.2.0 | UI library |
| `react-router-dom` | ^6.20.0 | Routing |
| `axios` | ^1.6.2 | HTTP client |
| `lucide-react` | ^0.294.0 | Icons |
| `tailwindcss` | ^3.3.5 | CSS framework |

---

## 🧪 Testing

```bash
# Run tests
npm test

# With coverage
npm test -- --coverage
```

### Manual Testing Checklist

- [ ] Signup creates new account
- [ ] Login authenticates user
- [ ] Dashboard loads after login
- [ ] Profile wizard saves data
- [ ] Edit profile updates successfully
- [ ] Logout clears session
- [ ] Protected routes redirect to login
- [ ] Calculation values are correct
- [ ] Responsive on mobile devices
- [ ] Error messages display properly

---

## 📖 Additional Resources

- **React Documentation**: https://react.dev
- **React Router**: https://reactrouter.com
- **Tailwind CSS**: https://tailwindcss.com
- **Axios**: https://axios-http.com
- **ICMR Guidelines**: Refer to attached PDF document

---

## 👥 Contributing

When adding new features:

1. **New Page**: Add in `src/pages/`, update `routes.jsx`
2. **New API**: Add in `src/api/`, add endpoint in `endpoints.js`
3. **New Component**: Add in appropriate `src/components/` folder
4. **New Hook**: Add in `src/hooks/`
5. **New Utility**: Add in `src/utils/`

Maintain the clean architecture and separation of concerns!

---

---

## 🎯 Next Steps (Phase 2 & 3)

- [ ] Add ingredients database integration
- [ ] Implement meal recommendation system
- [ ] Add calculation history page
- [ ] Add meal plan generation
- [ ] Add progress tracking
- [ ] Add food diary

---
