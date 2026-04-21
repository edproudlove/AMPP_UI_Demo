import pickle
import random
import time
import streamlit as st
from utils import CorrosionPredictor

# Load the DNN
with open('DNN_5D.pkl', 'rb') as inp:
    CorrosionModel = pickle.load(inp)

def generate_random_value(min_val, max_val):
    return random.uniform(min_val, max_val)

# Init session state with random inputs for the fields if not already set
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

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    hr { margin-top: 0.5rem; margin-bottom: 0.5rem; border: 1px solid black; }
    </style>
""", unsafe_allow_html=True)


# Streamlit UI setup
st.title("DNN Surrogate Leeds Model")
st.subheader("Enter Input Conditions:")
st.markdown("---", unsafe_allow_html=True)

def create_input_row(label_text, key, min_val, max_val):
    """Create a row with a label and a number input aligned horizontally."""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<b><span style='font-size:1.1em;'>{label_text}</span></b>", unsafe_allow_html=True)
    with col2:
        st.session_state[key] = st.number_input(
            label=label_text,
            value=st.session_state[key],
            min_value=min_val,
            max_value=max_val,
            label_visibility="collapsed"
        )

create_input_row("Temperature (°C): 0 - 100", 'temperature', 0.0, 100.0)
create_input_row("CO2 Partial Pressure (Bar): 0.1 - 10", 'pressure', 0.1, 10.0)
create_input_row("pH: 5 - 6", 'pH_val', 5.0, 6.0)
create_input_row("Flow Velocity (m/s): 0.1 - 10", 'flow_vel_val', 0.1, 10.0)
create_input_row("Pipe Diameter (m): 0.01 - 1", 'pipe_diam_value', 0.01, 1.0)

st.markdown("---", unsafe_allow_html=True)

# Button to calculate corrosion rate
if st.button('Calculate Corrosion Rate'):
    with st.spinner('Calculating...'):  
        try:
            temperature = st.session_state.temperature
            pressure = st.session_state.pressure
            pH_val = st.session_state.pH_val
            flow_vel_val = st.session_state.flow_vel_val
            pipe_diam_value = st.session_state.pipe_diam_value

            # Make the prediction using the model
            corr_rate = CorrosionModel.predict_v2(P=pressure, T=temperature, d=pipe_diam_value, v=flow_vel_val, ph=pH_val)
            
            # Display the output in Streamlit
            st.success(f'Predicted Corrosion Rate: {corr_rate:.3f} mm/year')

        except Exception as e:
            st.error(f'Error: {str(e)}')
