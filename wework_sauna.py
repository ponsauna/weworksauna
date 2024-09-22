#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import streamlit as st

# Haversine formula to calculate distance between two lat-long points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon1 - lon2)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Function to find the nearest WeWorks
def find_nearest_weworks(selected_sauna, sauna_data, wework_data):
    sauna = sauna_data[sauna_data['name'] == selected_sauna].iloc[0]
    sauna_lat, sauna_lon = sauna['latitude'], sauna['longitude']
    
    wework_data['distance'] = wework_data.apply(lambda row: haversine(sauna_lat, sauna_lon, row['latitude'], row['longitude']), axis=1)
    nearest_weworks = wework_data.nsmallest(3, 'distance')
    
    return nearest_weworks[['name', 'distance']]

# Load sauna and WeWork data from CSV files
wework_data = pd.read_csv('/Users/tsuyoshis/Desktop/python/Wework 緯度経度 - WeWeork_Address (2).csv')  # Replace with your sauna CSV file path
sauna_data = pd.read_csv('/Users/tsuyoshis/Desktop/python/東京サウナロケーション - SAUNA.csv')  # Replace with your WeWork CSV file path

# Streamlit App
st.title("Find Nearest WeWork from Sauna Locations")

# Text input for sauna name (for partial match search)
search_query = st.text_input("Search Sauna", "")

# Perform partial match search for saunas
if search_query:
    matched_saunas = sauna_data[sauna_data['name'].str.contains(search_query, case=False)]
    
    if not matched_saunas.empty:
        selected_sauna = st.selectbox("Select Sauna", matched_saunas['name'].tolist())
    else:
        st.write("No matching saunas found.")
        selected_sauna = None
else:
    selected_sauna = None

# If a sauna is selected, show the nearest WeWorks
if selected_sauna:
    nearest_weworks = find_nearest_weworks(selected_sauna, sauna_data, wework_data)
    st.write(f"Nearest WeWorks to {selected_sauna}:")
    st.write(nearest_weworks)


# In[ ]:




