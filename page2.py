import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

def lire_html(chemin_fichier):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier HTML : {e}")
        return None
    
def recup_df_2024():
    # Chargement du DataFrame df_2024
    try:
        df_2024 = pd.read_csv("Donnees/df_2024.csv")  # Remplacez "df_2024.csv" par le chemin correct
        return df_2024
    except FileNotFoundError:
        st.error("Le fichier df_2024.csv n'a pas été trouvé.")
        return
    
    
def page2():
    df_2024 = recup_df_2024()

    caserne = df_2024['IncGeo_BoroughName'].unique()
    caserne = [c.lower() for c in caserne]
    caserne = sorted(caserne)
    
    st.title("Affichage de Cartes HTML")

    # Case à cocher pour le choix des incidents
    choix_incidents = st.radio(
        "Sélectionnez les incidents à afficher :",
        ["Tous les incidents", "Incidents avec temps supérieur à 6 min"]
    )

    # Sélection de la carte à afficher
    carte_choisie = st.selectbox("Choisissez une carte :", caserne)
    
    if choix_incidents == "Tous les incidents":
        chemin_fichier = f"Donnees/{carte_choisie}.html"
    else :
        chemin_fichier = f"Donnees/{carte_choisie}.1html"
    
    # Lire et afficher la carte HTML choisie
    html_carte = lire_html(chemin_fichier)
    components.html(html_carte, height=600)  # Ajustez la hauteur selon vos besoins
    
    #if carte_choisie == "BARKING AND DAGENHAM":
    #    html_carte = lire_html("BARKING AND DAGENHAM.html")
    #elif carte_choisie == "BEXLEY":
    #    html_carte = lire_html("BEXLEY.html")
    #else:
    #    html_carte = None

    #if html_carte:
    #    components.html(html_carte, height=600)  # Ajustez la hauteur selon vos besoins
    #else:
    #    st.error("Carte HTML non trouvée.")