import streamlit as st

from fonctions import texte_justifie

def methodologie():
    st.title("Methodologie")
    
    st.markdown(texte_justifie(
        "Comme indiqué précédement nous avons fait évoluer notre variable cible, en passant d'une variable"
        " continue à des variables catégorielles avec de moins en moins de modalités.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Variable cible continue")
    st.markdown(texte_justifie(
        "<ul>"
            "<li><u>Modèles utilisés :</u> régression linéaire (pénalisée ou non) et modèle non linéaire. Pour déterminer les hyper"
            "-paramètres des modèles, le travail à été fait sur les jeux de données réduits.</li>"
            "<li><u>Evaluation des modèles :</u> coefficient de détermination (R²), racine de l'erreur quadratique (RMSE), "
            "graphique des valeurs prédites versus les valeurs observées et le graphique des résidus.</li>")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Variables cibles catégorielles")
    st.markdown(texte_justifie(
        "<ul>"
            "<li><u>Modèles utilisés :</u> Support Vector Machine (SVM), K-plus voisins (KNN), Arbre de décision, Forêt aléatoire"
            " et trois algorithmes de boosting (Gradient Boosting, XGB et LGBM). Pour la variable cible binaire le modèle "
            "de régression logistique a été testé.</li>"
            "<li><u>Evaluation des modèles :</u> utilisons de différentes métriques. L'exactitude (accuracy), la précision, le rappel"
            " (recall) et le f1-score.</li>")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

