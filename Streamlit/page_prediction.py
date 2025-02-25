import streamlit as st
import folium
from streamlit_folium import st_folium
#from pyproj import Geod
#import geopandas as gpd
#from shapely.geometry import Point
import geographiclib.geodesic as geodesic
import numpy as np
import pickle
import pandas as pd
import joblib
import cloudpickle
import streamlit.components.v1 as components
import shap


from fonctions import recup_df

def choix_heure():
    if st.session_state.show_heure_bouton:
        if st.button("Choix de l'heure de l'incident"):
            st.session_state.show_heure_choix = True
            st.session_state.show_position_bouton = False
            st.session_state.show_station_bouton = False
            st.session_state.show_type_bouton = False

    if st.session_state.show_heure_choix:
        heure_choisie = st.number_input("Choisir une heure (0-23)", min_value=0, max_value=23, value=12, step=1)

        if st.button("Valider"):
            st.session_state.heure = heure_choisie
            st.session_state.show_heure_choix  = False
            st.session_state.show_heure_bouton = False
            if "lat" not in st.session_state:
                st.session_state.show_position_bouton = True
            elif "station_dep" not in st.session_state:
                st.session_state.show_station_bouton = True
            if "type" not in st.session_state:
                st.session_state.show_type_bouton = True

def choix_lat_long():
    if "map_visible" not in st.session_state:
        st.session_state.map_visible = False
    if "coords_selected" not in st.session_state:
        st.session_state.coords_selected = False
    if "manual_input" not in st.session_state:
        st.session_state.manual_input = False
    if "position_choice_made" not in st.session_state:
        st.session_state.position_choice_made = False  # Ajout de cette ligne

    # Bouton initial pour lancer le choix de la position
    if st.session_state.show_position_bouton and not st.session_state.position_choice_made:
        if st.button("Choix de la position") and st.session_state.show_all:
            st.session_state.position_choice_made = True
            st.session_state.show_heure_bouton = False
            st.session_state.show_type_bouton = False

    # Affichage des options de saisie seulement après avoir cliqué sur le bouton initial
    if st.session_state.position_choice_made:
        choice = st.radio("Choisissez la méthode de saisie des coordonnées :", ("Carte", "Saisie manuelle"))

        if choice == "Carte":
            # Bouton pour afficher la carte
            if not st.session_state.map_visible:
                if st.button("Choix de la position sur la carte"):
                    st.session_state.map_visible = True
                    st.session_state.manual_input = False

            # Affichage de la carte
            if st.session_state.map_visible:
                st.write("Cliquez sur la carte pour sélectionner une position.")

                # Création de la carte Folium
                london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
                folium.LatLngPopup().add_to(london_map)

                # Affichage de la carte
                map_data = st_folium(london_map, width=700, height=500)

                # Récupération des coordonnées
                if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
                    st.session_state.lat = map_data["last_clicked"]["lat"]
                    st.session_state.lng = map_data["last_clicked"]["lng"]
                    st.session_state.coords_selected = True

                # Bouton pour fermer la carte
                if st.session_state.coords_selected:
                    if st.button("Fermer la carte"):
                        if "heure" not in st.session_state:
                            st.session_state.show_heure_bouton = True
                        if "type" not in st.session_state:
                            st.session_state.show_type_bouton = True
                        st.session_state.show_station_bouton = True
                        st.session_state.map_visible = False
                        st.session_state.show_position_bouton = False
                        st.session_state.coords_selected = False
                        st.session_state.position_choice_made = False

        elif choice == "Saisie manuelle":
            # Saisie manuelle des coordonnées
            if not st.session_state.manual_input:
                if st.button("Saisie manuelle des coordonnées"):
                    st.session_state.manual_input = True
                    st.session_state.map_visible = False

            if st.session_state.manual_input:
                lat_manual = st.number_input("Latitude", value=51.5074)
                lng_manual = st.number_input("Longitude", value=-0.1278)

                if st.button("Valider les coordonnées manuelles"):
                    st.session_state.lat = lat_manual
                    st.session_state.lng = lng_manual
                    st.session_state.coords_selected = True
                    st.session_state.manual_input = False
                    if "heure" not in st.session_state:
                        st.session_state.show_heure_bouton = True
                    if "type" not in st.session_state:
                        st.session_state.show_type_bouton = True
                    st.session_state.show_station_bouton = True
                    st.session_state.show_position_bouton = False
                    st.session_state.coords_selected = False
                    st.session_state.position_choice_made = False

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

