import streamlit as st
import pandas as pd
import os

from fonctions import texte_justifie
from fonctionsstat  import tab_stat


def visualisation():
    st.markdown(texte_justifie(
        "A ce stade notre dataframe représentant l'ensemble des incidents est composé de plus d'un millions de"
        " lignes représentant chacune un incident et de ??? variables représentant soit une information sur la "
        "description de l'incident soit la variable cible (temps). Un grand nombre des variables est qualitative"
        " et seulement sont des variables quantitatives (<code>Time*</code>, <code>Distance</code> et <code>Ratio</code>)."
        " Le tableau ne contient plus de valeurs manquantes, mais certaines valeurs extrème n'ont pas été retirées.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "A vue du grand nombre de données et après une étude préalable pour cette partie nous n'utiliserons que les données"
        " de 2023.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## Statistiques descriptives sur les variables quantitatives")
    
    st.markdown(texte_justifie(
        "Une rapide étude statistique nous donne les informations suivantes :")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df2023 = pd.read_csv("Donnees/Doc csv/df2023.csv")
    tab = tab_stat(df2023)

    st.table(tab)

    st.markdown("## Data Visualisation")

    st.markdown(texte_justifie(
        "Au vue de la distribution de la variable cible (temps total), nous avons dans un premier temps effectué"
        " une transformation Box-Cox pour tenter de rendre la variable le plus similaire possible à une distribution "
        "normale. De plus plus seuls certains graphiques sont présentés ici.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Informations temporelles")

    st.markdown(texte_justifie(
        "Au vue de la distribution de la variable cible (temps total), nous avons dans un premier temps effectué"
        " une transformation Box-Cox pour tenter de rendre la variable le plus similaire possible à une distribution "
        "normale.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Création des colonnes
    col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

    # Affichage du premier graphique dans la première colonne
    with col1:
        image_path = os.path.join("Donnees", "figures", "repartion_variable_HourOfCall.png")
        st.image(image_path)

    # Affichage du deuxième graphique dans la deuxième colonne
    with col2:
        image_path = os.path.join("Donnees", "figures", "evolution_HourOfCallboxcox_TotalResponseTime.png")
        st.image(image_path)

    st.markdown(texte_justifie(
        "L'influence de l'heure de l'incident sur le temps de réactions est visible sur le graphique numéro 2. Ce qui"
        " peut s'expliquer du côté métier (heure de traffic, disponibilité en heure creuse). Des influences sont aussi visibles "
        "entre le jour et le temps, ainsi que le mois et le temps mais ne sont pas significatif (influence sur les variatipns de "
        "l'ordre de 2% pour les jours et de l'ordre de 3% pour les mois très inférieur à 5% qui est notre seuil)")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Informations géographiques")

    st.markdown(texte_justifie(
        "Les incidents sont inégalement répartis géographiquement que ce soit par arrondissements, quartiers "
        "(sous division d'arrondissement) ou caserne. Ces variables étant fortement corrélées nous avons décidé "
        "de n'inclure que l'arrondissement (33 modalités) pour éviter d'inclure des variables liées et pour limiter"
        " le temps de calcul.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown(texte_justifie(
        "Les deux graphiques ci-dessous représentent l'évolution du temps de réponse (Box-Cox) en "
        "fonction de la distance d'une part et en fonction du ratio superficie caserne d'autre part.")
        , unsafe_allow_html=True)
    
    # Création des colonnes
    col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

    # Affichage du premier graphique dans la première colonne
    with col1:
        image_path = os.path.join("Donnees", "figures", "evolution_distanceboxcox_TotalResponseTime2.png")
        st.image(image_path)

    # Affichage du deuxième graphique dans la deuxième colonne
    with col2:
        image_path = os.path.join("Donnees", "figures", "evolution_ratioSCboxcox_TotalResponseTime.png")
        st.image(image_path)

    st.markdown(texte_justifie(
        "Ces deux graphiques montrent une relation avec ces deux variables ce qui s'explique par le fait"
         " que le temps de trajet est influencé mécaniquement par la distance et qu'il est aussi influencé "
         "par le nombre caserne proche information données par <code>ratioSC</code>")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Informations relationnelles caserne(déployées/responsable), arrondissement")

    st.markdown(texte_justifie(
        "Ces informations sont données par les variables : <code>Bor_resp_rep</code>, <code>Bor_inc_rep</code> et"
        " <code>Bor_inc_resp</code>, pour enivron 65% des incidents, ces trois variables sont nulles "
        "ce qui indique que l'arrondissement correspond à la caserne (déployée et responsable). De plus l'écart sur"
        " le temps moyen d'intervention est supérieur à 5% pour deux de ces variables (<code>Bor_resp_rep</code> : 14%,"
        " <code>Bor_inc_rep</code> : 10% et <code>Bor_inc_resp</code> : 4%).")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## Variables sélectionnées pour le machine learning")

    st.markdown(texte_justifie(
        "Pour sélectionner nos variables nous avons utilisé les critères suivants :"
        "<ul>"
            "<li> Les variables quantitatives (distance et densité)"
            "<ul>"
                "<li> Tendance sur les graphiques,</li>"
                "<li> Test de corrélation de Spearman est significatif.</li>"
            "</ul></li>"
            "<li> Les variables qualitatives (toutes les autres)"
            "<ul>"
                "<li> Ecart entre la moyenne du temps par catégorie la plus forte et la plus faible est supérieur à 5%</li>"
                "<li> Test d’ANOVA est significatif</li>"
            "</ul></li>"
        "</ul>")
        , unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Suites aux  différentes analyses nous avons décidé de travailler avec les variables explicatives suivantes :"
        "<ul>"
            "<li><code>HourOfCall</code> : l'heure de l'incident. Pour limiter le nombre de variables, nous avons plutôt"
            " utilisé deux variables binaires : H26 qui vaut 1 entre 2 et 6 heures (0 sinon) et H1117 qui vaut 1 entre 11"
            " et 17 heures. Ces intervalles correspondent au temps moyen de réponse les plus longs,</li>"
            "<li><code>IncGeo_BoroughCode</code> : l'arrondissement,</li>"
            "<li><code>ratioSC</code> : représentant la superficie affectée a une caserne </li>,"
            "<li><code>Stat_resp_rep</code> : variable binaire indiquant si la caserne responsable est la même que la caserne"
            " de départ</li>"
            "<li><code>Bor_inc_rep</code> : variable binaire indiquant si l'arrondissement de l'incident est le même que celui "
            "de la caserne répondante,</li>"
            "<li><code>Bor_resp_rep</code> : variable binaire indiquant si l'arrondissement de la caserne responsable est le même"
            " que celui de la caserne répondante,</li>"
            "<li><code>PropertyCategory</code> : le type de propriété impacté dans l'incident,</li>"
            "<li><code>distance</code> : la distance (à vol d’oiseau) entre le lieu d’incident et la caserne répondante.</li>"
        "</ul>")
        , unsafe_allow_html=True)

