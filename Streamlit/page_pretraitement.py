import streamlit as st

from fonctions import texte_justifie

def pretraitement():
    st.title("Prétraitement additionnel")

    st.markdown(texte_justifie(
        "Une grande partie du preprocessing a déjà été décrite : nettoyage des données, création de variables supplémentaires, "
        "transformation de la variable cible et sélection des variables explicatives. Une fois toutes ces étapes faites, nous avons"
        ), unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "<ul>"
            "<li><b>binarisé les variables multi-catégorielles</b> <code>IncGeo_BoroughCode</code> et <code>PropertyCategory</code>. Il y a donc 50 variables "
            "explicatives incluses dans nos modèles (48 binaires + 2 continues). </li>"
            
            "<li><b>séparé la base en trois jeux de données</b> (ou datasets) pour entraîner (<code>train_df</code>, 70% des incidents), "
            "valider (<code>validation_df</code>, 15%) et tester (<code>test_df</code>, 15%) nos modèles. "
            "De plus des jeux de données réduits ont été crées pour faciliter l'entrainement des modèles dans certains cas (sélection des hyper-paramètres).</li>"
            "<li><b>standardisé les deux variables quantitatives</b> <code>distance</code> et <code>ratioSC</code> (soit <code>distStd</code> et <code>ratioStd</code>). "
            "Nous avons utilisé la standardisation <code>RobustScaler</code> (qui utilise la médiane et l'interquartile) pour la distance et <code>MinMaxScaler</code> pour le ratio "
            "qui réduit l'intervalle de variation de la variable de manière proportionnelle</li>"
        "</ul>"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

