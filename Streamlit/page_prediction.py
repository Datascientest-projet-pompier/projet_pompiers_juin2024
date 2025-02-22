import streamlit as st
import folium
from streamlit_folium import st_folium
from pyproj import Geod
import pandas as pd
import numpy as np

from fonctions import recup_df

def choix_heure():
    if st.session_state.show_heure_bouton:  # Afficher le bouton seulement si show_heure_bouton est True
        if st.button("Choix de l'heure de l'incident") and st.session_state.show_all:
            st.session_state.show_heure_choix = True

    if st.session_state.show_heure_choix:
        heure_choisie = st.slider("Choisir une heure", 0, 23, 12)  # 0-23 heures, valeur initiale 12
        st.session_state.heure = heure_choisie

    if "heure" in st.session_state and st.session_state.show_heure_choix:
        if st.button("Valider"):
            st.session_state.show_heure_choix = False  # Cache le slide
            st.session_state.show_heure_bouton = False  # Cacher le bouton


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
    if st.session_state.show_position_bouton:
        if st.button("Choix de la position") and st.session_state.show_all:
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
                st.session_state.show_position_bouton = False

def calcul_dist(lat1, lon1, lat2, lon2):
    """
    Calcule la distance en mètres entre deux points géographiques.
    """
    geod = Geod(ellps='WGS84')
    _, _, distance = geod.inv(lon1, lat1, lon2, lat2)
    return np.round(distance, 3)

def trouver_station_proche(lat, lng, station_df):
    """
    Trouve la station la plus proche d'un point donné.

    Args:
        lat (float): Latitude du point de référence.
        lng (float): Longitude du point de référence.
        station_df (pd.DataFrame): DataFrame contenant les stations avec leurs coordonnées.

    Returns:
        tuple: (nom de la station la plus proche, distance en mètres)
    """

    distances = []
    for index, row in station_df.iterrows():
        distance = calcul_dist(lat, lng, row["Latitude"], row["Longitude"])
        distances.append(distance)

    station_df["Distance"] = distances

    # Trier et récupérer les 6 stations les plus proches
    station_proche = station_df.nsmallest(6, 'Distance')

    return station_proche

def choix_station():
    if st.session_state.show_station_bouton:  # Afficher le bouton seulement si show_heure_bouton est True
        if st.button("Choix de la station intervenant pour l'incident") and st.session_state.show_all:
            st.session_state.show_station_choix = True
        
        station_df = recup_df("FireStationInfo_2.csv",";")

    if st.session_state.show_station_choix:
        lat = st.session_state.lat
        lng = st.session_state.lng
        station_proche = trouver_station_proche(lat, lng, station_df)
        station_resp = station_proche.iloc[0]["Station name"]
        arrondissement = station_proche.iloc[0]["BoroughName"]
        st.session_state.station_resp = station_resp
        st.session_state.arrondissement = arrondissement
        st.write(f"Caserne responsable : {station_resp}.")

        station_names = station_proche["Station name"].tolist()
        choix_station = st.selectbox("Choisir une station", station_names)

        # Affichage de la station choisie
        st.write(f"Station choisie : {choix_station}")

        # Enregistrement de la distance
        if choix_station:  # Vérifier si une station a été sélectionnée
            df_info = station_proche[station_proche["Station name"] == choix_station]
            distance = df_info["Distance"].values[0]
            station_dep = df_info["Station name"].values[0]
            arrondissement_dep = df_info["BoroughName"].values[0]
            st.session_state.distance = distance
            st.session_state.station_dep = station_dep
            st.session_state.arrondissement_dep = arrondissement_dep

        if st.button("Valider"):
            st.session_state.show_station_bouton = False
            st.session_state.show_station_choix = False

def choix_type():
    if st.session_state.show_type_bouton:  # Afficher le bouton seulement si show_type_bouton est True
        if st.button("Choix du type d'incident") and st.session_state.show_all:
            st.session_state.show_heure_choix = True


def prediction():
    
    st.session_state.show_all = True
    
    
    station_df = recup_df("FireStationInfo_2.csv",";")
    st.title("Prédiction avec le Gradient Boosting")

    st.subheader("Choix des paramètre de l'incident")

    # Heure de l'incident
    if "show_heure_bouton" not in st.session_state:
        st.session_state.show_heure_bouton = True
    if "show_heure_choix" not in st.session_state:
        st.session_state.show_heure_choix = False
    choix_heure()
    
    # Choix de la position
    if "show_position_bouton" not in st.session_state:
        st.session_state.show_position_bouton = True
        st.session_state.show_station_bouton = False
    choix_lat_long()
    
    # Bouton pour choisir une caserne
    if "lat" in st.session_state:
        st.session_state.show_station_bouton = True
    if "show_station_choix" not in st.session_state:
        st.session_state.show_station_choix = False

    choix_station()

    # Bouton choix du type d'incident
    if "show_type_bouton" not in st.session_state:
        st.session_state.show_type_bouton = True
    choix_type()
    


    # Résumé
    st.subheader("Resumer des informations de l'incident")
    if "heure" in st.session_state:
        st.write(f"Heure de l'incident : {st.session_state.heure}h")
    if "arrondissement" in st.session_state:
        st.write(f"Arrondissement de l'incident : {st.session_state.arrondissement}")
    if "station_resp" in st.session_state:
        st.write(f"Station responsable : {st.session_state.station_resp}")
    if "arrondissement_dep" in st.session_state:
        st.write(f"Arrondissement de la caserne deployée : {st.session_state.arrondissement_dep}")
    if "station_dep" in st.session_state:
        st.write(f"Station déployée : {st.session_state.station_dep}")

    if st.button("Valider"):
        st.session_state.show_all = False

    