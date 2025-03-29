import streamlit as st
import folium
from streamlit_folium import st_folium
import geographiclib.geodesic as geodesic
import numpy as np
import pickle
import pandas as pd
import joblib
import cloudpickle
import streamlit.components.v1 as components
import shap
import traceback

from fonctions import recup_df

def choix_heure():
    """
    Permet à l'utilisateur de choisir une heure (0-23) avec validation.

    Returns:
        int: L'heure choisie par l'utilisateur ou None si l'utilisateur annule.
    """
    heure_choisie = st.number_input("Choisir une heure (0-23)", min_value=0, max_value=23, value=12, step=1)

    if st.session_state.liste_choix[0] and st.button("Confirmer l'heure"):
        st.session_state.liste_choix[0]=False
        return heure_choisie

def choix_lieu():

    lat, lng = None, None  # Initialiser lat et lng à None

    choix = st.radio("Choisissez la méthode de saisie des coordonnées :", ("Carte", "Saisie manuelle"))

    if choix == "Carte":
        # Création de la carte Folium
        london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
        folium.LatLngPopup().add_to(london_map)

        # Affichage de la carte
        map_data = st_folium(london_map, width=700, height=500)

        if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
            lat = map_data["last_clicked"]["lat"]
            lng = map_data["last_clicked"]["lng"]

        if lat is not None:
            st.write(lat, lng)

    if choix == "Saisie manuelle":
        lat = st.number_input("Latitude", value=51.5074)
        lng = st.number_input("Longitude", value=-0.1278)

    if lat is not None:
        if st.session_state.liste_choix[1] and st.button("Confirmer la position"):
            st.session_state.liste_choix[1]=False
            st.session_state.liste_choix[2]=True
            return lat, lng
        
    return None, None  # Retourner None, None si aucune coordonnée n'est sélectionnée


def calcul_dist(lat1, lon1, lat2, lon2):
    """
    Calcule la distance en mètres entre deux points géographiques en utilisant geographiclib.
    """
    geod = geodesic.Geodesic.WGS84
    result = geod.Inverse(lat1, lon1, lat2, lon2)
    distance = result['s12']  # Distance en mètres

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

def choix_station(lat, lng, station_df):
    liste_station = trouver_station_proche(lat, lng, station_df)
    station_resp = liste_station.iloc[0]["Station name"]

    st.write(f"La station responsable de l'incident est : {station_resp}")
    # Menu déroulant pour un choix unique
    station_names = liste_station["Station name"].tolist()
    station_rep = st.selectbox("Choisissez la station :", station_names)

    if station_rep is not None: 
        if st.session_state.liste_choix[2] and st.button("Confirmer la caserne"):
            st.session_state.liste_choix[2]=False
            return station_resp,station_rep
        else:
            return None,None

def choix_type():
    propriete = recup_df("PropertyCategory.csv")

    type_incident = propriete["PropertyCategory"].unique().tolist()
    type = st.selectbox("Choisir une station", type_incident)

    # Affichage de la station choisie
    if type is not None: 
        if st.session_state.liste_choix[3] and st.button("Confirmer le type"):
            st.session_state.liste_choix[3]=False
            return type
        else:
            return None

def prepa_incident(station_df):
    list_col = recup_df("list_col.csv")
    noms_colonnes = list_col.columns.tolist()
    df_bilan = pd.DataFrame(columns=noms_colonnes)

    caserne_resp = st.session_state.data.loc[0, 'caserne_resp']
    st.write(caserne_resp)

    # Utiliser loc pour accéder à la colonne 'inner london'
    inner = station_df.loc[station_df["Station name"] == caserne_resp, 'inner london']

    # Vérifier si une station correspondante a été trouvée
    if not inner.empty:
        # Vérifier si inner contient plusieurs valeurs
        if len(inner) > 1:
            st.warning(f"Plusieurs stations trouvées avec le nom : {caserne_resp}. Utilisation de la première.")
        df_bilan.loc[0, 'inner'] = inner.iloc[0]  # Prendre la première valeur
    else:
        st.error(f"Aucune station trouvée avec le nom : {caserne_resp}. Vérifiez le nom de la caserne.")
        df_bilan.loc[0, 'inner'] = None  # ou une autre valeur par défaut

    st.write(df_bilan)


        




