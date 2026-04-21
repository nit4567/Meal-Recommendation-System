import requests
import json
import time
import os

BASE_URL = "http://localhost:8000"
OUTPUT_DIR = "test_outputs"

# Ensure folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_disease_test(case_name, conditions, output_filename):
    print(f"\n==========================================")
    print(f"🧪 RUNNING TEST: {case_name.upper()}")
    print(f"==========================================")
    
    # 1. Create a unique user for this test
    test_email = f"user_{case_name.lower().replace(' ', '_')}_{int(time.time())}@iitkgp.edu"
    
    print(f"[*] Registering user: {test_email}")
    signup_res = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": test_email,
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": case_name
    })
    
    if signup_res.status_code != 200:
        print(f"❌ Signup Failed: {signup_res.text}")
        return
        
    token = signup_res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Setup Profile with specific diseases
    print(f"[*] Setting medical conditions: {conditions}")
    profile_payload = {
        "age": 25, "gender": "male", "height_cm": 175.0, "weight_kg": 70.0,
        "region": "North", "dietary_preference": "vegetarian", 
        "activity_level": "moderate", "goal": "maintenance",
        "medical_conditions": conditions, 
        "allergies": [], "mood": "good"
    }
    
    prof_res = requests.post(f"{BASE_URL}/profile", json=profile_payload, headers=headers)
    if prof_res.status_code != 200:
        print(f"❌ Profile Creation Failed: {prof_res.text}")
        return
        
    # 3. Generate the Plan via AI
    print("[*] Generating AI Weekly Plan (Calling Groq)...")
    plan_res = requests.post(f"{BASE_URL}/calculations/generate-ai-plan", headers=headers)
    
    if plan_res.status_code == 200:
        data = plan_res.json()
        print("✅ Success! Plan generated.")
        
        # 4. Save to test_outputs folder
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
            
        print(f"💾 Saved to {output_path}")
    else:
        print(f"❌ Plan Gen Failed: {plan_res.text}")

if __name__ == "__main__":
    print("🚀 Starting VegitaMeal Clinical Validation Suite...\n")
    
    # Run the 5 Core Cases
    run_disease_test("Baseline Healthy", [], "test_1_baseline.json")
    run_disease_test("Hypertension", ["hypertension"], "test_2_hypertension.json")
    run_disease_test("Thyroid", ["thyroid"], "test_3_thyroid.json")
    run_disease_test("Obesity", ["obesity"], "test_4_obesity.json")
    run_disease_test("Constipation", ["constipation"], "test_5_constipation.json")
    
    print("\n🎉 All tests complete! Check the 'test_outputs' folder.")