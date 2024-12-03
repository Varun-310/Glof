import xgboost as xgb
import pandas as pd
import random

# Load the trained model
def load_model():
    model = xgb.XGBClassifier()
    model.load_model("models/glof_prediction_model.pkl")
    return model

# Generate random sensor data
def generate_sensor_data():
    return {
        "Lake_Size_km2": round(random.uniform(0.5, 5.0), 2),
        "Water_Level_m": round(random.uniform(0.1, 10.0), 2),
        "Air_Temperature_C": round(random.uniform(-10.0, 35.0), 2),
        "Flow_Rate_m3_per_s": round(random.uniform(0.5, 50.0), 2),
        "Ground_Movement_mm": round(random.uniform(0.0, 5.0), 2),
        "Dam_Pressure_MPa": round(random.uniform(1.0, 10.0), 2),
        "Precipitation_mm": round(random.uniform(0.0, 100.0), 2),
        "Sensor_Accuracy_%": round(random.uniform(90.0, 100.0), 2),
        "Lake_Perimeter_Change_m": round(random.uniform(0.0, 2.0), 2),
        "Snowpack_Thickness_m": round(random.uniform(0.0, 5.0), 2),
        "Soil_Moisture_Content_%": round(random.uniform(0.0, 100.0), 2),
        "Solar_Radiation_W_per_m2": round(random.uniform(100.0, 1000.0), 2),
        "Water_Temperature_C": round(random.uniform(0.0, 30.0), 2),
        "Water_Turbidity_NTU": round(random.uniform(0.0, 10.0), 2),
        "Wind_Speed_m_per_s": round(random.uniform(0.0, 15.0), 2),
        "Rainfall_mm": round(random.uniform(0.0, 200.0), 2),
        "Snowfall_mm": round(random.uniform(0.0, 200.0), 2),
    }

# Simulate continuous prediction
def simulate_continuous_prediction():
    sensor_data = {
        "Lake Size (km²)": 3.5,
        "Water Level (m)": 15.2,
        "Air Temperature (°C)": 2.8,
        "Flow Rate (m³/s)": 12.4,
        "Ground Movement (mm)": 0.5,
        "Dam Pressure (MPa)": 3.2,
        "Precipitation (mm)": 8.3,
        "Sensor Accuracy (%)": 98.7,
        "Lake Perimeter Change (m)": 1.3,
        "Snowpack Thickness (m)": 1.5,
        "Soil Moisture Content (%)": 18.9,
        "Solar Radiation (W/m²)": 700,
        "Water Temperature (°C)": 4.1,
        "Water Turbidity (NTU)": 0.7,
        "Wind Speed (m/s)": 5.3,
        "Rainfall (mm)": 12.7,
        "Snowfall (mm)": 3.4,
    }
    glof_probability = 0.6  # Example probability value
    future_prediction = 0.75  # Example future prediction value
    return sensor_data, glof_probability, future_prediction

