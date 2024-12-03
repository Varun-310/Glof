import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Set up Matplotlib style for a black-themed graph
plt.style.use('dark_background')

# Streamlit app setup
st.set_page_config(page_title="Dynamic GLOF Probability Dashboard", layout="wide")

# Function to generate random probabilities
def generate_random_probability():
    return np.random.uniform(0, 1)

# Function to determine responsible parameters for the probability increase
def determine_responsible_parameters():
    parameters = [
        "Lake Size (km²)", "Water Level (m)", "Air Temperature (°C)",
        "Flow Rate (m³/s)", "Ground Movement (mm)", "Dam Pressure (MPa)",
        "Precipitation (mm)", "Sensor Accuracy (%)", "Lake Perimeter Change (m)",
        "Snowpack Thickness (m)", "Soil Moisture Content (%)",
        "Solar Radiation (W/m²)", "Water Temperature (°C)", "Water Turbidity (NTU)",
        "Wind Speed (m/s)", "Rainfall (mm)", "Snowfall (mm)"
    ]
    num_parameters = np.random.randint(1, 4)  # Randomly pick 1-3 parameters
    return np.random.choice(parameters, num_parameters, replace=False)

# Main app function
def main():
    st.title("Dynamic GLOF Probability Dashboard")
    st.markdown("---")

    # Create two columns: one for graph and one for side info
    col1, col2 = st.columns([3, 1])

    # Placeholder for the graph
    graph_placeholder = col1.empty()

    # Fixed section for contributing parameters and alerts
    with col2:
        st.markdown("### Contributing Parameters")
        parameters_placeholder = st.empty()
        st.markdown("### Alerts")
        alert_placeholder = st.empty()

    # Initialize probabilities
    probabilities = []

    # Infinite loop for dynamic updates
    while True:
        # Generate new probability
        new_probability = generate_random_probability()
        probabilities.append(new_probability)

        # Keep the last 20 probabilities
        if len(probabilities) > 20:
            probabilities = probabilities[-20:]

        # Determine responsible parameters
        responsible_parameters = determine_responsible_parameters()

        # Update the graph
        with graph_placeholder.container():
            fig, ax = plt.subplots(figsize=(14, 6))
            time_steps = np.arange(len(probabilities))
            ax.plot(time_steps, probabilities, marker='o', linestyle='-', linewidth=2, color='cyan', label="GLOF Probability")
            ax.fill_between(time_steps, probabilities, color='cyan', alpha=0.3)
            ax.set_title("GLOF Probability Over Time", fontsize=18, color='white')
            ax.set_xlabel("Time Steps", fontsize=14, color='white')
            ax.set_ylabel("Probability", fontsize=14, color='white')
            ax.set_ylim(0, 1)
            ax.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)
            ax.tick_params(colors='white')
            ax.legend(loc="upper left", fontsize=12, facecolor='black', edgecolor='white')
            st.pyplot(fig)

        # Update contributing parameters
        parameters_placeholder.markdown(
            f"**Parameters contributing to change:** {', '.join(responsible_parameters)}"
        )

        # Update alert if probability is high
        if new_probability > 0.7:
            alert_placeholder.warning("⚠️ **High Risk Detected! Immediate action is recommended.**")
        else:
            alert_placeholder.info("✅ Risk is under control.")

        # Pause for 2 seconds before updating
        time.sleep(2)

if __name__ == "__main__":
    main()
