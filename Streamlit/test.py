import folium
import streamlit as st

from streamlit_folium import st_folium

# center on Liberty Bell, add marker
london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# call to render Folium map in Streamlit
st_data = st_folium(london_map, width=725)
st.write(london_map)