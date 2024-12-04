import numpy as np
import pandas as pd
import xgboost as xgb
import random

# Load the trained model
model = xgb.XGBClassifier()
model.load_model("models/glof_prediction_model.pkl")  # Ensure the path is correct

# Function to generate sensor values dynamically
class SensorSimulator:
    def __init__(self, initial_values):
        self.values = initial_values
        self.trend = {key: random.uniform(-0.1, 0.1) for key in initial_values.keys()}  # Small gradual trends

    def update(self):
        new_values = {}
        for sensor, value in self.values.items():
            # Gradual increase/decrease
            change = self.trend[sensor] + random.uniform(-0.05, 0.05)  # Add some random noise
            new_value = value + change
            
            # Add occasional spikes
            if random.random() < 0.02:  # 2% chance for a spike
                spike = random.uniform(-1, 1)
                new_value += spike
            
            # Clamp values within realistic ranges (adjust ranges per sensor type)
            if sensor == "Lake_Size_km2":
                new_value = max(0, min(new_value, 5))  # Example: 0 to 5 km²
            elif sensor == "Air_Temperature_C":
                new_value = max(-20, min(new_value, 40))  # Example: -20°C to 40°C
            elif sensor == "Water_Level_m":
                new_value = max(0, min(new_value, 50))  # Example: 0 to 50 meters
            # Add more conditions for other sensors if needed
            
            new_values[sensor] = new_value
        
        self.values = new_values
        return self.values

# Initialize the simulator with initial sensor values
initial_sensor_values = {
    "Lake_Size_km2": 2.0,
    "Air_Temperature_C": 15.0,
    "Water_Level_m": 10.0,
    "Flow_Rate_m3_per_s": 50.0,
    "Ground_Movement_mm": 0.2,
    "Dam_Pressure_MPa": 2.0,
    "Precipitation_mm": 1.0,
    "Snowpack_Thickness_m": 0.5,
    "Soil_Moisture_Content_%": 20.0,
    "Solar_Radiation_W_per_m2": 200.0,
    "Water_Temperature_C": 5.0,
    "Water_Turbidity_NTU": 10.0,
    "Wind_Speed_m_per_s": 2.0,
    "Rainfall_mm": 0.0,
    "Snowfall_mm": 0.0,
}

sensor_simulator = SensorSimulator(initial_sensor_values)

# Function to predict GLOF probability
def predict_glof_probability(sensor_values):
    input_df = pd.DataFrame([sensor_values])
    
    # Predict probability
    probabilities = model.predict_proba(input_df)
    probability = probabilities[0, 1]  # Extract probability of GLOF occurrence (class 1)
    
    # Identify contributing sensors by feature importance
    feature_importance = model.get_booster().get_score(importance_type='weight')
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    top_features = [item[0] for item in sorted_features[:3]]  # Top 3 features
    
    return float(probability), top_features

