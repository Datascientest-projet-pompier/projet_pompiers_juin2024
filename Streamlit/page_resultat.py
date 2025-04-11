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
        "Dans cette partie, nous montrons uniquement les résultats de l'étape 2 de modélisation. "
        "Il concerne uniquement la variable cible binaire, <code>TotalResponseTime_Binary</code>. "
        "L'ensemble des notebooks de travail sont accessibles sur le dépôt Github "
        "<a href=\"https://github.com/Datascientest-projet-pompier/projet_pompiers_juin2024/tree/main\">ICI</a>. "
        "Les résultats de l'étape 1 pour chacune des quatre variables cibles sont commentés dans ces notebooks."
        )
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander(f"📌 Métriques Utilisées"):

        st.markdown(texte_justifie(
          "<ul><li><b>L'accuracy</b> mesure la proportion de prédictions correctes par rapport au nombre total d'observations. C'est une mesure globale de la performance du modèle."
          "</li></ul>")
        , unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image("Donnees/Images/Formule_accuracy.png",use_container_width=True, width=400) 
        with col3:
            st.write(' ')
        
        st.markdown(texte_justifie(
          "<ul><li><b>La précision</b>, pour chaque classe, mesure la proportion de valeurs correctement prédites (dans cette classe) par rapport au nombre total de ses prédictions."
          "</li></ul>")
        , unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image("Donnees/Images/Formule_precision.png",use_container_width=True, width=400) 
        with col3:
            st.write(' ')

        st.markdown(texte_justifie(
          "<ul><li><b>Le rappel</b>, pour chaque classe, mesure la proportion de valeurs correctement prédites (dans cette classe) par rapport au nombre total de ses observations."
          "</li></ul>")
        , unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image("Donnees/Images/Formule_recall.png",use_container_width=True, width=400) 
        with col3:
            st.write(' ')


        st.markdown(texte_justifie(
          "<ul><li><b>Le F1-score</b>, pour chaque classe, mesure la moyenne harmonique de la précision et du rappel."
          "</li></ul>")
        , unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image("Donnees/Images/Formule_f1score.png",use_container_width=True, width=400) 
        with col3:
            st.write(' ')

        st.markdown(texte_justifie(
          "<ul><li><b>L'AUC</b> mesure l'air sous la courbe ROC. Cette courbe indique le taux vrais positifs (ou rappel) en fonction du taux de faux positifs (ou spécificité). "
          "Elle mesure de la capacité du modèle à distinguer les classes."
          "</li></ul>")
        , unsafe_allow_html=True)            

    
    st.markdown("##### Résultats sur le jeu d'entraînement")
    st.markdown(texte_justifie(
        "Le tableau ci-dessous résume les mesures obtenues pour les différents modèles sur le jeu de données d'entraînement, <code>train2</code> (fusion de "
        "<code>train</code> et <code>validation</code>). <br><br>")
    , unsafe_allow_html=True)

    st.table(df_train.set_index('Modèle'))
    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("##### Résultats sur le jeu test")


    st.markdown(texte_justifie(
        "Le tableau ci-dessous résume les mesures obtenues pour les différents modèles sur le jeu de données test, <code>test</code>. <br><br>")
    , unsafe_allow_html=True)
    st.table(df_test.set_index('Modèle'))
    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(texte_justifie(
        "En se basant sur les mesures obtenues sur le jeu de données test, nous avons sélectionné comme modèle final celui de Gradient "
        "Boosting avec les hyper-paramètres obtenus à la suite de la seconde optimisation (<b>Gradient Boosting#2</b>). "
        )
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander(f"📌 Hyper-paramètres du modèle"):

        st.code("""
                # Nombre d'arbres dans l'ensemble (forêt aléatoire)
                n_estimators = 400
                # Taux d'apprentissage, contrôle la contribution de chaque arbre
                learning_rate = 0.0464
                # Fraction des données utilisées pour chaque arbre : 87.5%
                subsample = 0.875
                # Fraction minimale d'échantillons requise pour diviser un nœud interne : 0,05%  (518 incidents dans train2)
                min_samples_split = 0.0005
                # Profondeur maximale de chaque arbre : 9 niveaux
                max_depth = 9
                # Nombre maximal de caractéristiques considérées pour chaque division : 25 (sur 50)
                max_features = 25
                """, language="python")
