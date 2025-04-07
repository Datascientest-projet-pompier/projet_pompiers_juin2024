import streamlit as st

from fonctions import texte_justifie

import pandas as pd

data = {
    'Modèle': ['Forêt aléatoire #1', 'Gradient Boosting #2', 'XG Boost #2', 'LGBM #2', 'XG Boost #1', 'LGBM #1', 'Gradient Boosting #1'],
    'Accuracy': ['82.95', '80.95', '80.87', '80.78', '80.77', '80.61', '80.43'],
    'Precision_0': ['84.50', '83.21', '83.12', '83.10', '83.03', '82.94', '82.67'],
    'Precision_1': ['77.55', '73.08', '73.00', '72.71', '72.81', '72.44', '72.41'],
    'Recall_0': ['92.91', '91.50', '91.51', '91.38', '91.46', '91.34', '91.47'],
    'Recall_1': ['58.98', '55.56', '55.26', '55.27', '55.02', '54.79', '53.85'],
    'F1score_0': ['88.50', '87.16', '87.11', '87.04', '87.04', '86.94', '86.85'],
    'F1score_1': ['67.00', '63.13', '62.90', '62.80', '62.68', '62.39', '61.77'],
    'AUC ROC': ['75.94', '73.53', '73.38', '73.32', '73.24', '73.06', '72.66']
}
df_train = pd.DataFrame(data)

data = {
    'Modèle': ['Gradient Boosting #2', 'Forêt aléatoire #1', 'LGBM #2', 'XG Boost #2', 'XG Boost #1', 'LGBM #1', 'Gradient Boosting #1'],
    'Accuracy': ['80.50', '80.45', '80.43', '80.43', '80.42', '80.35', '80.25'],
    'Precision_0': ['82.80', '82.74', '82.77', '82.71', '82.69', '82.66', '82.45'],
    'Precision_1': ['72.41', '72.36', '72.24', '72.37', '72.39', '72.19', '72.34'],
    'Recall_0': ['91.32', '91.33', '91.26', '91.35', '91.38', '91.30', '91.48'],
    'Recall_1': ['54.56', '54.37', '54.48', '54.25', '54.17', '54.12', '53.35'],
    'F1score_0': ['86.85', '86.82', '86.81', '86.82', '86.81', '86.77', '86.73'],
    'F1score_1': ['62.23', '62.09', '62.12', '62.01', '61.97', '61.86', '61.41'],
    'AUC ROC': ['72.94', '72.85', '72.87', '72.80', '72.77', '72.71', '72.42']
}

df_test = pd.DataFrame(data)

def resultat():
    st.title("Quelques résultats")

    st.markdown(texte_justifie(
        "Dans cette partie nous ne montrerons que les résultats associés à la variable cible binaire <code>TotalResponseTime_Binary</code>."
        " L'ensemble des notebooks de travail sont accessibles sur le depot Github "
        "<a href=\"https://github.com/Datascientest-projet-pompier/projet_pompiers_juin2024/tree/main\">ICI</a>.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "L'entrainement des modèles c'est effectué en plusieurs étapes.")
    , unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Dans un premier temps les modèles sont lancés sur deux jeux de données réduits. "
        "Le premier contenant 140 000 incidents(#1) et le second contenant 250 000 incidents(#2). Avec les "
        "hyperparamètres trouvés le modèle est entrainé sur le jeu de données complet. Puis sur le jeu de données de validation. Puis"
        "sur le jeu de données de temps. ")
    , unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Dans un second temps les jeux de données d'entrainement et de validation sont fusionné. Le modèle est"
        " ensuite entrainer (sur le jeu fusionné) puis testé sur le jeu de données de test.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(r"""
        Cinq métriques sont utilisées :

        - **L'accuracy :** mesure la proportion de prédictions correctes par rapport au nombre total de prédictions. C'est une mesure globale de la performance du modèle,

        - **La précision :** mesure la précision pour chacune des classes(0 ou 1). Précision 0 renvoie la proportion de valeur prédite à 0 étant réellement à 0 par rapport au total des valeur 0.

        $$R_0=\frac{Vrais Positifs}{Vrais Positifs + Faux Positifs} $$

        idem pour Précision 1,

        - **Le Recall :** mesure la proportion de toutes les instances positives réelles qui ont été correctement identifiées par le modèle.

        $$F1_0=\frac{Vrais Positifs}{Vrais Positifs + Faux Négatifs}$$

        - **F1-score :** mesure la moyenne harmonique de la précision et du rappel. Mathématiquement

        - **AUC ROC :** mesure l'air sous la courbe ROC(Nombre de vrais positifs (rappel) en fonction du taux de faux positifs), elle mesure de la capacité du modèle à distinguer les classes.
        """
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Résultats sur le jeu d'entrainement (fusionné).")
    , unsafe_allow_html=True)

    st.table(df_train.set_index('Modèle'))
    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(texte_justifie(
        "Résultats sur le jeu de test.")
    , unsafe_allow_html=True)
    st.table(df_test.set_index('Modèle'))


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(texte_justifie(
        "Le choix du modèle c'est effectué à l'aide des résultats sur le jeu de données test. Au vue des résultats"
        "le modèle convservé est celui de <b>Gradient Boosting#2</b>")
    , unsafe_allow_html=True)
