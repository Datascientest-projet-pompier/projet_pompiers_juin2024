import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree


from fonctions import texte_justifie

# Fonction pour afficher un arbre spécifique
def afficher_arbre(gb_model, col_names, arbre_index=0, max_depth=2):
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(gb_model.estimators_[arbre_index, 0],  # Sélectionner l'arbre
              filled=True,
              feature_names=col_names,
              max_depth=max_depth,
              ax=ax)  # Utiliser l'axe pour Streamlit
    st.pyplot(fig)  # Afficher avec Streamlit


def count_var(gb_model, col_names, liste, arbre_index):
    # Récupérer l'arbre de décision
    tree = gb_model.estimators_[arbre_index, 0].tree_

    # Nombre de nœuds dans l'arbre
    n_nodes = tree.node_count

    # Initialisation du DataFrame avec des zéros pour le nombre d'apparitions
    resultat = pd.DataFrame(0, index=liste, columns=["Nombre d'apparition", "Proportion"])

    # Parcours des nœuds de l'arbre
    for i in range(n_nodes):
        feature_index = tree.feature[i]

        # Vérifier si le nœud utilise une caractéristique (non-feuille)
        if feature_index != -2:  # -2 signifie une feuille, pas une caractéristique
            feature_name = col_names[feature_index]

            # Si le nom de la variable est dans la liste, incrémenter son compteur
            if feature_name in liste:
                resultat.loc[feature_name, "Nombre d'apparition"] += 1

    # Calcul des proportions
    for var_name in liste:
        # Calculer la proportion par rapport au nombre total de nœuds (en pourcentage)
        if resultat.loc[var_name, "Nombre d'apparition"] > 0:
            resultat.loc[var_name, "Proportion"] = (resultat.loc[var_name, "Nombre d'apparition"] / n_nodes) * 100

    return resultat


