import streamlit as st

from fonctions import texte_justifie

def pretraitement():
    st.title("Prétraitement")
    
    st.markdown(texte_justifie(
        "Une grande partie du prétraitement à déjà été effectué lors des étapes précédentes (nétoyage des données, "
        "transformation des données, ajout de données ...).")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Pour cette étapes nous avons : "
        "<ul>"
            "<li> Standardisé les variables quantitatives restantes (cette manipulation sera faite après la division du jeu"
            "de données)."
            "<ul>"
                "<li><code>distance</code> : standardisation à l'aide de <code>RobustScaler</code> qui prend en compte"
                " la médiane et l'intervalle interquartile,</li>"
                "<li><code>ratioSC</code> : standardisation à l'aide de <code>MinMaxScaler</code> qui réduit l'intervalle "
                "de variation de la variable de manière proportionnelle.</li>"
            "</ul></li>"
            "<li> Binariser les variables quatégorielles, c'est à dire <code>IncGeo_BoroughCode</code> et "
            "<code>PropertyCategory</code>.</li>"
        "</ul>"
        "Après ces étapes nous avons à notre disposition un ensemble de 1 037 713 incidents décrit par 50 variables explicatives"
        "(48 binaires + 2 continues)")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Pour la variables cibles nous avons été amené à évoluer au cours de nos travaux, notre variable cible"
        " a donc été transformé. Voici les différentes étapes de son évolution."
        "<ul>"
            "<li> <b> Etape 1 :</b> <code>TotalResponseTime_BC</code> variable continue après transformation "
            "Box-Cox du temps de réponse,</li>"
            "<li> <b> Etape 2 :</b> <code>TotalResponseTime_Category</code> variable qualitative où chacune des"
            " dix catégories représente un intervalle de temps de réponse,</li>"
            "<li> <b> Etape 3 :</b> <code>TotalResponseTime_Category2</code> variable qualitative où chacune des"
            " six catégories représente un intervalle de temps de réponse,</li>"
            "<li> <b> Etape 4 :</b> <code>TotalResponseTime_Binary</code> variable binaire qui vaut 1 si le "
            "temps de réponse est ou égal à 6 minutes et 0 sinon (70,6% des incidents)</li>"     
        "</ul>")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "La dernière chose à faire avant de passer à la modélisation à été de séparer notre jeu de données."
        "Au vue de l'importance du nombre d'incidents, nous avons séparé notre jeu de données en trois datasets."
        " Un jeu d'entrainement (<code>train_df</code>) représentant 70% des données, un jeu de validation "
        "(<code>validation_df</code>) représentant 15% des données et un jeu de test "
        "(<code>test_df</code>) représentant 15% des données. De plus des jeux de données réduits ont été crée pour"
        " faciliter l'entrainement des modèles.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