def choix_station():
    if st.session_state.show_station_bouton:  # Afficher le bouton seulement si show_heure_bouton est True
        if st.button("Choix de la station intervenant pour l'incident"):
            st.session_state.show_station_choix = True
            st.session_state.show_heure_bouton = False
            st.session_state.show_type_bouton = False
        
        station_df = recup_df("FireStationInfo_2.csv",";")

    if st.session_state.show_station_choix:
        lat = st.session_state.lat
        lng = st.session_state.lng
        station_proche = trouver_station_proche(lat, lng, station_df)
        station_resp = station_proche.iloc[0]["Station name"]
        arrondissement = station_proche.iloc[0]["BoroughName"]
        arrondissement_code = station_proche.iloc[0]["BoroughCode"]
        inner = station_proche.iloc[0]["inner london"]
        ratio = station_proche.iloc[0]["ratio"]
        st.session_state.station_resp = station_resp
        st.session_state.arrondissement = arrondissement
        st.session_state.arrondissement_code = arrondissement_code
        st.session_state.inner = inner
        # Standardisation du ratio
        st.session_state.ratioSC = standardisation('Donnees/Modeles/tranfo_ratio.pkl',ratio,"ratioSC")

        st.write(f"Caserne responsable : {station_resp}.")

        station_names = station_proche["Station name"].tolist()
        choix_station = st.selectbox("Choisir une station", station_names)

        # Affichage de la station choisie
        st.write(f"Station choisie : {choix_station}")

        
        if choix_station:  # Vérifier si une station a été sélectionnée
            df_info = station_proche[station_proche["Station name"] == choix_station]
            distance = df_info["Distance"].values[0]
            station_dep = df_info["Station name"].values[0]
            arrondissement_dep = df_info["BoroughName"].values[0]
            st.session_state.station_dep = station_dep
            st.session_state.arrondissement_dep = arrondissement_dep
            # Standardisation de la distance
            st.session_state.distancestd = standardisation('Donnees/Modeles/tranfo_distance.pkl',distance,"ditance")
            # Construction stat_resp_rep
            if station_resp == station_dep :
                st.session_state.stat_resp_rep = 1
            else : 
                st.session_state.stat_resp_rep = 0
            # Construction Bor_inc_rep
            if arrondissement == arrondissement_dep :
                st.session_state.Bor_inc_rep = 1
            else :
                st.session_state.Bor_inc_rep = 0

        if st.button("Valider"):
            st.session_state.show_station_bouton = False
            st.session_state.show_station_choix = False
            if "heure" not in st.session_state:
                st.session_state.show_heure_bouton = True
            if "type" not in st.session_state:
                st.session_state.show_type_bouton = True

def choix_type():
    if st.session_state.show_type_bouton:  # Afficher le bouton seulement si show_type_bouton est True
        if st.button("Choix du type d'incident") and st.session_state.show_all:
            st.session_state.show_type_choix = True
            st.session_state.show_heure_bouton = False
            st.session_state.show_position_bouton = False
            st.session_state.show_station_bouton = False

    propriete = recup_df("PropertyCategory.csv")

    if st.session_state.show_type_choix:
        type_incident = propriete["PropertyCategory"].unique().tolist()
        choix_type = st.selectbox("Choisir une station", type_incident)

        # Affichage de la station choisie
        st.write(f"Type incident : {choix_type}")

        if st.button("Valider"):
            st.session_state.type = choix_type
            st.session_state.show_type_bouton = False
            st.session_state.show_type_choix = False
            if "heure" not in st.session_state:
                st.session_state.show_heure_bouton = True
            if "lat" not in st.session_state:
                st.session_state.show_position_bouton = True
            elif "station_dep" not in st.session_state:
                st.session_state.show_station_bouton = True

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

