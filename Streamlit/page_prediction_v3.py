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
import matplotlib.pyplot as plt

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
    distance = liste_station.loc[liste_station["Station name"]==station_rep, 'Distance'].iloc[0]

    if station_rep is not None:
        if st.session_state.liste_choix[2] and st.button("Confirmer la caserne"):
            st.session_state.liste_choix[2]=False
            return station_resp,station_rep,distance
        else:
            return None,None,None

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

def charger_model(chemin_fichier):
    try:
        with open(chemin_fichier, 'rb') as fichier_scaler:
            scaler_charge = pickle.load(fichier_scaler)
        return scaler_charge
    except FileNotFoundError:
        st.error("Fichier scaler non trouvé.")
        return None
    except Exception as e:
        st.error(f"Erreur lors du chargement du scaler : {e}")
        return None

def standardisation(lien, valeur, nom):
    model = charger_model(lien)
    if not isinstance(valeur, (list, pd.Series)):
        valeur = [valeur]
    df = pd.DataFrame({nom: valeur}, index=[0])
    if nom == "ditance":
        df.rename(columns={"ditance":"distance"}, inplace = True)
    if model is not None:
        try:
            return model.transform(df)
        except Exception as e:
            st.error(f"Erreur lors de la transformation : {e}")
            return None
    else:
        st.error("Pb avec le model")

def prepa_incident(station_df):
    list_col = recup_df("list_col.csv")
    noms_colonnes = list_col.columns.tolist()

    # Créer un DataFrame rempli de zéros
    df_bilan = pd.DataFrame(0, index=[0], columns=noms_colonnes)

    caserne_resp = st.session_state.data.loc[0, 'caserne_resp']
    caserne_dep = st.session_state.data.loc[0, 'caserne_dep']

    inner = station_df.loc[station_df["Station name"] == caserne_resp, 'inner london']
    df_bilan.loc[0, 'inner'] = inner.iloc[0]

    if st.session_state.data.loc[0, 'caserne_resp'] == st.session_state.data.loc[0, 'caserne_dep']:
        df_bilan.loc[0, 'Stat_resp_rep'] = 1

    caserne_dep = st.session_state.data.loc[0, 'caserne_dep']
    bor_rep = station_df.loc[station_df["Station name"] == caserne_dep, 'BoroughName'].iloc[0]
    bor_inc = station_df.loc[station_df["Station name"] == caserne_resp, 'BoroughName'].iloc[0]

    if bor_rep == bor_inc :
        df_bilan.loc[0, 'Bor_resp_rep'] = 1
        df_bilan.loc[0, 'Bor_inc_rep'] = 1

    heure = st.session_state.data.loc[0, 'heure']
    if 2 <= heure <= 6:
        df_bilan.loc[0, 'H26'] = 1
    elif 11 <= heure <= 17:
        df_bilan.loc[0, 'H1117'] = 1

    # Standardisation de la distance
    distance = st.session_state.data.loc[0, 'distance']
    distancestd = standardisation('Donnees/Modeles/tranfo_distance.pkl',distance,"ditance")
    df_bilan['distStd'] = df_bilan['distStd'].astype(float)
    df_bilan.loc[0, 'distStd'] = float(distancestd.item())

    # Standardisation du ratio
    ratio = station_df.loc[station_df["Station name"] == caserne_dep, 'ratio'].iloc[0]
    ratioSC = standardisation('Donnees/Modeles/tranfo_ratio.pkl',ratio,"ratioSC")
    df_bilan['ratioStd'] = df_bilan['ratioStd'].astype(float)
    df_bilan.loc[0, 'ratioStd'] = float(ratioSC.item())

    stat_code = "Borough_" + station_df.loc[station_df["Station name"] == caserne_dep, 'BoroughCode'].iloc[0]
    df_bilan.loc[0, stat_code] = 1
    property_code = 'PropCat_' + st.session_state.data.loc[0, 'type_property']
    df_bilan.loc[0, property_code] = 1

    return df_bilan

def afficher_explication_shap_version_horizontal(df):
    filename = 'Donnees/Modeles/explainer_shap.pkl'

    try:
        with st.spinner("Chargement de l'explicateur SHAP..."):
            with open(filename, 'rb') as f:
                explainer_shap = cloudpickle.load(f)

        with st.spinner("Calcul des valeurs SHAP..."):
            shap_values = explainer_shap(df)

        with st.spinner("Création du graphique SHAP..."):
            shap.initjs()
            plt.figure(figsize=(10, 6))
            shap.force_plot(
                explainer_shap.expected_value, shap_values.values[0], df.iloc[0], matplotlib=True, show=False
            )
            st.pyplot(plt.gcf())

    except Exception as e:
        st.error(f"Erreur avec SHAP : {e}")
        st.text(traceback.format_exc())

