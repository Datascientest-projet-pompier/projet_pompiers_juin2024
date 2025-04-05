import streamlit as st
import folium
from streamlit_folium import st_folium

def test():
    st.write("Test de la page")


    st.title("Carte interactive avec Streamlit")

    # 1. Créer une carte Folium
    m = folium.Map(location=[46.4, 1.5], zoom_start=6)  # Centrez la carte sur la France

    # 2. Ajouter des marqueurs (facultatif)
    folium.Marker([48.8566, 2.3522], popup="Paris").add_to(m)
    folium.Marker([47.2184, -1.5536], popup="Nantes").add_to(m)
    folium.Marker([46.6667, -1.1667], popup="Landeronde").add_to(m) # Votre localisation actuelle

    # 3. Afficher la carte dans Streamlit
    st_folium(m, width=700, height=500)

    st.markdown("Vous pouvez interagir avec cette carte : zoomer, déplacer, cliquer sur les marqueurs.")
