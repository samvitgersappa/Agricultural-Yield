import streamlit as st
import joblib
import requests
from PIL import Image
from io import BytesIO


# Load the trained model
#model = pickle.load(open('trained_model.pkl', 'rb'))
model = joblib.load('trained_model.pkl')

# Dictionary mapping integer values to crop names
crop_map = {
    1: 'Arecanut', 2: 'Arhar/Tur', 3: 'Castor seed', 4: 'Coconut',
    5: 'Cotton(lint)', 6: 'Dry chillies', 7: 'Gram', 8: 'Jute', 9: 'Linseed',
    10: 'Maize', 11: 'Mesta', 12: 'Niger seed', 13: 'Onion', 14: 'Other Rabi pulses',
    15: 'Potato', 16: 'Rapeseed & Mustard', 17: 'Rice', 18: 'Sesamum',
    19: 'Small millets', 20: 'Sugarcane', 21: 'Sweet potato', 22: 'Tapioca',
    23: 'Tobacco', 24: 'Turmeric', 25: 'Wheat', 26: 'Bajra', 27: 'Black pepper',
    28: 'Cardamom', 29: 'Coriander', 30: 'Garlic', 31: 'Ginger', 32: 'Groundnut',
    33: 'Horse-gram', 34: 'Jowar', 35: 'Ragi', 36: 'Cashewnut', 37: 'Banana',
    38: 'Soyabean', 39: 'Barley', 40: 'Khesari', 41: 'Masoor', 42: 'Moong(Green Gram)',
    43: 'Other Kharif pulses', 44: 'Safflower', 45: 'Sannhamp', 46: 'Sunflower',
    47: 'Urad', 48: 'Peas & beans (Pulses)', 49: 'other oilseeds', 50: 'Other Cereals',
    51: 'Cowpea(Lobia)', 52: 'Oilseeds total', 53: 'Guar seed', 54: 'Other Summer Pulses',
    55: 'Moth'
}

# Dictionary mapping integer values to seasons
season_map = {
    1: 'Whole Year', 2: 'Kharif', 3: 'Rabi', 4: 'Autumn', 5: 'Summer', 6: 'Winter'
}

# Dictionary mapping integer values to states
state_map = {
    1: 'Assam', 2: 'Karnataka', 3: 'Kerala', 4: 'Meghalaya', 5: 'West Bengal', 
    6: 'Puducherry', 7: 'Goa', 8: 'Andhra Pradesh', 9: 'Tamil Nadu', 10: 'Odisha', 
    11: 'Bihar', 12: 'Gujarat', 13: 'Madhya Pradesh', 14: 'Maharashtra', 
    15: 'Mizoram', 16: 'Punjab', 17: 'Uttar Pradesh', 18: 'Haryana', 
    19: 'Himachal Pradesh', 20: 'Tripura', 21: 'Nagaland', 22: 'Chhattisgarh', 
    23: 'Uttarakhand', 24: 'Jharkhand', 25: 'Delhi', 26: 'Manipur', 
    27: 'Jammu and Kashmir', 28: 'Telangana', 29: 'Arunachal Pradesh', 
    30: 'Sikkim'
}

# Streamlit UI
st.title('Agricultural Yield Predictor')

# Display image

response = requests.get("https://source.unsplash.com/600x400/?agriculture")
image = Image.open(BytesIO(response.content))
st.image(image, use_column_width=True)

# Input field for Crop
crop = st.selectbox('Select Crop:', options=list(crop_map.values()), index=0)

# Input field for Season
season = st.selectbox('Select Season:', options=list(season_map.values()), index=0)

# Input field for State
state = st.selectbox('Select State:', options=list(state_map.values()), index=0)

# Input fields for other features
area = st.number_input('Enter Area:', value=0.0)
production = st.number_input('Enter Production:', value=0.0)
annual_rainfall = st.number_input('Enter Annual Rainfall:', value=0.0)
fertilizer = st.number_input('Enter Fertilizer:', value=0.0)
pesticide = st.number_input('Enter Pesticide:', value=0.0)

# Make prediction button
if st.button('Predict'):
    # Map selected crop name back to its corresponding integer value
    crop_id = [key for key, value in crop_map.items() if value == crop][0]
    
    # Map selected season name back to its corresponding integer value
    season_id = [key for key, value in season_map.items() if value == season][0]
    
    # Map selected state name back to its corresponding integer value
    state_id = [key for key, value in state_map.items() if value == state][0]
    
    # Prepare input features as a list or numpy array
    input_features = [[crop_id, season_id, state_id, area, production, annual_rainfall, fertilizer, pesticide]]
    
    # Make prediction using the loaded model
    prediction = model.predict(input_features)
    
    # Display prediction
    st.subheader('Yield Prediction:')
    st.success(f"The predicted yield is {prediction[0]}")
