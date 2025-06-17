# src/visualization/config.py

# Path configurations
PROCESSED_DIR = "data/processed"

# Dashboard configurations
DASHBOARD_TITLE = "BRFSS Diabetes Dashboard"
DASHBOARD_PORT = 8050

# Feature configurations
BINARY_FEATURES = ["HighBP", "HighChol", "Smoker", "PhysActivity", "Fruits", "Veggies", "DiffWalk"]

# Feature descriptions (you can edit these)
FEATURE_DESCRIPTIONS = {
    "HighBP": "High Blood Pressure - Indicates whether respondent has been told they have high blood pressure by a doctor",
    "HighChol": "High Cholesterol - Indicates whether respondent has been told they have high cholesterol by a doctor", 
    "Smoker": "Smoking Status - Indicates whether respondent has smoked at least 100 cigarettes in their entire life",
    "PhysActivity": "Physical Activity - Indicates whether respondent had physical activity in past 30 days",
    "Fruits": "Fruit Consumption - Indicates whether respondent consumes fruit 1 or more times per day",
    "Veggies": "Vegetable Consumption - Indicates whether respondent consumes vegetables 1 or more times per day",
    "DiffWalk": "Difficulty Walking - Indicates whether respondent has serious difficulty walking or climbing stairs"
}

# Age category descriptions (you can edit these)
AGE_DESCRIPTIONS = {
    1: "1: Age 18-24 (Young Adults)",
    2: "2: Age 25-29 (Young Adults)",
    3: "3: Age 30-34 (Early Career)",
    4: "4: Age 35-39 (Early Career)",
    5: "5: Age 40-44 (Mid Career)",
    6: "6: Age 45-49 (Mid Career)",
    7: "7: Age 50-54 (Pre-retirement)",
    8: "8: Age 55-59 (Pre-retirement)",
    9: "9: Age 60-64 (Early Senior)",
    10: "10: Age 65-69 (Senior)",
    11: "11: Age 70-74 (Senior)",
    12: "12: Age 75-79 (Elderly)",
    13: "13: Age 80+ (Elderly)"
}

# Styling configurations
DARK_THEME = {
    'backgroundColor': '#1e1e1e',
    'color': '#ffffff',
    'fontFamily': 'Arial, sans-serif'
}

CARD_STYLE = {
    'backgroundColor': '#2d2d2d',
    'border': '1px solid #444',
    'borderRadius': '8px',
    'padding': '20px',
    'margin': '10px 0',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.3)'
}

CONTAINER_STYLE = {
    'backgroundColor': '#1e1e1e',
    'minHeight': '100vh',
    'padding': '20px 150px',
    'color': '#ffffff',
    'fontFamily': 'Arial, sans-serif'
}