def predictionv2():
    st.subheader("Prédiction avec les données de l'incident")
    # Initialiser un DataFrame avec une première ligne vide
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'heure': [''],
            'lat': [''],
            'lng': [''],
            'caserne_resp': [''],
            'caserne_dep': [''],
            'type_property': ['']
        })

    station_df = recup_df("FireStationInfo_2.csv",";")

    # Initialisation des variables à montrer
    if 'liste_choix' not in st.session_state:
        st.session_state.liste_choix = [True, True, False, True]
    liste_choix_base = ['Choix de l heure', 'Choix du lieu', 'Choix caserne déployée', 'Choix du type de propriété']

    # Créer une liste qui se met à jour automatiquement
    liste_choix_mise_a_jour = [choix for choix, est_choisi in zip(liste_choix_base, st.session_state.liste_choix) if est_choisi]

    # Création des onglets
    tab1, tab2 = st.tabs(["Préparation des données", "Prédiction avec le modèle"])

    with tab1:
        st.write(st.session_state.data)

        # Menu déroulant pour un choix unique
        if len(liste_choix_mise_a_jour) != 0:
            var = st.selectbox("Choisissez une variable d'intérêt :", liste_choix_mise_a_jour)

            if var == 'Choix de l heure':
                heure = choix_heure()
                if heure is not None:
                    st.session_state.data.loc[0, 'heure'] = heure
                    # Mettre à jour la liste après le choix de l'heure
                    if not st.session_state.liste_choix[0]:
                        liste_choix_mise_a_jour = [choix for choix, est_choisi in zip(liste_choix_base, st.session_state.liste_choix) if est_choisi]
                        # Recharger le selectbox pour refléter les changements
                        st.rerun()

            if var == 'Choix du lieu':
                lat, lng = choix_lieu()
                # Mettre à jour la liste après le choix de l'heure
                if lat is not None :
                    st.session_state.data.loc[0, 'lat'] = lat
                    st.session_state.data.loc[0, 'lng'] = lng
                
                    if not st.session_state.liste_choix[1]:
                        liste_choix_mise_a_jour = [choix for choix, est_choisi in zip(liste_choix_base, st.session_state.liste_choix) if est_choisi]
                        # Recharger le selectbox pour refléter les changements
                        st.rerun()

            if var == "Choix caserne déployée" and st.session_state.data.loc[0,'lat']!='' and st.session_state.data.loc[0,'lng']!='':
                station_resp,station_rep = choix_station(st.session_state.data.loc[0,'lat'],st.session_state.data.loc[0,'lng'], station_df)

                if station_rep is not None :
                    st.session_state.data.loc[0, 'caserne_resp'] = station_resp
                    st.session_state.data.loc[0, 'caserne_dep'] = station_rep
                
                    if not st.session_state.liste_choix[2]:
                        liste_choix_mise_a_jour = [choix for choix, est_choisi in zip(liste_choix_base, st.session_state.liste_choix) if est_choisi]
                        # Recharger le selectbox pour refléter les changements
                        st.rerun()

            if var == 'Choix du type de propriété':
                type = choix_type()
                if type is not None :
                    st.session_state.data.loc[0, 'type_property'] = type

                    if not st.session_state.liste_choix[3]:
                        liste_choix_mise_a_jour = [choix for choix, est_choisi in zip(liste_choix_base, st.session_state.liste_choix) if est_choisi]
                        # Recharger le selectbox pour refléter les changements
                        st.rerun()

    with tab2:
        if not (st.session_state.data.iloc[0] != '').all():
            st.write("Choisissez d'abord les paramètre de l'incident (onglet 1)")
        else:
            if st.button("Effectuer une prédiction"):
                prepa_incident(station_df)
            


