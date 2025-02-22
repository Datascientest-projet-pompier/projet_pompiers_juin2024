import streamlit as st
import folium
from streamlit_folium import st_folium
from pyproj import Geod
import pandas as pd
import numpy as np

from fonctions import recup_df

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

    return st.session_state.lat, st.session_state.lng

def calcul_dist(lat1, lon1, lat2, lon2):
    """
    Calcule la distance en mètres entre deux points géographiques.
    """
    geod = Geod(ellps='WGS84')
    _, _, distance = geod.inv(lon1, lat1, lon2, lat2)
    return np.round(distance, 3)

def trouver_station_proche(lat, lng):
    """
    Trouve la station la plus proche d'un point donné.

    Args:
        lat (float): Latitude du point de référence.
        lng (float): Longitude du point de référence.
        station_df (pd.DataFrame): DataFrame contenant les stations avec leurs coordonnées.

    Returns:
        tuple: (nom de la station la plus proche, distance en mètres)
    """
    station_df = recup_df("FireStationInfo_2.csv",";")

    # Calcul de la distance pour chaque station
    station_df["Distance"] = station_df.apply(
        lambda row: calcul_dist(lat, lng, row["Latitude"], row["Longitude"]), axis=1
    )

    # Trier et récupérer les 6 stations les plus proches
    station_proche = station_df.nsmallest(6, 'Distance')

    return station_proche

def prediction():
    st.title("Prédiction avec le Gradient Boosting")

    # Heure de l'incident
    st.subheader("Choix de l'heure de l'incident")

    if "show_heure" not in st.session_state:
        st.session_state.show_heure = False

    if st.button("Choix de l'heure de l'incident"):
        st.session_state.show_heure = True  # Indique qu'il faut afficher le slider

    if st.session_state.show_heure:
        heure_choisie = st.slider("Choisir une heure", 0, 23, 12)  # 0-23 heures, valeur initiale 12
        st.session_state.heure = heure_choisie

    if "heure" in st.session_state and st.session_state.show_heure:
        if st.button("Valider"):
            st.session_state.show_heure = False  # Cache le slide


    # Choix de la position
    st.subheader("Choix de la position")
    lat, lng = choix_lat_long()
    #if lat is not None and lng is not None:
        # Sauvegarde des résultats dans la session
        #st.session_state.lat = lat
        #st.session_state.lng = lng
    
    # Bouton pour choisir une caserne
    st.subheader("Choix de la caserne")
    st.session_state.show_stat = False
    if st.button("Choix de la caserne"):

        if lat is None or lng is None:
            st.write("Choisir le lieu de l'incident d'abord")

        else :
            station_proche = trouver_station_proche(lat, lng)

            # Sauvegarde des résultats dans la session
            st.session_state.station_proche = station_proche

            st.session_state.show_stat = True  # Indique qu'il faut afficher le slider
    
    # Liste déroulante pour le choix de la station
    if "station_proche" in st.session_state and st.session_state.show_stat:
        station_resp = st.session_state.station_proche.iloc[0]["Station name"]
        st.session_state.station_resp = station_resp
        st.write(f"Caserne responsable : {station_resp}.")
        choix_station = ""
        station_names = st.session_state.station_proche["Station name"].tolist()
        choix_station = st.selectbox("Choisir une station", station_names)

        # Affichage de la station choisie
        st.write(f"Station choisie : {choix_station}")

        #enregistrement de la distance
            
        if choix_station != "":
            df_info = st.session_state.station_proche[st.session_state.station_proche["Station name"]== choix_station]
            distance = df_info["Distance"].values[0]
            st.session_state.distance = distance
            st.session_state.station_dep = df_info["Station name"].values[0]

            if st.button("Valider"):
                st.session_state.show_stat = False  # Cache le slider



    # Bouton choix du type d'incident
    st.subheader("Type d'incident")
    if st.button("Type d'incident"):
        st.write("test")


    # Résumé
    st.subheader("Resumer des informations de l'incident")
    if "heure" in st.session_state:
        st.write(f"Heure de l'incident : {st.session_state.heure}h")
    if "station_resp" in st.session_state:
        st.write(f"Station responsable : {st.session_state.station_resp}")
    if "station_dep" in st.session_state:
        st.write(f"Station déployée : {st.session_state.station_dep}")

    