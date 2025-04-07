import folium
import streamlit as st

from streamlit_folium import st_folium

# Crée la carte
london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# Ajoute un marqueur
folium.Marker([51.5074, -0.1278], tooltip="Londres").add_to(london_map)

# Affiche la carte dans Streamlit
st_folium(london_map, width=725,height=500, key="map1")
