import streamlit as st
from fonctions import texte_justifie

def variables():
    st.title("Sélection des variables du modèle")

    tab1, tab2 = st.tabs(["Variable cible", "Variables explicatives"])



    with tab1:
        st.subheader("Transformations additionnelles du temps de réponse") 
        st.markdown(texte_justifie(   
            "Nous avons été amenés à considérer quatre variables cibles différentes pour la modélisation :"
            "<ul>"
            "<li> <code>TotalResponseTime_BC</code> :  variable continue après transformation "
            "Box-Cox du temps de réponse</li>"
            "<li> <code>TotalResponseTime_Category</code> : variable qualitative où chacune des"
            " dix catégories représente un intervalle de temps de réponse,</li>"
            "<li> <code>TotalResponseTime_Category2</code> : variable qualitative où chacune des"
            " six catégories représente un intervalle de temps de réponse</li>"
            "<li> <code>TotalResponseTime_Binary</code> variable binaire qui vaut 1 si le "
            "temps de réponse est ou égal à 6 minutes et 0 sinon (70,6% des incidents)</li>"
            "</ul>"
            "Les intervalles de temps pour les variables qualitatives ont été choisis de sorte à répartir équitablement les incidents dans "
            "ces catégories, tout en prenant en compte la limite de 6 minutes car la Brigade des Pompiers de Londres a pour objectif "
            "d'avoir un temps moyen de réponse inférieur à 6 minutes."
            "<br><br>")
        , unsafe_allow_html=True)
        st.image("Donnees/Images/Variables_cibles_categorisees.png",use_container_width=True) 
    
    with tab2:
        st.subheader("Sélection des variables explicatives")


        with st.expander(f"Méthode pour le choix"):
            st.markdown(texte_justifie(
            "Pour sélectionner les variables, nous avons utilisé les critères suivants :"
            "<ul>"
                "<li> Pour les variables quantitatives (distance et ratio),"
                "<ul>"
                    "<li> On observe une tendance sur les graphiques</li>"
                    "<li> Le test de corrélation de Spearman est significatif (erreur de type I fixée à 5%).</li>"
                "</ul></li>"
                "<li> Pour les variables qualitatives (toutes les autres),"
                "<ul>"
                    "<li> L'écart entre la moyenne du temps de réponse par catégorie la plus forte et la plus faible est supérieur à 5%</li>"
                    "<li> Le test d’ANOVA est significatif</li>"
                "</ul></li>"
            "</ul>")
            , unsafe_allow_html=True)

        st.markdown(texte_justifie(
        "À la suite des analyses décrites dans les pages précédentes, nous avons inclus dans le modèle les variables explicatives suivantes  :"
        "<ul>"
            "<li><code>distance</code> : la distance (à vol d’oiseau) entre le lieu d’incident et la caserne répondante</li>"
            "<li><code>ratioSC</code> : la superficie moyenne d'un arrondissement affectée a une caserne spécifique</li>"
            "<li><code>HourOfCall</code> : l'heure de l'incident. Pour limiter le nombre de variables, nous avons plutôt"
            " utilisé deux variables binaires : <code>H26</code> qui vaut 1 entre 2 et 6 heures (0 sinon) et <code>H1117</code> qui vaut 1 entre 11"
            " et 17 heures. Ces intervalles correspondent au temps moyen de réponse les plus longs.</li>"
            "<li><code>IncGeo_BoroughCode</code> : l'arrondissement</li>"
            "<li><code>Stat_resp_rep</code> : variable binaire indiquant si la caserne responsable est la même que la caserne"
            " de départ</li>"
            "<li><code>Bor_inc_rep</code> : variable binaire indiquant si l'arrondissement de l'incident est le même que celui "
            "de la caserne répondante</li>"
            "<li><code>Bor_resp_rep</code> : variable binaire indiquant si l'arrondissement de la caserne responsable est le même"
            " que celui de la caserne répondante</li>"
            "<li><code>PropertyCategory</code> : le type de propriété impacté dans l'incident</li>"

        "</ul>")
        , unsafe_allow_html=True)
