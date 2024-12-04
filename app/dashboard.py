import streamlit as st
import matplotlib.pyplot as plt
import time
from prediction import generate_sensor_values, predict_glof_probability

# Set up Matplotlib style for a black-themed graph
plt.style.use('dark_background')

def main():
    st.set_page_config(layout="wide")  # Use the full screen
    st.title("Dynamic GLOF Probability Dashboard")
    st.markdown("---")

    # Layout: Two columns, full graph on the left, alerts and contributing sensors on the right
    col1, col2 = st.columns([4, 1])

    # Placeholder for the graph
    graph_placeholder = col1.empty()

    # Fixed section for contributing parameters and alerts
    with col2:
        st.markdown("### Alerts")
        alert_placeholder = st.empty()
        st.markdown("### Contributing Sensors")
        sensor_placeholder = st.empty()

    # Initialize probabilities
    probabilities = []

    # Infinite loop for dynamic updates
    while True:
        # Generate new sensor values
        sensor_values = generate_sensor_values()

        # Predict GLOF probability and contributing sensors
        new_probability, contributing_sensors = predict_glof_probability(sensor_values)
        probabilities.append(new_probability)

        # Keep the last 20 probabilities
        if len(probabilities) > 20:
            probabilities = probabilities[-20:]

        # Update the graph
        with graph_placeholder.container():
            fig, ax = plt.subplots(figsize=(16, 8))  # Larger graph
            time_steps = range(len(probabilities))
            ax.plot(time_steps, probabilities, marker='o', linestyle='-', linewidth=2, color='cyan', label="GLOF Probability")
            ax.fill_between(time_steps, probabilities, color='cyan', alpha=0.3)
            ax.set_title("GLOF Probability Over Time", fontsize=20, color='white')
            ax.set_xlabel("Time Steps", fontsize=16, color='white')
            ax.set_ylabel("Probability", fontsize=16, color='white')
            ax.set_ylim(0, 1)
            ax.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)
            ax.tick_params(colors='white')
            ax.legend(loc="upper left", fontsize=14, facecolor='black', edgecolor='white')
            st.pyplot(fig)

        # Update alert if probability is high
        if new_probability > 0.7:
            alert_placeholder.warning("⚠️ **High Risk Detected! Immediate action is recommended.**")
        else:
            alert_placeholder.info("✅ Risk is under control.")

        # Update contributing sensors
        sensor_placeholder.markdown(f"**Top Contributing Parameters:**\n- {', '.join(contributing_sensors)}")

        # Pause for 2 seconds before updating
        time.sleep(2)

if __name__ == "__main__":
    main()