def param_incident():

    st.title("Prédiction avec le Gradient Boosting")
    st.subheader("Choix des paramètre de l'incident")
    
    # Paramétrisation de tous les bouton
    # Paramétrisation de tous les bouton
    if "show" not in st.session_state:
        st.session_state.show = True

    if st.session_state.show:
        if st.button("Définir les paramètres de l'incident") and st.session_state.show:
            #st.session_state.clear()
            st.session_state.show_all = True
            st.session_state.show_heure_bouton = True
            st.session_state.show_heure_choix = False
            st.session_state.show_position_bouton = True
            st.session_state.show_position_choix = False
            st.session_state.show_station_bouton = False
            st.session_state.show_station_choix = False
            st.session_state.show_type_bouton = True
            st.session_state.show_type_choix = False
            st.session_state.show = False

    # Heure de l'incident
    if "show_heure_bouton" in st.session_state:
        if st.session_state.show_heure_bouton:
            choix_heure()
    
    # Choix de la position
    if "show_position_bouton" in st.session_state:
        if st.session_state.show_position_bouton:
            choix_lat_long()
    
    # Bouton pour choisir une caserne
    if "lat" in st.session_state:
        if st.session_state.show_station_bouton:
            choix_station()

    # Bouton choix du type d'incident
    if "show_type_bouton" in st.session_state:
        if st.session_state.show_type_bouton:
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
    if "type" in st.session_state:
        st.write(f"Type d'incidident : {st.session_state.type}")

def validation(): 
    if "boutons_visibles" not in st.session_state:
        st.session_state.boutons_visibles = True

    if st.session_state.boutons_visibles:
        valide = "heure" in st.session_state and "arrondissement" in st.session_state and "station_dep" in st.session_state
        valide = valide and "type" in st.session_state

        if valide:
            col1, col2 = st.columns(2)  # Utilisation de colonnes pour une meilleure disposition

            if col1.button("Valider paramètre incident"):
                st.session_state.show_all = False
                st.session_state.valid_pred = True
                st.session_state.boutons_visibles = False  # Masquer les boutons
            if col2.button("Recommencer choix des paramètres"):
                st.session_state.clear()
                st.session_state.boutons_visibles = False  # Masquer les boutons
                st.rerun()

def afficher_chemin_prediction(model, data, feature_names):
    """
    Affiche le chemin de prédiction précis pour une donnée donnée.

    Args:
        model (GradientBoostingClassifier): Le modèle entraîné.
        data (pd.DataFrame): La donnée pour laquelle afficher le chemin.
        feature_names (list): Les noms des caractéristiques.
    """

    # Sélectionner le premier arbre (vous pouvez itérer sur tous les arbres si nécessaire)
    tree = model.estimators_[0, 0].tree_

    node_index = 0
    path = []

    while tree.children_left[node_index] != -1:
        feature = tree.feature[node_index]
        threshold = tree.threshold[node_index]
        value = data.iloc[0, feature]

        path.append({
            "node_index": node_index,
            "feature": feature_names[feature],
            "threshold": threshold,
            "value": value,
            "decision": "left" if value <= threshold else "right"
        })

        if value <= threshold:
            node_index = tree.children_left[node_index]
        else:
            node_index = tree.children_right[node_index]

    # Afficher le chemin
    st.write("Chemin de prédiction :")
    for step in path:
        st.write(f"Nœud {step['node_index']}: {step['feature']} { '<=' if step['decision'] == 'left' else '>'} {step['threshold']:.4f} (Valeur: {step['value']:.4f})")

def afficher_explication_shap(df):
    filename = 'Donnees/Modeles/explainer_shap.pkl'
    try:
        with st.spinner("Chargement de l'explicateur SHAP..."):
            with open(filename, 'rb') as f:
                explainer_shap = cloudpickle.load(f)

        if explainer_shap:
            # Vérification du format de df
            if not isinstance(df, pd.DataFrame):
                st.error("Les données doivent être un DataFrame pandas.")
                return

            with st.spinner("Calcul des valeurs SHAP..."):
                shap_values = explainer_shap(df)

            with st.spinner("Création du graphique SHAP..."):
                shap_html = shap.force_plot(explainer_shap.expected_value, shap_values.values, df)

            shap_html_str = f"<head>{shap.getjs()}</head><body>{shap_html.html()}</body>"
            st.components.v1.html(shap_html_str, height=600)
        else:
            st.warning("L'explicateur SHAP n'est pas disponible.")
    except FileNotFoundError:
        st.error(f"Le fichier {filename} n'a pas été trouvé.")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}\n{traceback.format_exc()}")

