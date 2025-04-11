import streamlit as st
import pandas as pd
import os
import numpy as np
import streamlit.components.v1 as components
from PIL import Image

from fonctions import texte_justifie
from fonctionsstat  import tab_stat
from fonctions import recup_df

import matplotlib.pyplot as plt

import fonctionsgraph

def lire_html(chemin_fichier):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier HTML : {e}")
        return None

def visualisation():
    st.title("Visualisation")

    st.markdown(texte_justifie(
        "Nous avons analysé le jeu de données (ou dataframe) obtenu précédemment avant de commencer la modélisation. "
        "L'objectif est de mieux connaître notre variable cible et de sélectionner les variables explicatives "
        "pertinentes à inclure dans les modèles testés.<br><br>"
        "Compte tenu du grand nombre d'observations (plus d'un million d'incidents sur 10 ans) et après une étude préalable, "
        "nous avons limité l'analyse qui suit aux incidents de 2023. "
        "A noter, il n'y a pas de valeur manquante dans le dataframe mais il peut y avoir des valeurs extrêmes ou aberrantes.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Récupération des données de 2023
    df2023 = pd.read_csv("Donnees/Doc csv/df2023_v2.csv")

    # Création des onglets
    tab1, tab2 ,tab3, tab4 = st.tabs(["Statistiques descriptives","Variable cible", "Variables explicatives","Visualisation géographique"])

    with tab1:
      st.subheader("Statistiques descriptives")
      st.markdown(texte_justifie(
        " Notre jeu de données contient un grand nombre de variables qualitatives et seulement cinq variables quantitatives dont le temps de réponse"
        " (décomposé en temps de réaction et de trajet), la distance et le ratio de la superficie de l'arrondissement par son nombre de casernes.<br>"        
        "Le tableau ci-dessous présente leurs statistiques descriptives :")
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

      tab = tab_stat(df2023)
      st.table(tab)
      
      with st.expander(f"📌 Interprétation"):

        st.markdown(texte_justifie(
          "En 2023, le temps total de réponse moyen est de 319 secondes (5 min 19 sec) avec un écart type de 130 secondes (2 min 10 sec). La distribution est asymétrique puisque 75% "
          "des temps est inférieur à 381 secondes (6 min 21 sec) et que le temps maximum est de presque 20 minutes. <br>"
          "Pour information, les données où le temps est supérieur à 20 minutes sont considérées (par la Brigade des Pompiers de Londres) comme des données aberrantes "
          "et sont donc supprimées en amont de la publication de la base de données. ")
        , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(texte_justifie(
          "En 2023, La distance moyenne parcourue par le camion (entre la caserne de départ et le lieu d'incident) "
          "est de 1,79 kilomètres avec un écart-type de 1,78 km. A nouveau, la distribution est asymétrique. "
          "A noter, cette donnée est approximée pour la moitié des incidents (imputation nécessaire pour les données manquantes de latitude et longitude).")
        , unsafe_allow_html=True)

    with tab2:
      st.subheader("Transformation du temps total de réponse")
      st.markdown(texte_justifie(
        "La variable cible est le temps total de réponse (<code>TotalResponseTime</code>) qui est la somme des temps"
        " de réaction (<code>TurnoutTime</code>) et de trajet (<code>TravelTime</code>). "
        " Les graphiques ci-dessous montrent la distribution de cette variable, elle est asymétrique."
        "<br>"), unsafe_allow_html=True)

      # Charger l'image avec PIL
      image = Image.open("Donnees/Images/temps-original.png")

      # Redimensionner l'image à 50%
      new_size = (image.width // 3*2, image.height // 3*2)
      resized_image = image.resize(new_size)

      # Centrer avec Streamlit
      st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
      st.image(resized_image)
      st.markdown("</div>", unsafe_allow_html=True)

      st.markdown(texte_justifie(
         "De nombreux modèles supposent que la distribution de la variable cible soit normale. Ce n'est pas le cas du temps de réponse. "
         "Nous avons donc décidé de tranformer notre variable cible pour approcher une distribution normale. "
        "Nous avons testé quatre transformations : logarithmique, racine carrée, Box-Cox et Yeo Jonhson.<br>"
        "<b>Nous avons sélectionné la transformation Box-Cox.</b>"
        )
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)
      # Choix de la transformation à afficher
      var_liste = ['Logarithmique','Racine carrée','Box-Cox','Yeo-Johnson']
      # Menu déroulant pour un choix unique
      var_transfo = st.selectbox("Choisissez une transformation :", var_liste)

      if var_transfo == 'Logarithmique':
        # Charger l'image avec PIL
        image = Image.open("Donnees/Images/temps-logarithme.png")

        # Redimensionner l'image à 50%
        new_size = (image.width // 3*2, image.height // 3*2)
        resized_image = image.resize(new_size)

        # Centrer avec Streamlit
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(resized_image)
        st.markdown("</div>", unsafe_allow_html=True)

      elif var_transfo == 'Racine carrée':
        # Charger l'image avec PIL
        image = Image.open("Donnees/Images/temps-racine-carree.png")

        # Redimensionner l'image à 50%
        new_size = (image.width // 3*2, image.height // 3*2)
        resized_image = image.resize(new_size)

        # Centrer avec Streamlit
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(resized_image)
        st.markdown("</div>", unsafe_allow_html=True)

      elif var_transfo == 'Box-Cox':
        # Charger l'image avec PIL
        image = Image.open("Donnees/Images/temps-boc-cox.png")

        # Centrer avec Streamlit
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(image)
        st.markdown("</div>", unsafe_allow_html=True)

      else:
        # Charger l'image avec PIL
        image = Image.open("Donnees/Images/temps-teo-jonhson.png")

        # Centrer avec Streamlit
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(image)
        st.markdown("</div>", unsafe_allow_html=True)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
         "La valeur de lambda estimée pour la transformation Yeo-Johnson est inférieur à 1. Il est donc attendu "
         "que les résultats soient similaires à la transformation Box-Cox. L'amélioration de la symétrie de la distribution est visible "
         "avec les transformations racine carré, Box-Cox et Yeo-Johnson. La transformation logarithmique modifie mais n'améliore pas les résultats du QQ-plot. "
         "Pour les autres transformations, les résultats sont meilleurs que ceux des données sur l’échelle d'origine pour les valeurs extrêmes. "
         "Pour les quantiles théoriques négatifs, les résultats sont meilleurs pour Box-Cox et Yeo-Johnson comparés à la transformation racine carrée."
        )
      , unsafe_allow_html=True) 
              
    with tab3:
      st.subheader("Graphiques sur les variables explicatives")

      st.markdown(texte_justifie(
        "Dans cette section, nous présentons notre analyse graphique de certaines des variables du jeu de données. "
        "L'objectif de cette étude était de sélectionner les variables explicatives à inclure dans notre modélisation."
        )
        , unsafe_allow_html=True)

      st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("#### Informations temporelles")
      # Choix de l'arbre affiché
      var_liste = ['HourOfCall','DayOfWeek','Month']
      # Menu déroulant pour un choix unique
      var_temps = st.selectbox("Choisissez une variable d'intérêt :", var_liste)

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      # Affichage du premier graphique dans la première colonne
      with col1:
        fonctionsgraph.graph_countIncident(df2023, var_temps)

      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_pointplot(df2023, var_temps)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "<ul><li><code>HourOfCall</code> : "
            "il y a un impact sur le temps moyen de réponse des pompiers de Londres. "
            "Le temps moyen de réponse est plus important sur les plages horaires 2-6h et 11-18h. "
            "De jour, le temps de trajet moyen augmente, spécialement sur la tranche 11-17h, plage horaire où "
            "le trafic est plus dense car l'activité humaine est plus intense. "
            "De nuit, le temps de réaction augmente car il y a moins de pompiers dans les casernes. "
            "Sur le temps total moyen, l'écart entre la valeur la plus forte (pour Hour=6h) "
            "et la plus faible (pour Hour=22h) est de l'ordre de 6%.</li>"
            
            "<li><code>DayOfWeek</code> : l'écart entre le temps total moyen le plus long (le vendredi) et le plus "
            "court (le jeudi) est de l'ordre de 2%.</li>"
            "<li><code>Month</code> l'écart entre le temps total moyen le"
            " plus long (en novembre) et le plus court (en avril) est de l'ordre de 3%.</li>"
            "Seule la variable <code>HourOfCall</code> montre cet écart de plus de 5% et le test ANOVA est significatif (p-value<5%)."
            "</ul>"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fonctionsgraph.test_anova(df2023, 'HourOfCall')

      st.markdown("#### Informations géographiques")
      # Choix de l'arbre affiché
      var_nom = ['Arrondissement', "Quartier", "Caserne de départ", "Bonne localisation", "Inner London"]

      # Menu déroulant pour un choix unique
      var_fr = st.selectbox("Choisissez une variable d'intérêt :", var_nom)
      indice = var_nom.index(var_fr)

      var_list = ['IncGeo_BoroughName','IncGeo_WardName','DeployedFromStation_Name','GoodLocation',"inner"]
      var_geo = var_list[indice]

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      # Affichage du premier graphique dans la première colonne
      with col1:
        if var_geo in ['GoodLocation','inner']:
            fonctionsgraph.graphQuali_boxplot(df2023, var_geo)
        else:
            fonctionsgraph.graphQuali_countPlot(df2023, var_geo)

      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        if var_geo in ['GoodLocation','inner']:
            fonctionsgraph.graphQuali_pointplot(df2023, var_geo)
        else:
            fonctionsgraph.graphQuali_meanPlot(df2023, var_geo, rest=50)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "<ul><li>Arrondissement (Borough): "
            "le temps de réponse moyen varie entre 25,7 à 30,1, soit une différence de 15% environ.</li>"
            "<li> Quartier (Ward) : il y a plus de 600 quartiers différents ; nous n'avons représenté qu'un partie "
            "correspondant aux 50 premiers/derniers pour lesquels la moyenne du temps de réponse "
            "est la plus forte/faible. Il y a une différence de l'ordre de 40% entre Darwin (temps moyen=36,1) et "
            "Norbury & Pollards Hill (21,3).</li>"
            "<li> Caserne de départ (du camion allant à l'incident) : il y a 102 casernes différentes. L'écart entre le temps moyen de la catégorie "
            "la plus forte et la plus faible est de l'ordre de 20%. </li>"
            "Le test ANOVA est significatif (p-value<5%) pour les 3 variables (résultats montrés pour l'arrondissement). "
            "Le quartier et la caserne sont des variables qualitatives avec beaucoup de catégories. L'information entre arrondissement et quartier est partiellement redondante."
            "</ul>"          
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fonctionsgraph.test_anova(df2023, 'IncGeo_BoroughName')

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(texte_justifie(
            "<ul>"
                "<li> Bonne localisation : l'écart entre le temps de réponse moyen des deux catégories est de l'ordre de 1%. "
                "De plus, cette variable est connue a posteriori.</li>"
            "</ul>"
            )
            , unsafe_allow_html=True)

        st.markdown(texte_justifie(
            "<ul>"
                "<li> Inner London : les arrondissements de Londres peuvent se situer au centre (inner London) ou non (outer London). "
                "L'écart entre le temps de réponse moyen des deux catégories est de l'ordre de 6% et le test ANOVA est significatif.</li>"
            "</ul>"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        fonctionsgraph.test_anova(df2023, 'inner')
        st.markdown("<br>", unsafe_allow_html=True)


      st.markdown("#### Information sur le type d'incident")
      st.markdown(texte_justifie(
        "Le type d'incident est décrit par trois variables : <code>Fire</code>, <code>IncidentGroup</code> et <code>DetailedIncidentGroup</code> "
        "qui donnent une information plus ou moins détaillée sur le type d'incident.")
        , unsafe_allow_html=True)

      # Choix de l'arbre affiché
      var_liste = ['Fire','IncidentGroup','DetailedIncidentGroup']
      # Menu déroulant pour un choix unique
      var_type = st.selectbox("Choisissez une variable d'intérêt :", var_liste)

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      # Affichage du premier graphique dans la première colonne
      with col1:
        if var_type == 'DetailedIncidentGroup':
            fonctionsgraph.graphQuali_countPlot(df2023, var_type)
        else:
            fonctionsgraph.graphQuali_boxplot(df2023, var_type)


      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        if var_type == 'DetailedIncidentGroup':
            fonctionsgraph.graphQuali_meanPlot(df2023, var_type, rest=50)
        else:
            fonctionsgraph.graphQuali_pointplot(df2023, var_type)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
           "Le tableau ci-dessous la répartition des incidents en fonction de la variable <code>IncidentGroup</code>. "
           "Plus de la moitié des incidents sont des fausses alarmes (déclenchement automatique d'alarme incendie ou appel)"
        ), unsafe_allow_html=True)
        st.write(df2023['IncidentGroup'].value_counts(normalize=True))
        st.markdown(texte_justifie(
            "Que ce soit sur les variables <code>Fire</code> ou <code>IncidentGroup</code>, la distribution des temps est"
            " similaire selon le type d'incident. Il y a moins de 3% d'écart entre le temps moyen le plus long"
            " et le plus court.<br><br>"
            "La troisième variable indiquant le type d'incident (<code>DetailedIncidentGroup</code>) est plus détaillée que"
            " <code>IncidentGroup</code>, avec 27 catégories différentes (chacune n'appartenant qu'à une seule catégorie "
            "de <code>IncidentGroup</code>). La répartition dans cette variable est hétérogène. Un peu plus de 40% des incidents"
            " correspond à une fausse alarme du type AFA (automatic fire alarm). La différence entre la moyenne du temps de réponse la plus forte et la plus"
            " faible est de l'ordre de 40%. Cependant, nous avons découvert que la plupart des catégories de cette variable ne peut être définie qu'a posteriori. "
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("#### Information sur le type de propriété impacté")
      st.markdown(texte_justifie(
        "Comme pour le type d'incident, il existe trois variables catégorielles "
        "qui donnent une information plus ou moins détaillée sur le type de propriété : "
        "<code>'PropertyCategory'</code>, <code>PropertyType</code> et <code>'HighPropertyType'</code> "
        " avec respectivement 3 , 47 et 293 modalités.")
        , unsafe_allow_html=True)

      # Choix de l'arbre affiché
      var_liste = ['PropertyCategory','HighPropertyType','PropertyType']
      # Menu déroulant pour un choix unique
      var_prop = st.selectbox("Choisissez une variable d'intérêt :", var_liste)

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      # Affichage du premier graphique dans la première colonne
      with col1:
        fonctionsgraph.graphQuali_countPlot(df2023, var_prop)

      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_meanPlot(df2023, var_prop, rest=50)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "Les temps de réponse moyens varient en fonction du type de propriété impacté (<code>'PropertyCategory'</code>). Le temps de réponse moyen "
            "pour un incident affectant un bateau est plus long de 10% que celui pour un incident sur un bâtiment résidentiel. De plus, le test ANOVA est "
            "significatif (p-value inférieure à 5%). Les résultats sont similaires pour les deux autres variables."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        fonctionsgraph.test_anova(df2023, 'PropertyCategory')



      st.markdown("#### Distance entre la caserne de départ et le lieu d'incident")
      st.markdown(texte_justifie(
        "La distance varie de 0,6 mètre à 18,8 kilomètres. Sa distribution est asymétrique à droite, 50%"
        " des valeurs étant comprise entre 0.87 et 2,2 kilomètres (pour les incidents 2023).")
        , unsafe_allow_html=True)

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      with col1:
        st.image("Donnees/Images/rep_distance.png",use_container_width=True)

      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        st.image("Donnees/Images/graph_distance.png",use_container_width=True)

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "On observe que le temps de réponse total augmente avec la distance. Sans surprise, "
            "c’est le temps de trajet qui est affecté par la distance et non le temps de réaction (résultats non montrés).<br>"
            " Nous avons calculé la corrélation linéaire (Pearson) , monotone (Spearman) et de rang (Pearson). Le tableau ci-dessous présente les résultats. "
            "La plus forte est obtenue avec la méthode de Spearman ; elle est de 0,66.<br>"
            "Remarque : la methode de Spearman est non paramétrique; elle ne fait pas d'hypothèse de normalité sur les"
            " variables. Compte tenu de la distribution de la distance (voir figure ci-dessus), cette méthode est plus "
            "adaptée que Pearson (hypothèse de normalité)"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fonctionsgraph.afficher_correlations(df2023,'distance')

      st.markdown("#### Ratio superficie de l'arrondissement / nombre de casernes")
      st.markdown(texte_justifie(
            "Bien que le nombre de valeurs possibles soit fini, la densité de casernes par arrondissement (<code>'ratioSC'</code>) est une variable continue "
            "(plutôt que catégorielle). En effet, si une caserne venait à être ajoutée dans un arrondissement, <code>'ratioSC'</code> pourrait prendre une "
            "nouvelle valeur. Le modèle pourrait rester valide si <code>'ratioSC'</code> est continue ; ce ne serait pas le cas si <code>'ratioSC'</code> est "
             "catégorielle. "
            )
            , unsafe_allow_html=True)


      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      with col1:
        fonctionsgraph.graph_countIncident(df2023, 'ratioSC')

      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_pointplot(df2023, 'ratioSC')

      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
                "Le temps total de réponse moyen augmente quand le ratio "
                "superficie/nombre de casernes augmente. C'est cohérent car plus ce ratio"
                " est fort, moins il y a de casernes au mètre carré (et donc elles ont en moyenne plus de distance à parcourir)."
                " Nous avons calculé la corrélation linéaire (Pearson) , monotone (Spearman) et de rang (Pearson). Le tableau ci-dessous présente les résultats. "
                "La plus forte est obtenue avec la méthode de Spearman ; elle est de 0,19.<br>"
                )
                , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        fonctionsgraph.afficher_correlations(df2023,'ratioSC')


      st.markdown("#### Indicatrices sur arrondissement et casernes")

      # Choix de l'arbre affiché
      var_nom = ['Stat_resp_rep', "Bor_resp_rep", "Bor_inc_rep", "Bor_inc_resp"]

      # Menu déroulant pour un choix unique
      var = st.selectbox("Choisissez une variable d'intérêt :", var_nom)
      var_bool = var_nom[indice]

      # Création des colonnes
      col1, col2 = st.columns(2)  # Crée deux colonnes de largeur égale

      # Affichage du premier graphique dans la première colonne
      with col1:
        fonctionsgraph.graphQuali_boxplot(df2023, var_bool)


      # Affichage du deuxième graphique dans la deuxième colonne
      with col2:
        fonctionsgraph.graphQuali_pointplot(df2023, var_bool)


      with st.expander(f"📌 Interprétation"):
        st.markdown(texte_justifie(
            "<ul>"
                "<li> <code>Stat_resp_rep</code> : il y environ 15% d'écart entre le temps moyen de réponse le plus long"
                " (<code>Stat_resp_rep = 0</code>) et le plus cours (<code>Stat_resp_rep = 1</code>)."
                " Il est d'ailleurs cohérent que le temps de réponse soit écourté lorsque le camion"
                " provient de la caserne responsable du secteur.</li>"
            "Le test ANOVA est significatif (p-value<5%)"
            "</ul>"
            )
            , unsafe_allow_html=True)
        fonctionsgraph.test_anova(df2023, 'Stat_resp_rep')
        st.markdown("<br>", unsafe_allow_html=True)


        st.markdown(texte_justifie(
            "<ul>"
                "<li> <code>Bor_resp_rep</code> : il y environ 14% d'écart entre le temps moyen de réponse le plus long "
                "le temps total moyen,  (<code>Bor_resp_rep = 0</code>) et le plus cours (<code>Bor_resp_rep = 1</code>).</li>"
                "Le test ANOVA est significatif (p-value<5%)"
            "</ul>"
            )
            , unsafe_allow_html=True)
        
        fonctionsgraph.test_anova(df2023, 'Bor_resp_rep')
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(texte_justifie(
            "<ul>"
                "<li> <code>Bor_inc_rep</code> : il y a environ 10% d'écart entre le temps moyen de réponse le plus long "
                "(<code>Bor_inc_rep = 0</code>) et le plus cours (<code>Bor_inc_rep = 1</code>).</li>"
                "Le test ANOVA est significatif (p-value<5%)"
            "</ul>"
            )
            , unsafe_allow_html=True)
        
        fonctionsgraph.test_anova(df2023, 'Bor_inc_rep')
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(texte_justifie(
            "<ul>"
                "<li> <code>Bor_inc_resp</code> : il y a moins de 5% d'écart entre le temps moyen de réponse le plus long (<code>Bor_inc_resp = 0</code>)"
                "et le plus cours (<code>Bor_inc_resp = 1</code>).</li>"
            "</ul>"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

      with tab4:
        df_2024 = recup_df("df_2024.csv")

        caserne = df_2024['IncidentStationGround'].unique()
        caserne = [c.lower() for c in caserne]
        caserne = sorted(caserne)

        st.subheader("Localisation des incidents sur cartes HTML")

        st.markdown(texte_justifie(
            "Dans cet onglet, vous pouvez visualiser les incidents 2023 sur une carte HTML. Les droites lient chaque lieu d'incident "
            "à la caserne de départ du camion de secours. Les lieux d'incident sont colorés en vert si le temps de réponse des pompiers est strictement inférieur "
            "à 6 minutes. Sinon, ils sont colorés en rouge.<br><br>"
            )
        , unsafe_allow_html=True)

        # Case à cocher pour le choix des incidents
        choix_incidents = st.radio(
          "Sélectionnez les incidents à afficher :",
          ["Tous les incidents", "Incidents avec temps supérieur à 6 min"]
        )

        # Sélection de la carte à afficher
        carte_choisie = st.selectbox("Choisissez un quartier :", caserne)

        if choix_incidents == "Tous les incidents":
          chemin_fichier = f"Donnees/Cartes/{carte_choisie}.html"
        else :
          chemin_fichier = f"Donnees/Cartes/{carte_choisie}1.html"

        # Lire et afficher la carte HTML choisie
        html_carte = lire_html(chemin_fichier)
        components.html(html_carte, height=600)  # Ajustez la hauteur selon vos besoins
