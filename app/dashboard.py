import streamlit as st
import plotly.graph_objects as go
from prediction import simulate_continuous_prediction
import random
import time

# Set wide layout
st.set_page_config(layout="wide")

# Title of the Dashboard
st.title("GLOF Prediction Dashboard")

# Fixed sensor data
st.subheader("Sensor Data (Fixed Values)")
sensor_data, _, _ = simulate_continuous_prediction()

# Display sensor data in fixed boxes
sensor_cols = st.columns(len(sensor_data))
for i, (key, value) in enumerate(sensor_data.items()):
    sensor_cols[i].metric(key, f"{value:.2f}")

# Dynamic graph section
st.subheader("Dynamic GLOF Occurrence Probability Graph")

# Placeholder for dynamic graph
graph_placeholder = st.empty()

# Initialize dynamic graph data
time_steps = list(range(10))  # Fixed 10 time steps for visualization
dynamic_probabilities = [random.uniform(0.2, 0.5) for _ in range(10)]

# Continuous updates for the graph
for _ in range(50):  # Simulate 50 iterations for dynamic updates
    # Simulate dynamic probability changes
    new_probability = dynamic_probabilities[-1] + random.uniform(-0.05, 0.05)
    new_probability = max(0.0, min(new_probability, 1.0))  # Clamp within [0, 1]
    dynamic_probabilities.append(new_probability)
    dynamic_probabilities.pop(0)  # Keep the list size fixed to 10

    # Create the graph
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time_steps,
            y=dynamic_probabilities,
            mode="lines+markers",
            name="GLOF Probability",
        )
    )
    fig.update_layout(
        title="Dynamic GLOF Occurrence Probability",
        xaxis_title="Time Step",
        yaxis_title="Probability",
        yaxis_range=[0, 1],
    )

    # Render the graph
    graph_placeholder.plotly_chart(fig, use_container_width=True)

    # Show alert if probability exceeds 75%
    if new_probability > 0.75:
        st.error("⚠️ ALERT: High Probability of GLOF Occurrence!")

    time.sleep(1)  # Real-time simulation (1-second interval)
