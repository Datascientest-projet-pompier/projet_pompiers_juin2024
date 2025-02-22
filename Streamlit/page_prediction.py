import streamlit as st
import folium
from streamlit_folium import st_folium

def choix_lat_long():
    if "map_visible" not in st.session_state:
        st.session_state.map_visible = False
    if "coords_selected" not in st.session_state:
        st.session_state.coords_selected = False
    if "lat" not in st.session_state:
        st.session_state.lat = None
    if "lng" not in st.session_state:
        st.session_state.lng = None

    # Bouton pour afficher la carte
    if st.button("Choix de la position"):
        st.session_state.map_visible = True
        st.session_state.coords_selected = False

    # Affichage de la carte uniquement si l'utilisateur a cliqué sur "Choix de la position"
    if st.session_state.map_visible:
        st.write("Cliquez sur la carte pour sélectionner une position.")

        # Création de la carte Folium
        london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
        london_map.add_child(folium.LatLngPopup())

        # Affichage de la carte
        map_data = st_folium(london_map, width=700, height=500)

        # Récupération des coordonnées
        if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
            st.session_state.lat = map_data["last_clicked"]["lat"]
            st.session_state.lng = map_data["last_clicked"]["lng"]
            st.session_state.coords_selected = True

        # Bouton pour fermer la carte après sélection
        if st.session_state.coords_selected:
            if st.button("Fermer la carte"):
                st.session_state.map_visible = False

    # Affichage des coordonnées sélectionnées
    if st.session_state.coords_selected:
        st.write(f"Coordonnées sélectionnées : Latitude = {st.session_state.lat}, Longitude = {st.session_state.lng}")

    return st.session_state.lat, st.session_state.lng

def prediction():
    st.title("Prédiction avec le Gradient Boosting")

    # Choix de la position
    st.subheader("Choix de la position")
    choix_lat_long()

    # Bouton pour choisir une caserne (fonctionnalité à préciser)
    if st.button("Choix de la caserne"):
        st.write("Fonction à implémenter : sélection d'une caserne.")

