import streamlit as st
import matplotlib.pyplot as plt
import time
from prediction import generate_sensor_values, predict_glof_probability

# Set up Matplotlib style for a black-themed graph
plt.style.use('dark_background')

def main():
    st.set_page_config(layout="wide")  # Use the full screen
    st.title("Dynamic GLOF Probability and Parameter Dashboard")
    st.markdown("---")

    # Layout: Full-width graph for GLOF probability on top, parameter graphs below
    glof_col = st.container()
    param_cols = st.columns(4)  # Four columns for the parameter graphs

    # Placeholders for graphs
    glof_graph_placeholder = glof_col.empty()
    snowfall_graph_placeholder = st.sidebar.empty()  # Placeholder in the sidebar
    rainfall_graph_placeholder = st.sidebar.empty()  # Placeholder in the sidebar
    lake_size_graph_placeholder = st.sidebar.empty()  # Placeholder in the sidebar
    water_level_graph_placeholder = st.sidebar.empty()  # Placeholder in the sidebar

    # Fixed section for alerts and contributing sensors
    st.markdown("---")
    alert_col, sensor_col = st.columns([2, 3])
    alert_placeholder = alert_col.empty()
    sensor_placeholder = sensor_col.empty()

    # Initialize session state variables for storing history
    if "probabilities" not in st.session_state:
        st.session_state.probabilities = []
        st.session_state.snowfall_history = []
        st.session_state.rainfall_history = []
        st.session_state.lake_size_history = []
        st.session_state.water_level_history = []

    # Create initial figure for graphs
    fig_glof, ax_glof = plt.subplots(figsize=(16, 8))
    fig_snowfall, ax_snowfall = plt.subplots(figsize=(6, 4))
    fig_rainfall, ax_rainfall = plt.subplots(figsize=(6, 4))
    fig_lake_size, ax_lake_size = plt.subplots(figsize=(6, 4))
    fig_water_level, ax_water_level = plt.subplots(figsize=(6, 4))

    # Infinite loop for dynamic updates
    while True:
        # Generate new sensor values
        sensor_values = generate_sensor_values()

        # Predict GLOF probability and contributing sensors
        new_probability, contributing_sensors = predict_glof_probability(sensor_values)

        # Update probabilities and parameter history in session state
        st.session_state.probabilities.append(new_probability)
        st.session_state.snowfall_history.append(sensor_values["Snowfall_mm"])
        st.session_state.rainfall_history.append(sensor_values["Rainfall_mm"])
        st.session_state.lake_size_history.append(sensor_values["Lake_Size_km2"])
        st.session_state.water_level_history.append(sensor_values["Water_Level_m"])

        # Keep the last 20 values for plotting
        for history in [st.session_state.probabilities, st.session_state.snowfall_history, 
                        st.session_state.rainfall_history, st.session_state.lake_size_history, 
                        st.session_state.water_level_history]:
            if len(history) > 20:
                history.pop(0)

        # Update the GLOF Probability graph
        time_steps = range(len(st.session_state.probabilities))
        ax_glof.clear()
        ax_glof.plot(time_steps, st.session_state.probabilities, marker='o', linestyle='-', linewidth=2, color='cyan', label="GLOF Probability")
        ax_glof.fill_between(time_steps, st.session_state.probabilities, color='cyan', alpha=0.3)
        ax_glof.set_title("GLOF Probability Over Time", fontsize=20, color='white')
        ax_glof.set_xlabel("Time Steps", fontsize=16, color='white')
        ax_glof.set_ylabel("Probability", fontsize=16, color='white')
        ax_glof.set_ylim(0, 1)
        ax_glof.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)
        ax_glof.tick_params(colors='white')
        ax_glof.legend(loc="upper left", fontsize=14, facecolor='black', edgecolor='white')
        glof_graph_placeholder.pyplot(fig_glof)

        # Update parameter graphs in the sidebar
        for placeholder, history, ax, title, color in zip(
            [snowfall_graph_placeholder, rainfall_graph_placeholder, lake_size_graph_placeholder, water_level_graph_placeholder],
            [st.session_state.snowfall_history, st.session_state.rainfall_history, 
             st.session_state.lake_size_history, st.session_state.water_level_history],
            [ax_snowfall, ax_rainfall, ax_lake_size, ax_water_level],
            ["Snowfall (mm)", "Rainfall (mm)", "Lake Size (km²)", "Water Level (m)"],
            ['blue', 'green', 'orange', 'red']
        ):
            ax.clear()
            time_steps = range(len(history))
            ax.plot(time_steps, history, marker='o', linestyle='-', linewidth=2, color=color, label=title)
            ax.fill_between(time_steps, history, color=color, alpha=0.3)
            ax.set_title(title, fontsize=16, color='white')
            ax.set_xlabel("Time Steps", fontsize=12, color='white')
            ax.set_ylabel("Value", fontsize=12, color='white')
            ax.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)
            ax.tick_params(colors='white')
            ax.legend(loc="upper left", fontsize=10, facecolor='black', edgecolor='white')
            placeholder.pyplot(fig_snowfall if ax == ax_snowfall else fig_rainfall if ax == ax_rainfall else fig_lake_size if ax == ax_lake_size else fig_water_level)

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