def afficher_explication_shap2(df):
    filename = 'Donnees/Modeles/explainer_shap.pkl'
    try:
        with open(filename, 'rb') as f:
            explainer_shap = cloudpickle.load(f)

        if explainer_shap:
            # Obtenir les valeurs SHAP pour la nouvelle ligne
            shap_values = explainer_shap(df)

            # Créer le graphique SHAP sans matplotlib
            shap_html = shap.force_plot(explainer_shap.expected_value, shap_values.values, df)

            # Afficher le graphique dans Streamlit
            shap_html_str = f"<head>{shap.getjs()}</head><body>{shap_html.html()}</body>"
            st.components.v1.html(shap_html_str, height=600)
        else:
            st.warning("L'explicateur SHAP n'est pas disponible.")
    except FileNotFoundError:
        st.error(f"Le fichier {filename} n'a pas été trouvé.")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")


    filename = 'Donnees/Modeles/explainer_lime.pkl'
    try:
        with open(filename, 'rb') as f:
            explainer_lime = cloudpickle.load(f)
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'explainer LIME : {e}")
        return

    # Continuez avec l'explication LIME
    explanation = explainer_lime.explain_instance(df.values[0], gb_model2.predict_proba, num_features=10)
    st.components.v1.html(explanation.as_html(), height=800)

def afficher_explication_lime(df, gb_model2):
    filename = 'Donnees/Modeles/explainer_lime.pkl'
    try:
        with open(filename, 'rb') as f:
            explainer_lime = cloudpickle.load(f)
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'explainer LIME : {e}")
        return

    try:
        explanation = explainer_lime.explain_instance(df.values[0], gb_model2.predict_proba, num_features=10)
        st.components.v1.html(explanation.as_html(), height=800)
    except Exception as e:
        st.error(f"Erreur lors de l'explication LIME : {e}")

def prediction():
    param_incident()
    st.subheader("Prédiction avec les données de l'incident")

    validation()

    if "valid_pred" in st.session_state:
        if st.session_state.valid_pred:
            
            # Charger les noms de colonnes
            list_col = recup_df("list_col.csv")
            noms_colonnes = list_col.columns.tolist()

            # Créer un tableau NumPy de zéros
            zeros = np.zeros((1, len(noms_colonnes)))

            # Créer le DataFrame
            df = pd.DataFrame(zeros, columns=noms_colonnes)

            # Mise a jour dataframe
            df["inner"] = st.session_state.inner
            df["Bor_inc_rep"] = st.session_state.Bor_inc_rep
            df["Bor_resp_rep"]= st.session_state.Bor_inc_rep
            df["Stat_resp_rep"]= st.session_state.Bor_inc_rep
            if st.session_state.heure <= 6 and st.session_state.heure >= 2:
                df["H26"] = 1
            elif st.session_state.heure <= 17 and st.session_state.heure >= 11:
                df["H1117"] = 1
            nom_col_type = "PropCat_" + st.session_state.type
            df[nom_col_type] = 1
            nom_col_arrondissement = "Borough_" + st.session_state.arrondissement_code
            df[nom_col_arrondissement] = 1
            df["distStd"] = st.session_state.distancestd
            df["ratioStd"] = st.session_state.ratioSC
            
            st.write(df)
            
            filename = 'Donnees/Modeles/gradient_boosting_model2v2.joblib'
            gb_model2 = joblib.load(filename)

            # Afficher la prédiction
            st.markdown("#### Prédiction avec les données de l'incident")
            df_trans = gb_model2.predict_proba(df)
            prob_classe_0 = round(df_trans[0, 0], 4)
            prob_classe_1 = round(df_trans[0, 1], 4)
            st.write("Prédiction que l'arrivée sur site soit inférieur à 6 min : ",prob_classe_0)
            st.write("Prédiction que l'arrivée sur site soit inférieur à 6 min : ",prob_classe_1)

            # Afficher l'arbre de decision
            st.markdown("#### Arbre de prédiction")            
            noms_colonnes = df.columns.tolist()
            afficher_chemin_prediction(gb_model2, df, noms_colonnes)

            # Interprétation
            st.markdown("#### Interprétation avec Lime et Shap")
            col1, col2 = st.columns(2)  # Utilisation de colonnes pour une meilleure disposition
            st.warning("Attention Interprétation Lime rencontre un problème, et fait planté l'application")

            if col1.button("Interprétation lime"):
                afficher_explication_lime(df,gb_model2)
                
            if col2.button("Interpretation shap"):
                afficher_explication_shap(df)
            
            