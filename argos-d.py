#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:15:06 2021

@author: fas
"""

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

from my_utils_st import load_data, create_Chart


def filter_data(df, col, val1, val2):   # Filter data
    mask = (df[col].dt.date >= val1) & (df[col].dt.date <= val2)
    return df.loc[mask]


def show_map(layer):                    # Creates and show map
    r = pdk.Deck(layers=layer,
                 initial_view_state=view,
                 map_style="mapbox://styles/mapbox/" +
                 map_types[picked_type],
                 )
    st.pydeck_chart(r)


def data_expander(key):                 # Expander for data
    expander = st.beta_expander('Data')
    expander.dataframe(key)


st.set_page_config(layout="wide")
map_types = {"Light": "light-v10", "Dark": "dark-v10",
             "Outdoor": "outdoors-v11", "Satellite": "satellite-v9"}

# Sidebar widgets
st.sidebar.title("Argos dashboard")
st.sidebar.header("Maritime awareness")
option = st.sidebar.selectbox('Select view:', ["By source", "Fusion"])
picked_type = st.sidebar.selectbox('Map style:', ["Light", "Dark",
                                                  "Outdoor", "Satellite"])
end_date = st.sidebar.date_input('Filter by date (UTC):')
days_back = st.sidebar.slider('Filter by days range', min_value=0, max_value=7)
start_date = end_date.replace(day=end_date.day - days_back)
st.write("Start date: ", start_date, "End date: ", end_date)

# Load data
camtes = load_data('/home/fas/Streamlit/data/camtes.xls', 'camtes')
seavision = load_data('/home/fas/Streamlit/data/seavision.xlsx',
                      'seavision')
satelital = load_data('/home/fas/Streamlit/data/sat2.csv', 'sat')

# Create maps
filtered_camtes = filter_data(camtes, 'DTG', start_date, end_date)
camtes_chart = create_Chart('ScatterplotLayer',
                            filtered_camtes[['Longitude', 'Latitude']],
                            [0, 255, 0])

filtered_seavision = filter_data(seavision, 'DTG', start_date, end_date)
seavision_chart = create_Chart('ScatterplotLayer',
                               filtered_seavision[['Longitude', 'Latitude']],
                               [0, 0, 255])

filtered_satelital = filter_data(satelital, 'DTG', start_date, end_date)
satelital_chart = create_Chart('ScatterplotLayer',
                               filtered_satelital[['Longitude', 'Latitude']],
                               [255, 0, 0])

# Render maps
view = pdk.ViewState(latitude=-50, longitude=-60, zoom=3,)
if (option == "By source"):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.write("Camtes", filtered_camtes.shape[0])
        show_map(camtes_chart)
        data_expander(filtered_camtes)

    with col2:
        st.write("Seavision", filtered_seavision.shape[0])
        show_map(seavision_chart)
        data_expander(filtered_seavision)

    with col3:
        st.write("Satélite", filtered_satelital.shape[0])
        show_map(satelital_chart)
        data_expander(filtered_satelital)

else:
    show_map([camtes_chart, seavision_chart, satelital_chart])
