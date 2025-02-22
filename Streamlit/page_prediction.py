import streamlit as st
import folium
from streamlit_folium import folium_static

import streamlit as st
import folium
from streamlit_folium import folium_static
import streamlit_modal as modal

def prediction():
    st.title("Prédiction")

    # Bouton pour ouvrir le modal
    if st.button("Ouvrir la carte"):
        with modal.container():
            st.header("Carte de Londres")
            london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
            folium_static(london_map)

    # Récupération des coordonnées cliquées 
    if "clicked_lat" in st.session_state and "clicked_lon" in st.session_state:
        st.write(f"Latitude cliquée : {st.session_state.clicked_lat}")
        st.write(f"Longitude cliquée : {st.session_state.clicked_lon}")
