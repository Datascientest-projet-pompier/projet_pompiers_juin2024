import streamlit as st

from fonctions import texte_justifie

import pandas as pd

data = {
    'Modèle': ['Forêt aléatoire #1', 'Gradient Boosting #2', 'XG Boost #2', 'LGBM #2', 'XG Boost #1', 'LGBM #1', 'Gradient Boosting #1'],
    'Accuracy': ['0.8295', '0.8095', '0.8087', '0.8078', '0.8077', '0.8061', '0.8043'],
    'Precision_0': ['0.8450', '0.8321', '0.8312', '0.8310', '0.8303', '0.8294', '0.8267'],
    'Precision_1': ['0.7755', '0.7308', '0.7300', '0.7271', '0.7281', '0.7244', '0.7241'],
    'Recall_0': ['0.9291', '0.9150', '0.9151', '0.9138', '0.9146', '0.9134', '0.9147'],
    'Recall_1': ['0.5898', '0.5556', '0.5526', '0.5527', '0.5502', '0.5479', '0.5385'],
    'F1score_0': ['0.8850', '0.8716', '0.8711', '0.8704', '0.8704', '0.8694', '0.8685'],
    'F1score_1': ['0.6700', '0.6313', '0.6290', '0.6280', '0.6268', '0.6239', '0.6177'],
    'AUC ROC': ['0.7594', '0.7353', '0.7338', '0.7332', '0.7324', '0.7306', '0.7266']
}
df_train = pd.DataFrame(data)

data = {
    'Modèle': ['Gradient Boosting #2', 'Forêt aléatoire #1', 'LGBM #2', 'XG Boost #2', 'XG Boost #1', 'LGBM #1', 'Gradient Boosting #1'],
    'Accuracy': ['0.8050', '0.8045', '0.8043', '0.8043', '0.8042', '0.8035', '0.8025'],
    'Precision_0': ['0.8280', '0.8274', '0.8277', '0.8271', '0.8269', '0.8266', '0.8245'],
    'Precision_1': ['0.7241', '0.7236', '0.7224', '0.7237', '0.7239', '0.7219', '0.7234'],
    'Recall_0': ['0.9132', '0.9133', '0.9126', '0.9135', '0.9138', '0.9130', '0.9148'],
    'Recall_1': ['0.5456', '0.5437', '0.5448', '0.5425', '0.5417', '0.5412', '0.5335'],
    'F1score_0': ['0.8685', '0.8682', '0.8681', '0.8682', '0.8681', '0.8677', '0.8673'],
    'F1score_1': ['0.6223', '0.6209', '0.6212', '0.6201', '0.6197', '0.6186', '0.6141'],
    'AUC ROC': ['0.7294', '0.7285', '0.7287', '0.7280', '0.7277', '0.7271', '0.7242']
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
