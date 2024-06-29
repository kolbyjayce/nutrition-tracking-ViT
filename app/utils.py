import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

def save_incorrect_prediction(food_id, image_data, actual_label, nutrition_info):
    # Connect to database
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    
    # save record into table
    cursor.execute('''
    INSERT INTO incorrect_predictions (food_id, image_data, actual_label, nutrition_info)
    VALUES (?, ?, ?, ?)
    ''', (food_id, image_data, actual_label, str(nutrition_info)))
    
    # close connection
    conn.commit()
    conn.close()


def get_nutrition_info(food_label: str):
    api_key = os.getenv('USDA_API_KEY')
    if not api_key:
        raise ValueError('USDA_API_KEY not found in .env file')
    
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_label}&api_key={api_key}"

    response = requests.get(url)

    if response.status_code != 200: # api request failed
        raise ValueError(f'Failed to get nutrition info for {food_label}. {response.status_code}')
    
    data = response.json()

    if "foods" in data and len(data['foods']) > 0:
        food_data = data['foods'][0] # assume first item is correct

        food_info = {
            "fdcId": food_data.get("fdcId"),
            "description": food_data.get("description"),
            "nutrients": {nutrient["nutrientName"]: nutrient["value"]
                          for nutrient in food_data.get("foodNutrients", [])}
        }
        return food_info
    else:
        raise ValueError(f'No nutrition info found for {food_label}')
    
def preprocess_nutrition_info(raw_info):
    fdcId, description, nutrients = raw_info.items() # unpack the dictionary

    processed_info = {}
    for nutrient, value in nutrients[1].items():
        
        if nutrient == "Energy":
            nutrient = "Calories"

        if isinstance(value, dict) and 'amount' in value and 'unit' in value:
            # Convert object to string if it's a structured object
            processed_info[nutrient] = f"{value['amount']} {value['unit']}"
        else:
            # Use the value as is if it's already a simple format
            processed_info[nutrient] = value
    
    return processed_info