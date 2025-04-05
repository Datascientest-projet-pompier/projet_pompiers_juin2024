import streamlit as st
import folium
from streamlit_folium import st_folium

def test():
    st.write("Test de la page")


    st.title("Test de carte SIMPLE")

    m = folium.Map(location=[46.4, 1.5], zoom_start=6)
    st_folium(m)
