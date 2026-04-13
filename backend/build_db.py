import os
import pandas as pd
import json

DATA_DIR = "data"
OUTPUT_FILE = "raw_ingredients_db.json"

def get_clean_category(filename):
    """Cleans the filename to use as the food category/type."""
    name = filename.replace(".csv", "").replace(".xlsx", "").strip()
    # Optional: strip the prefix like "(A)" if you want it cleaner
    # name = name.split(")", 1)[-1] 
    return name

def parse_ifct_value(val):
    """
    Parses IFCT strings into a (mean, standard_deviation) tuple.
    Returns (float, float) for numbers, or (str, None) for text.
    """
    if pd.isna(val) or val is None:
        return None, None
    
    val_str = str(val).strip()
    
    # Handle IFCT specific text markers for zero/trace amounts
    # TR = Trace, ND = Not Detected, BLQ = Below Limit of Quant, NEG = Negligible
    if val_str.upper() in ["TR", "ND", "BLQ", "-", "", "NEG"]: 
        return 0.0, 0.0
        
    # Handle the "Mean ± SD" format
    if '±' in val_str:
        parts = val_str.split('±')
        try:
            mean = float(parts[0].strip())
            sd = float(parts[1].strip())
            return mean, sd
        except ValueError:
            return None, None
            
    # Handle standard numbers (no ± symbol)
    try:
        return float(val_str), 0.0
    except ValueError:
        # If it's pure text (like a food name or region), return it as-is
        return val_str, None

# Master dictionary to hold all food items
food_db = {}

def ingest_dataframe(df, category_name):
    """Processes a dataframe, parses values, and merges it into food_db."""
    # Standardize column names just in case of whitespace
    df.columns = df.columns.str.strip()
    
    # Check for primary keys
    code_col = next((col for col in df.columns if 'code' in col.lower()), None)
    name_col = next((col for col in df.columns if 'name' in col.lower()), None)
    
    if not code_col:
        print(f"Skipping {category_name}: No Food Code column found.")
        return

    # Replace pandas NaN with Python None for clean JSON serialization
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        f_code = str(row[code_col]).strip()
        
        # Initialize the food item if it doesn't exist yet
        if f_code not in food_db:
            food_db[f_code] = {
                "food_code": f_code,
                "food_type": category_name,
            }
            if name_col:
                food_db[f_code]["name"] = str(row[name_col]).strip()
                
        # Merge all nutritional columns
        for col in df.columns:
            if col not in [code_col, name_col]:
                raw_value = row[col]
                mean_val, sd_val = parse_ifct_value(raw_value)
                
                # Create safe JSON keys (e.g., "Protein (g)" -> "protein_g")
                safe_col_name = col.lower().replace(" ", "_").replace("(", "").replace(")", "").strip()
                
                if mean_val is not None:
                    # If it's text, just save the string
                    if isinstance(mean_val, str):
                        food_db[f_code][safe_col_name] = mean_val
                    else:
                        # Save numeric mean and SD
                        food_db[f_code][f"{safe_col_name}_mean"] = mean_val
                        food_db[f_code][f"{safe_col_name}_sd"] = sd_val

# ==========================================
# 1. Process CSV Folders (Tables 3 to 6)
# ==========================================
csv_tables = ["data_table_3", "data_table_4", "data_table_5", "data_table_6"]

for table_folder in csv_tables:
    folder_path = os.path.join(DATA_DIR, table_folder)
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)
                category = get_clean_category(file)
                try:
                    df = pd.read_csv(file_path)
                    ingest_dataframe(df, category)
                    print(f"Ingested CSV: {category}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    else:
        print(f"Warning: Directory '{folder_path}' not found.")

# ==========================================
# 2. Process Excel Files (Table 8)
# ==========================================
excel_files = ["Table 8.xlsx","Table 11.xlsx","Table 1.xlsx"]  # List of Excel files to process

for excel_file in excel_files:
    file_path = os.path.join(DATA_DIR, excel_file)
    if os.path.exists(file_path):
        try:
            # Read all sheets into a dictionary of DataFrames
            sheets = pd.read_excel(file_path, sheet_name=None)
            for sheet_name, df in sheets.items():
                category = get_clean_category(sheet_name)
                ingest_dataframe(df, category)
                print(f"Ingested Sheet: {category} from {excel_file}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    else:
        print(f"Warning: File '{file_path}' not found.")

# ==========================================
# 3. Export to JSON
# ==========================================
final_db_list = list(food_db.values())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_db_list, f, indent=4)

print("-" * 40)
print(f"Extraction complete! Merged {len(final_db_list)} items into {OUTPUT_FILE}")