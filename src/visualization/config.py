# src/visualization/config.py

# Path configurations
PROCESSED_DIR = "data/processed"

# Dashboard configurations
DASHBOARD_TITLE = "BRFSS Diabetes Dashboard"
DASHBOARD_PORT = 8050

# Feature configurations
BINARY_FEATURES = ["HighBP", "HighChol", "Smoker", "PhysActivity", "Fruits", "Veggies", "DiffWalk"]

# Feature descriptions in Indonesian
FEATURE_DESCRIPTIONS = {
    "HighBP": "Tekanan Darah Tinggi - Menunjukkan apakah responden pernah diberitahu oleh dokter bahwa mereka memiliki tekanan darah tinggi",
    "HighChol": "Kolesterol Tinggi - Menunjukkan apakah responden pernah diberitahu oleh dokter bahwa mereka memiliki kolesterol tinggi", 
    "Smoker": "Status Merokok - Menunjukkan apakah responden pernah merokok setidaknya 100 batang rokok dalam hidupnya",
    "PhysActivity": "Aktivitas Fisik - Menunjukkan apakah responden melakukan aktivitas fisik dalam 30 hari terakhir",
    "Fruits": "Konsumsi Buah - Menunjukkan apakah responden mengonsumsi buah 1 kali atau lebih per hari",
    "Veggies": "Konsumsi Sayuran - Menunjukkan apakah responden mengonsumsi sayuran 1 kali atau lebih per hari",
    "DiffWalk": "Kesulitan Berjalan - Menunjukkan apakah responden memiliki kesulitan serius dalam berjalan atau menaiki tangga"
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

# Styling configurations - LIGHT THEME
LIGHT_THEME = {
    'backgroundColor': '#ffffff',
    'color': '#000000',
    'fontFamily': 'Arial, sans-serif'
}

CARD_STYLE = {
    'backgroundColor': '#ffffff',
    'border': '1px solid #ddd',
    'borderRadius': '8px',
    'padding': '20px',
    'margin': '10px 0',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
}

CONTAINER_STYLE = {
    'backgroundColor': '#f8f9fa',
    'minHeight': '100vh',
    'padding': '20px 150px',
    'color': '#000000',
    'fontFamily': 'Arial, sans-serif'
}