def afficher_explication_shap(df):
    filename = 'Donnees/Modeles/explainer_shap.pkl'

    try:
        with st.spinner("Chargement de l'explicateur SHAP..."):
            with open(filename, 'rb') as f:
                explainer_shap = cloudpickle.load(f)

        with st.spinner("Calcul des valeurs SHAP..."):
            shap_values = explainer_shap(df)

        with st.spinner("Création du graphique SHAP..."):
            shap.initjs()  # Assurez-vous que JS de SHAP est bien chargé
            plt.figure(figsize=(10, 6))
            shap.summary_plot(shap_values, df)
            st.pyplot(plt.gcf())  # Affiche le graphique dans Streamlit

    except Exception as e:
        st.error(f"Erreur avec SHAP : {e}")
        st.text(traceback.format_exc())


def predictionv3():


    st.subheader("Prédiction à l'aide du modèle final (Gradient Boosting)")
    # Initialiser un DataFrame avec une première ligne vide
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'heure': [''],
            'lat': [''],
            'lng': [''],
            'caserne_resp': [''],
            'caserne_dep': [''],
            'distance':[''],
            'type_property': [''],
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
                station_resp,station_rep, distance = choix_station(st.session_state.data.loc[0,'lat'],st.session_state.data.loc[0,'lng'], station_df)

                if station_rep is not None :
                    st.session_state.data.loc[0, 'caserne_resp'] = station_resp
                    st.session_state.data.loc[0, 'caserne_dep'] = station_rep
                    st.session_state.data.loc[0, 'distance'] = distance

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

        if (st.session_state.data.iloc[0] != '').all():
            if st.button("Effacer les valeurs saisies"):
                st.session_state.data = pd.DataFrame({
                    'heure': [''],
                    'lat': [''],
                    'lng': [''],
                    'caserne_resp': [''],
                    'caserne_dep': [''],
                    'distance':[''],
                    'type_property': ['']
                    })
                st.session_state.liste_choix = [True, True, False, True]
                liste_choix_mise_a_jour = [choix for choix, est_choisi in zip(liste_choix_base, st.session_state.liste_choix) if est_choisi]
                # Recharger le selectbox pour refléter les changements
                st.rerun()


    with tab2:
        if not (st.session_state.data.iloc[0] != '').all():
            st.write("Choisissez d'abord les paramètres de l'incident (onglet 1)")
        else:
            df_bilan = prepa_incident(station_df)

            filename = 'Donnees/Modeles/gradient_boosting_model2v2.joblib'
            gb_model2 = joblib.load(filename)

            df_trans = gb_model2.predict_proba(df_bilan)


            if df_bilan.empty:
                st.warning("⚠️ Le DataFrame df_bilan est vide. Aucune prédiction ne peut être effectuée.")
            else:
                idx = 0

                X_input = df_bilan.iloc[[idx]]  # Toujours en DataFrame

                st.markdown("#### Observation sélectionnée")
                st.write(X_input)
                st.markdown("<br>", unsafe_allow_html=True)

                # Calcul des prédictions à chaque arbre
                probas = list(gb_model2.staged_predict_proba(X_input))
                proba_classe_1 = [p[0][1] for p in probas]
                proba_classe_0 = [p[0][0] for p in probas]

                # Affichage côte à côte
                st.markdown("#### Évolution des probabilités pour chaque classe")

                fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(14, 6))

                # Probabilité classe 0
                ax0.plot(range(1, len(proba_classe_0)+1), proba_classe_0, marker="o", color='blue')
                ax0.set_title("Classe 0 (tps réponse < 6 minutes)")
                ax0.set_xlabel("Nombre d'arbres")
                ax0.set_ylabel("Probabilité")
                ax0.grid(True)

                # Probabilité classe 1
                ax1.plot(range(1, len(proba_classe_1)+1), proba_classe_1, marker="o", color='green')
                ax1.set_title("Classe 1 (tps réponse >= 6 minutes)")
                ax1.set_xlabel("Nombre d'arbres")
                ax1.set_ylabel("Probabilité")
                ax1.grid(True)

                st.pyplot(fig)

                final_pred = gb_model2.predict(X_input)[0]
                final_proba = gb_model2.predict_proba(X_input)[0][final_pred]
                st.write(f" **Classe prédite finale :** {final_pred} et **Probabilité finale :** {final_proba:.4f}")
                st.markdown("<br>", unsafe_allow_html=True)

            # Interprétation
            st.markdown("#### Explicabilité de la prédiction de l'incident")


            afficher_explication_shap_version_horizontal(df_bilan)
