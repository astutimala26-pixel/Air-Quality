import streamlit as st
import pickle
import pandas as pd

# --- 1. LOAD THE SAVED MODEL ---
try:
    # This looks for the file in the same folder
    model = pickle.load(open('air_quality_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("⚠️ Error: 'air_quality_model.pkl' not found. Make sure it is in this folder.")
    st.stop()

# --- 2. DEFINE THE HEALTH CATEGORY FUNCTION ---
# This is the exact same logic from your Colab notebook
def pm25_to_aqi(pm):
    if pm <= 12:
        return "Good", "green"
    elif pm <= 35:
        return "Moderate", "yellow"
    elif pm <= 55:
        return "Unhealthy (Sensitive)", "orange"
    elif pm <= 150:
        return "Unhealthy", "red"
    elif pm <= 200:
        return "Very Unhealthy", "purple"
    else:
        return "Hazardous", "brown"

# --- 3. BUILD THE UI ---
st.set_page_config(page_title="Air Quality Predictor", page_icon="🍃")

st.title('🍃 Air Quality Prediction System')
st.markdown("Enter the pollutant levels below to predict **PM2.5** concentration.")

# --- 4. INPUT FORM ---
# These inputs match your Colab features: ["PM10", "NO2", "SO2", "CO", "Ozone"]
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        pm10 = st.number_input('PM10 Level', min_value=0.0, value=180.0)
        no2 = st.number_input('NO2 Level', min_value=0.0, value=45.0)
        so2 = st.number_input('SO2 Level', min_value=0.0, value=20.0)
    
    with col2:
        co = st.number_input('CO Level', min_value=0.0, value=1.1)
        ozone = st.number_input('Ozone Level', min_value=0.0, value=35.0)
    
    submit_btn = st.form_submit_button("Predict Air Quality", type="primary")

# --- 5. PREDICTION LOGIC ---
if submit_btn:
    # Arrange inputs exactly as the model expects
    features = ["PM10", "NO2", "SO2", "CO", "Ozone"]
    input_data = pd.DataFrame([[pm10, no2, so2, co, ozone]], columns=features)
    
    # Get Prediction
    prediction = model.predict(input_data)
    pm25_result = prediction[0]
    
    # Get Category
    category, color = pm25_to_aqi(pm25_result)
    
    # Show Results
    st.divider()
    st.subheader("Results")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric(label="Predicted PM2.5", value=f"{pm25_result:.2f}")
    
    with col_b:
        # Display colored box based on health category
        if color == "green":
            st.success(f"Category: {category}")
        elif color == "yellow":
            st.warning(f"Category: {category}")
        else:
            st.error(f"Category: {category}")