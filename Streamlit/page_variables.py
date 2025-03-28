import streamlit as st
from fonctions import texte_justifie

def variables():
    st.title("Les Variables du modèle")
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

