import streamlit as st

from fonctions import texte_justifie

def methodologie():
    st.title("Méthodologie")
    
    st.markdown(texte_justifie(
        "Comme indiqué précédement nous avons fait évoluer notre variable cible, en passant d'une variable"
        " continue à des variables catégorielles avec de moins en moins de modalités. Dans une première étape, nous avons "
        "testé des modèles sur les quatre variables cibles. Puis nous avons affiné la modélisation après avoir sélectionné "
        "la variable cible la plus appropriée et la famille de modèles la plus pertinente."
        )
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Etape 1", "Etape 2"])



    with tab1:   

        st.subheader("Première étape de modélisation")

        st.markdown("#### Jeux de données utilisés")
        st.markdown(texte_justifie(
            "Dans cette première étape de modélisation, nous avons utilisé le dataset <code>train</code> pour entraîner les modèles et "
            "<code>validation</code> pour estimer leurs performances. Nous avons testé des modèles sur les quatre variables cibles, soit une continue et trois catégorielles."
            )
        , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### Variable cible continue")
        st.markdown(texte_justifie(
            "Nous avons modélisé le temps de réponse, après transformation Box-Cox (TotalResponseTime_BC). L’objectif est de prédire la durée exacte "
            "(en minutes et secondes) en fonction des 50 variables explicatives."
            "<ul>"
                "<li><u>Modèles utilisés</u> : régressions linéaires pénalisées ou non et modèles non linéaires "
                "basés sur des algorithmes de classification tels que les arbres de décision, les forêts aléatoires et d’autres plus complexes "
                "utilisant des méthodes de boosting."
                "</li>"
                "<li><u>Evaluation des modèles</u> utililisation de métriques (coefficient de détermination (R²) pour les régression linéaires et RMSE pour tous les modèles) et "
                "évaluation graphique (valeurs prédites versus observées et graphique des résidus).</li>")
        , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### Variables cibles catégorielles")
        st.markdown(texte_justifie(
            "La modélisation du temps de réponse (variable continue) permet une prédiction fine mais peut être plus sensible aux variations et aux erreurs "
            "de mesure. À l’inverse, la classification des catégories de temps de réponse peut simplifier l’interprétation et faciliter la mise en place de "
            "seuils décisionnels concrets pour l’optimisation des interventions. "
        "<ul>"
            "<li><u>Modèles utilisés :</u> Support Vector Machine (SVM), K-plus voisins (KNN), Arbre de décision, Forêt aléatoire"
            " et trois algorithmes de boosting (Gradient Boosting, XGB et LGBM). Pour la variable cible binaire le modèle "
            "de régression logistique a aussi été testé.</li>"
            "<li><u>Evaluation des modèles</u> : utililisation de métriques (accuracy, précision, rappel et f1-score."
            "Nous avons utilisé les valeurs médianes / minimales / maximales de ces mesures pour les variables multi-catégorielles "
            "afin faciliter l’analyse (au vu du nombre élevé de catégories). "
            " </li>")
        , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### Recherche des hyper-paramètres")
        st.markdown(texte_justifie(
            "Que ce soit pour la modélisation de la variable continue ou des catégorielles, "
            "pour tous les modèles avec hyper-paramètres, nous avons réalisé une première estimation en les fixant de façon aléatoire puis nous avons "
            "effectué une recherche pour sélectionner les meilleurs possibles. Nous avons alors utilisé un jeu de données réduit (avec 140 000 incidents) "
            "afin de diminuer les temps de calcul. Une fois les hyper-paramètres sélectionnées, le modèle était entraîné sur le jeu de données complet."    
        ), unsafe_allow_html=True)

        st.markdown(texte_justifie(
        "Dans le cas de la variable cible binaire, comme les résultats étaient satisfaisants, nous avons fait deux recherches d’hyper-paramètres. La première a été "
        "effectuée en utilisant le jeu de données réduit avec 140 000 incidents (#1). La seconde a été faite sur un jeu de données avec 215 000 incidents (#2) et après "
        "modification du domaine de recherche des hyper-paramètres (basée sur les résultats de la première recherche). "
        ), unsafe_allow_html=True)

    with tab2:
        st.subheader("Seconde étape de modélisation")
        st.markdown(texte_justifie(
            "Les résultats sur la variable cible continue et les deux multi-catégorielles sont mauvais. En revanche, ceux de la variable binaire sont satisfaisants. "
            "Nous avons travaillé uniquement sur cette variable dans la seconde étape et sur un sous-ensemble de modèles (ceux avec les meilleurs résultats en étape 1). "
            "Nous avons utilisé le dataset <code>train2</code> (qui correspond au regroupement de "
            "<code>train</code> et <code>validation</code>) pour entraîner les modèles et "
            "<code>test</code> pour estimer leurs performances")
        , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)