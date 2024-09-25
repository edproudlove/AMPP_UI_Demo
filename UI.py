import pickle
import random
import time
import streamlit as st
from utils import CorrosionPredictor

# Load the model
with open('DNN_5D.pkl', 'rb') as inp:
    CorrosionModel = pickle.load(inp)

# Function to generate random values
def generate_random_value(min_val, max_val):
    return random.uniform(min_val, max_val)

# Initialize session state for the input fields if not already set
if 'temperature' not in st.session_state:
    st.session_state.temperature = generate_random_value(0, 100)
if 'pressure' not in st.session_state:
    st.session_state.pressure = generate_random_value(0.1, 10)
if 'pH_val' not in st.session_state:
    st.session_state.pH_val = generate_random_value(5, 6)
if 'flow_vel_val' not in st.session_state:
    st.session_state.flow_vel_val = generate_random_value(0.1, 10)
if 'pipe_diam_value' not in st.session_state:
    st.session_state.pipe_diam_value = generate_random_value(0.01, 1)

# Streamlit UI setup
st.title("DNN Surrogate Leeds Model")
st.subheader("Enter Input Conditions")

# Input fields with session state values (so user input is retained)
st.session_state.temperature = st.number_input('Temperature (°C): 0 - 100', value=st.session_state.temperature, min_value=0.0, max_value=100.0)
st.session_state.pressure = st.number_input('Pressure (Bar): 0.1 - 10', value=st.session_state.pressure, min_value=0.1, max_value=10.0)
st.session_state.pH_val = st.number_input('pH: 5 - 6', value=st.session_state.pH_val, min_value=5.0, max_value=6.0)
st.session_state.flow_vel_val = st.number_input('Flow Velocity (m/s): 0.1 - 10', value=st.session_state.flow_vel_val, min_value=0.1, max_value=10.0)
st.session_state.pipe_diam_value = st.number_input('Pipe Diameter (m): 0.01 - 1', value=st.session_state.pipe_diam_value, min_value=0.01, max_value=1.0)

# Button to calculate corrosion rate
if st.button('Calculate Corrosion Rate'):
    start_time = time.time()

    try:
        # Use the values stored in session state
        temperature = st.session_state.temperature
        pressure = st.session_state.pressure
        pH_val = st.session_state.pH_val
        flow_vel_val = st.session_state.flow_vel_val
        pipe_diam_value = st.session_state.pipe_diam_value
        
        # Make the prediction using the model
        corr_rate = CorrosionModel.predict_v2(P=pressure, T=temperature, d=pipe_diam_value, v=flow_vel_val, ph=pH_val)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Display the output in Streamlit
        st.success(f'Corrosion Rate: {corr_rate:.3f} mm/year')
        st.info(f'Response Time: {elapsed_time:.3f} seconds')

    except Exception as e:
        st.error(f'Error: {str(e)}')