import json
import os
from django.conf import settings  # ✅ Required to access BASE_DIR safely

# ✅ Define the path first
NUTRITION_PATH = os.path.join(settings.BASE_DIR, "predictor", "model", "nutrition.json")

# ✅ Now load the file
try:
    with open(NUTRITION_PATH, "r") as f:
        nutrition_data = json.load(f)
except FileNotFoundError:
    nutrition_data = {}
    print("⚠️ nutrition.json file not found at:", NUTRITION_PATH)

# ✅ Function to get nutrition info
def get_nutrition_info(dish_name):
    return nutrition_data.get(dish_name.lower(), {"error": "Nutrition info not found."})
