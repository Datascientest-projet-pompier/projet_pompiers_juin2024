import streamlit as st
import pandas as pd
import os
import numpy as np

from fonctions import texte_justifie
from fonctionsstat  import tab_stat

import matplotlib.pyplot as plt

import fonctionsgraph

def visualisation():
    st.title("Visualisation")

    st.markdown(texte_justifie(
        "A ce stade notre dataframe représentant l'ensemble des incidents est composé de plus d'un millions de"
        " lignes représentant chacune un incident et plus de 50 variables représentant soit une information sur la "
        "description de l'incident soit la variable cible (temps). L'objectif de cette partie est l'étude de ces variables"
        " pour choisir celles qui seront conservées dans le modèle.<br>"
        "A vue du grand nombre de données et après une étude préalable, pour cette partie nous n'utiliserons que les données"
        " de 2023.<br>"
        "Remarque : Le tableau ne contient plus de valeurs manquantes, mais les valeurs extrème ou abérantes peuvent encore être présente.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Récupération des données de 2023
    df2023 = pd.read_csv("Donnees/Doc csv/df2023.csv")

    # Création des onglets
    tab1, tab2 = st.tabs(["Etude statistique", "Data Visualisation"])

    with tab1:
      st.subheader("Etude statistique")
      st.markdown(texte_justifie(
        " Notre jeu de données contient un grand nombre de variables qualitative et seulement cinq variables quantitatives"
        " (<code>Time...</code>, <code>Distance</code> et <code>RatioSc</code>)."
        "Une rapide étude statistique nous donne les informations suivantes :")
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)
      
      tab = tab_stat(df2023)
      st.table(tab)

    with tab2:
      st.subheader("Data Visualisation")
      
      st.markdown(texte_justifie(
        "Au vue de la distribution de la variable cible (temps total), nous avons dans un premier temps effectué"
        " une transformation Box-Cox pour tenter de rendre la variable le plus similaire possible à une distribution "
        "normale. De plus plus seuls certains graphiques sont présentés ici.")
        , unsafe_allow_html=True)
      
      st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("### Informations temporelles")
      # Choix de l'arbre affiché
      var_liste = ['HourOfCall','DayOfWeek','Month']
      # Menu déroulant pour un choix unique
      var = st.selectbox("Choisissez une variable d'intérêt :", var_liste)

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale
      
      # Affichage du premier graphique dans la première colonne
      with col1:
        fonctionsgraph.graph_countIncident(df2023, var)
    
      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_pointplot(df2023, var)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "Au vue de la distribution de la variable cible (temps total), on peut observer que les variables <code>"
            "DayOfWeek</code> et <code>Month</code> on peu d'influence sur la variables <code>boxcox_TotalResponseTime</code>.<br>"
            "En effet pour la variable <code>DayOfWeek</code> l'écart entre le temps total moyen le plus long (le vendredi) et le plus "
            "court (le jeudi) est de l'ordre de 2% et pour la variable <code>Month</code> l'écart entre le temps total moyen le"
            " plus long (en novembre) et le plus court (en avril) est de l'ordre de 3%.<br>"
            " Cette variation est inférieur à 5% pour ces deux variables elles ne seront pas conservées dans la suite de la modélisation.<br>"
            " Pour la variable <code>HourOfCall</code> on peut constater un impact sur le temps moyen de trajet. "
            "Le temps de trajet moyen augmente le jour, spécialement sur la tranche 10-18h, plage horaire où"
            " le trafic est plus dense car l'activité humaine plus intense. Il y a deux pics correspondant aux plages "
            "horaires 2-6h et 11-18h. Sur le temps total moyen, l'écart entre la valeur la plus forte (pour Hour=6h) "
            "et la plus faible (pour Hour=22h) est de l'ordre de 6%"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fonctionsgraph.test_anova(df2023, 'HourOfCall')

      st.markdown("### Informations géographiques")
      # Choix de l'arbre affiché
      var_nom = ['Arrondissement', "Quartier", "Station déployée"]

      # Menu déroulant pour un choix unique
      var = st.selectbox("Choisissez une variable d'intérêt :", var_nom)
      indice = var_nom.index(var)

      var_list = ['IncGeo_BoroughName','IncGeo_WardName','DeployedFromStation_Name']
      var = var_list[indice]
      
      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale
      
      # Affichage du premier graphique dans la première colonne
      with col1:
        fonctionsgraph.graphQuali_countPlot(df2023, var)
    
      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_meanPlot(df2023, var, rest=50)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "Pour l'arrondissement la moyenne de TotalResponseTime varie entre 25,7 à 30,1 soit une différence de 15% environ."
            " On peut donc supposer que l'arrondissement où a lieu l'incident a un impact sur les temps.<br>"
            "Le dataFrame contient plus de 600 quartiers différents ; nous n'avons représenté qu'un partie"
            " d'entre eux, correspondant aux 50 premiers/derniers pour lesquels la moyenne de TotalResponseTime"
            " est la plus forte/faible.<br>"
            "Pour TotalResponseTime, il y a une différence de l'ordre de 40% entre Darwin (temps moyen=36,1) et"
            " Norbury & Pollards Hill (21,3).<br>"
            "Les temps moyens varient aussi en fonction de la caserne de départ. La différence entre la moyenne "
            "la plus forte et la plus faible est de l'ordre de 20% pour le temps total."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("### Variables explicatives du type d'incident")
      st.markdown(texte_justifie(
        "Le type d'incident est décrit par deux variables : <code>IncidentGroup</code> et <code>DetailedIncidentGroup</code> "
        "qui donnent une information plus ou moins détaillée sur le type d'incident.")
        , unsafe_allow_html=True)
      
      # Choix de l'arbre affiché
      var_liste = ['IncidentGroup','DetailedIncidentGroup']
      # Menu déroulant pour un choix unique
      var = st.selectbox("Choisissez une variable d'intérêt :", var_liste)
      
      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale
      
      # Affichage du premier graphique dans la première colonne
      with col1:
        if var == 'IncidentGroup':
            fonctionsgraph.graphQuali_boxplot(df2023, 'IncidentGroup')
        else:
            fonctionsgraph.graphQuali_countPlot(df2023, var)
    
      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        if var == 'IncidentGroup':
            fonctionsgraph.graphQuali_pointplot(df2023, 'IncidentGroup')
        else:
            fonctionsgraph.graphQuali_meanPlot(df2023, var, rest=50)

      with st.expander(f"📌 Interprétation"):
        st.write(df2023['IncidentGroup'].value_counts(normalize=True))
        st.markdown(texte_justifie(
            "La distribution des temps est similaire selon le type d'incident. "
            "Sur le temps total moyen, il y a moins de 3% d'écart entre le temps le plus long (IncidentGroup=Special Service)"
            " et le plus cours (False Alarm)<br>"
            "La seconde variable indiquant le type d'incident : DetailedIncidentGroup est plus détaillée que IncidentGroup,"
            " avec 27 catégories différentes (chacune n'appartenant qu'à une seule catégorie de IncidentGroup)."
            " La répartition de DetailedIncidentGroup est hétérogène.<br>"
            "Un peu plus de 40% des incidents sont une fausse alarme du type AFA (automatic fire alarm). "
            "Les cinq catégories suivantes relèvent d'un autre type de fausse alarme, d'un 1er ou 2nd feu, d'une inondation"
            " (flooding) ou d'une gestion d'entrée/sortie de personnes. La différence entre la moyenne la plus forte et la plus"
            " faible est de l'ordre de 40% pour le temps de réaction, le temps de trajet et le temps total."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("### Variables explicatives de propriété")
      st.markdown(texte_justifie(
        "Comme pour le type d'incident il existe deux variables descriptives : <code>'PropertyCategory'</code> et"
        " <code>'HighPropertyType'</code> qui donnent une information plus ou moins détaillée sur le type de propriété.")
        , unsafe_allow_html=True)
      
      # Choix de l'arbre affiché
      var_liste = ['PropertyCategory','DetailedIncidentGroup']
      # Menu déroulant pour un choix unique
      var = st.selectbox("Choisissez une variable d'intérêt :", var_liste)
      
      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale
      
      # Affichage du premier graphique dans la première colonne
      with col1:
        fonctionsgraph.graphQuali_countPlot(df2023, var)
    
      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_meanPlot(df2023, var, rest=50)
    
      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "La distribution des temps est similaire selon le type de propriété. "
            "La différence entre la moyenne la plus forte et la plus faible est de l'ordre de 10% "
            "pour le total.<br>"
            "Pour la variable qui détaille plus finement le type de propriété impacté par l'incident ;"
            " chaque catégorie de HighPropertyType appartient à une seule catégorie de PropertyCategory."
            " Il est donc cohérent de voir que plus de 60% des incidents ont lieu dans un immeuble d'habitation"
            " (catégorie majoritaire parmi les bâtiments d'habitation).<br>"
            "La différence entre la moyenne la plus forte et la plus faible est supérieur à 15% pour le temps total."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("### Distance")
      st.markdown(texte_justifie(
        "La distance est la seule variable explicative quantitative de notre jeu de données."
        " Elle varie de 0,6 mètre à 18,8 kilomètres. Sa distribution est asymétrique à droite, 50%"
        " des valeurs étant comprise entre 0.87 et 2,2 kilomètres.")
        , unsafe_allow_html=True)

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      with col1:
        st.image("Donnees/Images/rep_distance.png",use_container_width=True)
    
      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        st.image("Donnees/Images/graph_distance.png",use_container_width=True)
    
      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "La distance influence le temps de trajet ce qui est logique.<br>"
            " Nous avons calculé les corrélations linéaires (Pearson) , monotones (Spearman) et de rang (Pearson)."
            " Les plus fortes sont obtenues avec la méthode de Spearman. Pour le temps de réponse total, cette corrélation"
            " est de 0,66.<br>"
            "Remarque : la methode de Spearman est non paramétrique; elle ne fait pas d'hypothèse de normalité sur les"
            " variables. Compte tenu de la distribution de la distance (voir figure ci-dessus), cette méthode est plus "
            "adaptée que Pearson (hypothèse de normalité)"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fonctionsgraph.afficher_correlations(df2023,'distance')
      
      st.markdown("### RatioSC")
      st.markdown(texte_justifie(
        "")
        , unsafe_allow_html=True)      

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      with col1:
        fonctionsgraph.graph_countIncident(df2023, 'ratioSC')
    
      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_pointplot(df2023, 'ratioSC')

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
                "A FAIRE"
                )
                , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        fonctionsgraph.afficher_correlations(df2023,'ratioSC')
    
      
    


