import tensorflow as tf
import numpy as np
import json
from PIL import Image
import os

from django.conf import settings  # ✅ So we can use settings.BASE_DIR

# Paths
MODEL_PATH = os.path.join(settings.BASE_DIR, "predictor", "model", "best_food11_model.keras")
CLASS_NAMES_PATH = os.path.join(settings.BASE_DIR, "predictor", "model", "class_names.json")
NUTRITION_PATH = os.path.join(settings.BASE_DIR, "predictor", "model", "nutrition.json")

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load class names (LIST)
with open(CLASS_NAMES_PATH, "r") as f:
    class_names = json.load(f)  # Example: ["Bread", "Egg", ...]

# Load nutrition data (DICT)
try:
    with open(NUTRITION_PATH, "r") as f:
        nutrition_data = json.load(f)
except FileNotFoundError:
    nutrition_data = {}
    print("⚠️ nutrition.json file not found at:", NUTRITION_PATH)


# ✅ Prediction function
def predict_dish(image_file):
    # Prepare the image
    image = Image.open(image_file).resize((128, 128)).convert("RGB")
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Predict
    predictions = model.predict(image_array)
    predicted_index = np.argmax(predictions[0])
    predicted_label = class_names[predicted_index]
    confidence = float(predictions[0][predicted_index])  # confidence score

    return predicted_label, confidence


# ✅ Nutrition fetch function
def get_nutrition_info(dish_name):
    return nutrition_data.get(dish_name.lower(), {"error": "Nutrition info not found."})
