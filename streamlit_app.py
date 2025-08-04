# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 15:19:52 2025

@author: bahaa
"""

import streamlit as st
import pandas as pd
import numpy as np

# Load all Excel files and combine data
@st.cache_data
def load_data():
    years = [f"{year}-{year+1}" for year in range(2012, 2020)]
    all_data = []
    for year in years:
        path = f"./Predicted Freeze-Thaw Cycles ({year}).xlsx"
        df = pd.read_excel(path)
        df['Year'] = year
        all_data.append(df)
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def find_nearby_points(df, input_lat, input_lon, max_distance_km=20):
    distances = haversine(input_lat, input_lon, df['Latitude'].values, df['Longitude'].values)
    nearby_mask = distances <= max_distance_km
    nearby_df = df[nearby_mask].copy()
    nearby_df['Distance_km'] = distances[nearby_mask]
    return nearby_df.sort_values('Distance_km')

def main():
    st.title("Freeze-Thaw Cycles Lookup Tool")

    df = load_data()

    lat = st.number_input("Latitude", format="%.6f", value=36.12)
    lon = st.number_input("Longitude", format="%.6f", value=-95.89)
    max_dist = st.slider("Search radius (km)", 1, 100, 20)

    if st.button("Search"):
        results = find_nearby_points(df, lat, lon, max_dist)
        if results.empty:
            st.warning("No data found within the search radius.")
        else:
            st.write(f"Found {len(results)} points near ({lat}, {lon}):")
            st.dataframe(results[['Year', 'Latitude', 'Longitude', 'Total Freeze-Thaw Cycles', 'Damaging Freeze-Thaw Cycles', 'Distance_km']])

if __name__ == "__main__":
    main()