def interpretabilite():
    st.title("Interpretabilité du modèle")

    st.markdown(texte_justifie(
        "Dans cette partie, nous présenterons l’interprétabilité (globale) et l’explicabilité (locale) du modèle."
        " L’interprétabilité consiste à expliquer le cheminement du modèle en répondant à la question : comment le modèle "
        "fait-il ses choix ? L’explicabilité, quant à elle, vise à expliquer pourquoi, avec ces données, le modèle a prédit "
        "ce résultat. Pour comprendre l'interprétabilité et l'explicabilité il faut dans un premier temps comprendre le "
        "modèle.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Le modèle utilise le gradient boosting, une méthode basée sur les arbres de décision. Cela signifie"
        " que le modèle construit une série de petits arbres, qui, une fois combinés, permettent d’améliorer la précision"
        " des prédictions.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Expander pour afficher/masquer le modèle de Gradient Boosting
    with st.expander("📌 Le modèle de gradient boosting"):
        st.markdown(texte_justifie(
            "Le Gradient Boosting est une technique d'apprentissage supervisé que l'on utilise ici pour "
            "la classification binaire. Il construit des modèles successifs en corrigeant les erreurs du modèle précédent.")
            , unsafe_allow_html=True)

        st.image("Donnees/Images/illustration gradient boosting.png",
                  caption="Illustration du Gradient Boosting", use_container_width=True)

        st.markdown(r"""
            ##### Les étapes du **gradient boosting**

            - **Etape 1 :** 🚀 Initialisation.

            Le modèle effectue une première prévision pour chaque individus, est s'aidant de la proportion de la classe
            "positive $p$

            - **Etape 2 :** ❌ Calcul des pseudos-résidus.

            Pour chaque individu, on évalue l’erreur de classification en utilisant une fonction de perte.

            - **Etape 3 :** 🚀 Entrainement d'un nouvelle arbre.
            Un nouvelle arbre est entrainé pour minimiser les erreurs calculer précédemment.

            - **Etape 4 :** Mise à jour du modèle.

                Une fois l’arbre entraîné, on met à jour le modèle global avec la formule suivante :


                $$F_{t+1}(x) = F_t(x) + \lambda h_t(x)$$

                    
                Où :
                - $F_t(x)$ est la prédiction précédente et $F_{t+1}(x)$ la prédiction désirée.
                - $h_t(x)$ est l’arbre nouvellement ajouté (étape 3).
                - $\lambda$ est le taux d’apprentissage (learning rate), qui contrôle la vitesse d’ajustement.

            - **Etape 5 :** 🔁 Répétition.

            On répète les étapes 2 à 4 jusqu'à convergence du modèle ou jusqu'à atteindre le nombre maximal d'itérations.
            """, unsafe_allow_html=True)

        st.markdown("""
            ##### Les hyperparamètres utilisés
            Les hyperparamètres ont été déterminé à l'aide d'un jeu de données réduit. Voici les valeurs trouvées et leurs
            explications
            """, unsafe_allow_html=True)

        st.code("""
            # Nombre d'arbres dans l'ensemble (forêt aléatoire)
            n_estimators = 400
            # Taux d'apprentissage, contrôle la contribution de chaque arbre
            learning_rate = 0.0464
            # Fraction des données utilisées pour chaque arbre (87.5% dans ce cas)
            subsample = 0.875
            # Fraction minimale d'échantillons requise pour diviser un nœud interne
            min_samples_split = 0.0005
            # Profondeur maximale de chaque arbre (9 niveaux dans ce cas)
            max_depth = 9
            # Nombre maximal de caractéristiques considérées pour chaque division
            max_features = 25
            """, language="python")

    # Création des onglets
    tab1, tab2 = st.tabs(["Interprétabilité", "Explicabilité"])

    with tab1:
        st.subheader("Interprétabilité")
        st.markdown(texte_justifie(
            "L'interprétabilité du modèle peu être vue de deux manières :"
            "<ul>"
                "<li> Visualisation des arbres de décisions.</li>"
                "<li> Importances des variables.</li>"
            "</ul>")
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        filename = 'Donnees/Modeles/gradient_boosting_model2v2.joblib'
        gb_model2 = joblib.load(filename)

        st.markdown("##### 👁️ Visualisation de l'arbre de prédiction")

        st.markdown(texte_justifie(
            "Pour notre modèle la profondeur il y a eu 400 itérations maximums (<code>n_estimators = 400</code>) à chaque itération "
            "un arbre de prédiction est construit pour minimiser l'erreur précédente. Chaque arbre à une profondeur maximale de"
            " 9 (<code>max_depth = 9</code>).<br>"
            " Il nous est donc impossible de représenter chaque arbre n'y d'en représenter la totalité.")
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Récupération des noms de colonne
        df = pd.read_csv("Donnees/Doc csv/list_col.csv")
        col_names = df.columns.tolist()

        # Choix de l'arbre affiché
        num_arbre = st.number_input("Itération de l'algorithme",
                                            min_value=0,
                                            max_value=gb_model2.estimators_.shape[0],
                                            value=1,
                                            step=1)

        with st.expander(f"👁️ Visualisation de l'arbre de prédication itération : {num_arbre}"):
            # Récupération du nom des colonnes
            afficher_arbre(gb_model2,col_names, arbre_index=num_arbre-1, max_depth=2)

        with st.expander(f"👁️ Utilisation de la variable dans l'arbre d'itération : {num_arbre}"):
            liste = st.multiselect("Vos variables d'intéret :", col_names)
            st.write(count_var(gb_model2, col_names, liste, num_arbre-1))

        with st.expander(f"📌 Interprétation arbre à l'initialisation"):
            afficher_arbre(gb_model2,col_names, arbre_index=0, max_depth=2)
            st.markdown(texte_justifie(
                "Dans cet arbre, la première séparation se fait sur la variable <code>Bor_resp_rep</code> qui est une variable"
                " binaire représentant si la caserne déployée (répondante) et la caserne responsable sont dans le même"
                " arrondissement (1 = oui, 0 = non). Au second niveau, les deux noeuds se séparent en branches supplémentaires"
                " selon la même variable : la distance standardisée (distStd). La borne est légèrement différente si la caserne"
                " répondante et la caserne déployée sont identiques (<code>distStd<=0.531</code> versus <code>distStd=0.484</code>"
                "). La distance a aussi beaucoup de poids sur le troisième niveau de l'arbre car elle intervient dans 3 tests "
                "sur 4."
                )
                , unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(texte_justifie(
                "Vous trouverez ci-dessous la proportion d'apparition de chaque variables."
                )
                , unsafe_allow_html=True)
            tab = count_var(gb_model2, col_names, col_names, 0)
            st.write(tab)



        with st.expander(f"📌 Interprétation arbre à la dernière itération"):
            afficher_arbre(gb_model2,col_names, arbre_index=399, max_depth=2)
            st.markdown(texte_justifie(
                "Dans cet arbre, la première séparation se fait sur la variable <code>Borough_E09000010</code>, qui est"
                " une variable binaire indiquant si l'observation appartient à un certain arrondissement (1 = oui, 0 = non)."
                " Cette séparation divise les données en deux sous-ensembles principaux.<br>"
                "Au second niveau, si l'observation appartient à l'arrondissement correspondant à <code>Borough_E09000010</code>"
                ", une nouvelle séparation est effectuée sur la variable <code>H1117</code>, qui est également binaire et indique si "
                "l'incident à eu lieu entre 11h et 17h. En revanche, si l'observation ne correspond pas à cet arrondissement,"
                " la séparation se fait sur la variable <code>Bor_inc_rep</code>, qui indique si l'incident a été signalé"
                " dans le même arrondissement que la caserne qui à répondue.<br>"
                "Au troisième niveau, les branches se divisent encore en fonction de plusieurs variables :"
                "<ul>"
                    "<li>Dans le sous-arbre gauche, la séparation est faite sur <code>Borough_E09000007</code> et "
                    "<code>Borough_E09000020</code></li>"
                    "<li>Dans le sous-arbre droit, deux variables interviennent : <code>distStd</code>, qui correspond"
                    " à une mesure de distance normalisée, et <code>PropCat_Boat</code>, qui est une variable catégorique "
                    "liée aux propriétés."
                )
                , unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(texte_justifie(
                "Vous trouverez ci-dessous la proportion d'apparition de chaque variables."
                )
                , unsafe_allow_html=True)
            tab = count_var(gb_model2, col_names, col_names, 399)
            st.write(tab)



        st.markdown("##### 👁️ Visualisation de l'importance des variables")

        # Calcul de l'importance des features en pourcentage
        feat_imp = pd.DataFrame({'importance': gb_model2.feature_importances_ * 100}, index=gb_model2.feature_names_in_)

        # Filtrer pour ne garder que les features avec importance > 1%
        feat_imp = feat_imp[feat_imp['importance'] > 1].sort_values(by='importance', ascending=False)

        # Transposer le tableau pour le rendre horizontal
        feat_imp_t = feat_imp.T  # Transformation du tableau

        st.markdown(texte_justifie(
            "Une autre manière d'interpréter le modèle est de voir l'importance des variables est d'utiliser l'attribut de classe "
            "<code>g_model2.features_importances_</code>."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.dataframe(feat_imp_t.style.format("{:.2f}%"))

        with st.expander("📌 Interprétation"):
            st.markdown(texte_justifie(
                "Seuls cinq variables ont une importance de plus de 1%, à elles cinqs elles représentent plus de 90% du modèle.<br>"
                "Elles sont composées de deux variables donnant des informations \"géographique\" et des informations carractérisant"
                " les relations \" Borough Caserne Déployée - Borough Caserne Responsable - Borough Incident\" "
                "<ul>"
                    "<li><code>Distance</code> représentant la distance séparant le lieu de l'incident et la caserne qui c'est déplacée. "
                    "L'importance de cette variable était prévisible car plus la distance augmente plus le temps de trajet augmente.</li>"
                    "<li><code>RatioSC</code> représentant la superficie affectée à une caserne, plus le ratio est élevé et plus la caserne"
                    " à beaucoup de chose à gérer.</li>"
                    "<li><code>Stat_resp_rep</code>, <code>Bor_resp_rep</code> et <code>Bor_resp_rep</code> représentant des indicateurs (OUI/NON) "
                    "sur la correspondance entre Station_répondante et Station_responsable pour le premier, entre Borough_répondante et "
                    "Borough_responsable pour le second et entre Borough_incident et Borough_répondante pour le dernier.</li>"
                "</ul>"
                )
                , unsafe_allow_html=True)

        st.markdown(texte_justifie(
            "Une autre manière de trouver les variables importantes et de déterminer leur influence (positive ou négative) est "
            "de visualiser les shap-values."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Charger l'image
        image = Image.open("Donnees/Images/shap_values.png")

        # Redimensionner l'image (ex: 50% de la taille originale)
        new_size = (int(image.width *0.6), int(image.height *0.6))
        image_resized = image.resize(new_size)

        # Afficher l'image redimensionnée
        st.image(image_resized, use_container_width=False)

        with st.expander("📌 Interprétation"):
            st.markdown(texte_justifie(
                "<ul>"
                    "<li> La distance standardisée distStd est la variable la plus importante. Si la distance est faible"
                    " (SHAP values négatives), la valeur prédite l'est aussi ce qui correspond à temps d'intervention inférieur"
                    " à 6 min. On constate aussi l'inverse. Il est cohérent qu'une distance plus longue implique un temps"
                    " de trajet plus long.</li>"
                    "<li>Graphiquement, les valeurs fortes de Stat_resp_rep sont associées à de faibles valeurs SHAP."
                    " Autrement dit, lorsque la caserne responsable est celle qui répond à l'incident (Stat_resp_rep=1), "
                    "il y a plus de chance que le temps d'intervention soit inférieur à 6 minutes. Cette influence s'explique"
                    " car si la caserne déployée (répondante) n'est pas la caserne responsable cela implique sûrement une "
                    "distance plus importante.</li>"
                    "<li>Les observations où <code>H1117=1</code> / <code>H26=1</code> sont associées à des valeurs SHAP élevées."
                    " Autrement dit, il y a plus de chance que le temps d'intervention soit supérieur à 6 minutes si l'incident "
                    "a lieu sur les plages horaires [2 - 6] et [11 - 17]. Pour la plage horaire nocturne, cela s'explique par"
                    " une faible mobilisation (heures creuses, moins de pompiers présents en caserne). Pour l'autre plage,"
                    " on peut supposer que la densité importante du trafic routier augmente le temps de trajet.</li>"
                    "<li>Des valeurs fortes de <code>ratioStd</code> sont associées à des valeurs SHAP élevées. Pour rappel "
                    "<code>ratioStd</code> représente le ratio entre la superficie d'un arrondissement par rapport au nombre"
                    " de casernes dans celui-ci. Il y a donc plus de chance que le temps d'intervention soit supérieur"
                    " à 6 minutes quand cette densité est forte. On peut supposer que moins il y a de casernes au kilometre"
                    " carré (ratio fort), plus la caserne a de distance à parcourir pour agir et donc plus le temps de trajet"
                    " est long.</li>"
                    "<li>Les variables <code>PropCat_Outdoor</code>, <code>PropCat_Other</code> Residential et <code>PropCat_Dwelling"
                    "</code> - qui précisent le type de localisation de l'incident - influencent la prédiction du modèle de façon"
                    " positive pour la première et négative pour les deux autres. Autrement dit, si un incident a lieu en extérieur"
                    " (<code>PropCat_Outdoor=1</code>, forte valeur), il y a plus de chance que le temps de trajet soit supérieur"
                    " à 6 minutes ; c'est l'inverse si l'incident a lieu chez un particulier (Dwelling) ou dans un autre type de"
                    " résidence (temps de trajet de moins de 6 minutes plus probable).</li>"
                "</ul>"
                ), unsafe_allow_html=True)

        with st.expander("⚠️ Différences entre features_importances et shape_values "):
            st.markdown("""
            | Méthode | Comment c'est calculé ? | Points forts | Limitations |
            |---------|-------------------------|--------------|-------------|
            | **feature_importances_** | Basé sur la **réduction de de la pseudo-erreur** dans les arbres de décision. Plus une feature réduit l'erreur en séparant les données, plus elle est importante. | Rapide à calculer, facile à interpréter. | Biaisé : favorise les features avec plus de valeurs uniques (ex. variables numériques vs. catégoriques). |
            | **SHAP values**  | Basé sur la **théorie des jeux** : il attribue une contribution individuelle à chaque feature en tenant compte de toutes les combinaisons possibles de features. | Plus fiable, prend en compte les interactions entre features. | Plus lent à calculer, nécessite plus de ressources. |
            """)

    with tab2:
        st.subheader("Explicabilité")

        st.markdown(texte_justifie(
            "L'explicabilité permet de comprendre comment le modèle, à fait sa prédiction. Quelles ont été les variables qui ont"
            "permis la prédiction.<br>"
            "Pour illustrer l'explicabilité nous avons choisis incidents donc la prédiction est 1 (supérieur à 6 min), le premier "
            "incident à un temps total d'intervention supérieur à 6 min (prédiction correcte) et le second un temps total d'intervention"
            "inférieur à 6 min (prédiction incorrecte). Deux autre incidents ont étés choisis de tel sorte que la prédiction est"
            " 0 (inférieur à 6 min), e premier incident à un temps total d'intervention inférieur à 6 min (prédiction correcte) et"
            " le second un temps total d'intervention supérieur à 6 min (prédiction incorrecte)"
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.image("Donnees/Images/explicabilite.png",
                  caption="Explicabilité de quatre réponses", use_container_width=True)

        with st.expander("📌 Interprétation"):
            st.markdown(texte_justifie(
                "<ul>"
                    "<li><b>Incident n°1 :</b> observation = prédiction = temps d'intervention supérieur à 6 minutes.<br>"
                    "La variable <code>H1117=0</code> est la principale variable avec une contribution négative au modèle"
                    " alors que <code>distStd=1.244</code>, <code>H26=1</code>, <code>Stat_resp_rep=0</code> et <code>Borough_E09000028=1</code>"
                    " sont les principales avec une contribution positive. Ces observations sont cohérentes avec nos conclusions de "
                    "l'interprétabilité global : le fait que l'incident ait eu lieu sur la plage horaire nocturne [2-6] et que la caserne déployée"
                    " ne soit pas la caserne responsable influence la prédiction vers la valeur positive (ResponseTimeBinary prédit à 1).</li>"
                    "<li><b>Incident n°0 :</b> observation : temps d'intervention supérieur à 6 minutes, prédiction incorrecte.<br>"
                    "Les variables <code>distStd=-0.1353</code>, <code>Stat_resp_rep=1</code>, <code>H26=0</code> et <code>H1117=0</code>"
                    " ont une contribution négative suffisante pour que la prédiction soit négative (temps d'intervention inférieur à"
                    " 6 minutes) alors que la valeur observée est positive.</li>"
                    "<li><b>Incident n°2 :</b> observation = prédiction = temps d'intervention inférieur à 6 minutes.<br>"
                    "La contribution négative des variables <code>distStd=-0.01524</code> et <code>H1117=0</code> est suffisante"
                    " pour contrebalancer la contribution positive des variables <code>H26=1</code>, <code>Stat_resp_rep=0</code>"
                    " et <code>Borough_E09000028=1</code>.</li>"
                    "<li><b>Incident n°15 :</b> observation : temps d'intervention inférieur à 6 minutes, prédiction incorrecte.<br>"
                    "La contribution négative de la variable <code>H1117=0</code> n'est pas suffisante pour contrebalancer la contribution"
                    " positive des variables <code>distStd=0.6656</code>, <code>Stat_resp_rep=0</code>, <code>Bor_inc_rep=0</code>,"
                    " <code>Bor_resp_rep=0</code>.</li>"
                "</ul>"
                ), unsafe_allow_html=True)
