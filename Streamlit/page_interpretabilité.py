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
    # S'assurer que la colonne "Proportion" est bien de type float
    resultat["Proportion"] = resultat["Proportion"].astype(float)


    for var_name in liste:
        # Calculer la proportion par rapport au nombre total de nœuds (en pourcentage)
        if resultat.loc[var_name, "Nombre d'apparition"] > 0:
            resultat.loc[var_name, "Proportion"] = (resultat.loc[var_name, "Nombre d'apparition"] / n_nodes) * 100

    return resultat


def interpretabilite():
    st.title("Interprétation du modèle")

    st.markdown(texte_justifie(
        "Dans cette section, nous présentons l'interprétabilité (échelle globale) et l'explicabilité (échelle locale) du modèle final. "
        " L’interprétabilité consiste à expliquer le cheminement du modèle en répondant à la question : comment le modèle "
        "fait-il ses choix ? L’explicabilité, quant à elle, vise à expliquer pourquoi, avec ces données, le modèle a prédit "
        "ce résultat. Pour comprendre l'interprétabilité et l'explicabilité il faut dans un premier temps comprendre le "
        "modèle.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "L'algorithme de Gradient Boosting est une méthode de classification basée sur les arbres de décision. Cela signifie"
        " que le modèle construit une série de petits arbres, qui, une fois combinés, permettent d’améliorer la précision"
        " des prédictions.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Expander pour afficher/masquer le modèle de Gradient Boosting
    with st.expander("📌 Le modèle de gradient boosting"):
        st.markdown(texte_justifie(
            "Un modèle Gradient Boosting se compose d'un ensemble d'estimateurs (ou apprenants) \"faibles\" qui, une fois combinés, forment un estimateur \"fort\"."
            " A chaque étape, l'arbre est construit en corrigeant les erreurs de l'arbre précédent.")
            , unsafe_allow_html=True)

        st.image("Donnees/Images/illustration gradient boosting.png",
                  caption="Illustration du Gradient Boosting", use_container_width=True)

        st.markdown(r"""
            ##### Les étapes du **gradient boosting**

            - **Etape 1 :**  Initialisation

            Un première arbre est choisi en s'aidant de la proportion de la classe
            "positive" $p$

            - **Etape 2 :** Calcul des pseudos-résidus

            Pour chaque observation du dataset, l’erreur de classification est calculée en utilisant une fonction de perte.

            - **Etape 3 :**  Entraînement d'un nouvel arbre
            Un nouvel arbre est entraîné afin de minimiser les erreurs calculer précédemment.

            - **Etape 4 :** Mise à jour du modèle.

                Une fois l’arbre entraîné, le modèle global est mis à jour avec la formule suivante :


                $$F_{t+1}(x) = F_t(x) + \lambda h_t(x)$$


                Où :
                - $F_t(x)$ est la prédiction précédente et $F_{t+1}(x)$ la prédiction désirée.
                - $h_t(x)$ est l’arbre nouvellement ajouté (étape 3).
                - $\lambda$ est le taux d’apprentissage (learning rate), qui contrôle la vitesse d’ajustement.

                    
            - **Etape 5 :** Répétition.

            On répète les étapes 2 à 4 jusqu'à convergence du modèle ou jusqu'à atteindre le nombre maximal d'itérations (c'est un deshyper-paramètre du modèle).
            """, unsafe_allow_html=True)

    # Création des onglets
    tab1, tab2 = st.tabs(["Interprétabilité", "Explicabilité"])

    with tab1:
        st.subheader("Interprétabilité")
        st.markdown(texte_justifie(
            "L'interprétabilité du modèle peut être étudiée de deux manières :"
            "<ul>"
                "<li> Visualisation des arbres de décision</li>"
                "<li> Importance des variables explicatives</li>"
            "</ul>")
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        filename = 'Donnees/Modeles/gradient_boosting_model2v2.joblib'
        gb_model2 = joblib.load(filename)

        st.markdown("##### 👁️ Visualisation de l'arbre de prédiction")

        st.markdown(texte_justifie(
            "Notre modèle se compose de 400 arbres (<code>n_estimators = 400</code>). "
            "Chaque arbre a une profondeur maximale de 9 (<code>max_depth = 9</code>). "
            " Il n'est pas possible de représenter sur un même graphique la totalité du modèle puisqu'il s'agit d'une forêt. "
            "Ci-dessous, nous représentons chacun des arbres de décision. Nous limitons cette représentation aux trois premiers niveaux des arbres."
            )
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

        with st.expander(f"👁️ Visualisation de l'arbre de décision # {num_arbre}"):
            # Récupération du nom des colonnes
            afficher_arbre(gb_model2,col_names, arbre_index=num_arbre-1, max_depth=2)

        with st.expander(f"👁️ Proportion des variables utilisées dans l'arbre # {num_arbre}"):
            liste = st.multiselect("Sélectionnez vos variables d'intérêt :", col_names)
            st.write(count_var(gb_model2, col_names, liste, num_arbre-1))

        with st.expander(f"📌 Interprétation de l'arbre à l'initialisation"):
            afficher_arbre(gb_model2,col_names, arbre_index=0, max_depth=2)
            st.markdown(texte_justifie(
                "Dans cet arbre, la première séparation se fait sur la variable <code>Bor_resp_rep</code> qui est une variable"
                " binaire représentant si la caserne déployée (répondante) et la caserne responsable sont dans le même"
                " arrondissement (1 = oui, 0 = non). Au second niveau, les deux noeuds se séparent en branches supplémentaires"
                " selon la même variable : la distance standardisée (<code>distStd</code>). La borne est légèrement différente si la caserne"
                " répondante et la caserne déployée sont identiques (<code>distStd<=0.531</code> versus <code>distStd=0.484</code>"
                "). La distance a aussi beaucoup de poids sur le troisième niveau de l'arbre car elle intervient dans 3 tests "
                "sur 4."
                )
                , unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(texte_justifie(
                "Vous trouverez ci-dessous la proportion d'apparition de chaque variable dans l'arbre. "
                "Sur la totalité de l'arbre, la variable <code>distStd</code> apparaît 102 fois (soit dans 16,5% des nœuds de l'arbre) alors que "
                "<code>Bor_resp_rep</code> n'apparaît que lors du premier test."
                )
                , unsafe_allow_html=True)
            tab = count_var(gb_model2, col_names, col_names, 0)
            st.write(tab)



        with st.expander(f"📌 Interprétation de l'arbre à la dernière itération"):
            afficher_arbre(gb_model2,col_names, arbre_index=399, max_depth=2)
            st.markdown(texte_justifie(
                "Dans cet arbre, la première séparation se fait sur la variable <code>Borough_E09000010</code>, qui "
                "indique si l'incident a lieu ou non (1 = oui, 0 = non) dans l'arrondissement E09000010, soit Enfield. "
                "Au second niveau, si l'incident a lieu à Enfied, la séparation se fait sur la variable <code>Bor_inc_rep</code>, qui indique si l'incident "
                "a lieu dans le même arrondissement que la caserne de départ du camion. "
                "Si l'incident n'a pas lieu à Enfied, la séparation suivante est effectuée sur la variable <code>H1117</code>, qui indique si "
                "l'incident a eu lieu entre 11h et 17h. "
                "Au troisième niveau, les branches se divisent encore en fonction de plusieurs variables : des indicatrices d'arrondissement "
                "(<code>Borough_E09000007</code> et <code>Borough_E09000020</code>), la distance (<code>distStd</code>) et la variable binaire <code>PropCat_Boat</code>, "
                "qui indique si l'incident a lieu (ou non) sur un bateau."
                )
                , unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(texte_justifie(
                "Vous trouverez ci-dessous la proportion d'apparition de chaque variable dans l'arbre. "
                "Sur la totalité de l'arbre, la variable <code>distStd</code> apparaît 55 fois (soit dans 22,6% des nœuds de l'arbre) et "
                "<code>Bor_resp_rep</code> apparaît sept (2,9% des noeuds)."
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
            "Le tableau ci-dessous présente les variables avec une importance de plus de 1% d’après l’attribut de classe "
            "<code>features_importances_</code>."
            )
            , unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.dataframe(feat_imp_t.style.format("{:.2f}%"))

        with st.expander("📌 Interprétation"):
            st.markdown(texte_justifie(
                "Seules cinq variables ont une importance de plus de 1%. Elles représentent cependant plus de 90% du modèle.<br>"
                "Il s'agit de variables donnant des informations \"géographiques\""
                "<ul>"
                    "<li><code>Distance</code> représente la distance séparant le lieu de l'incident de la caserne de départ du camion de secours s'étant rendu sur l'incident. "
                    "L'importance de cette variable était prévisible car plus la distance augmente plus le temps de trajet augmente.</li>"
                    "<li><code>RatioSC</code> représente la superficie moyenne de l'arrondissement affectée à une caserne ; plus le ratio est élevé et plus la caserne"
                    " une grande superficie à gérer et donc plus le temps de réponse s'accroît.</li>"
                    "<li><code>Stat_resp_rep</code> indique si la caserne responsable du secteur de l'incident est identique à celle dont part le camion de secours (=caserne répondante).</li>"
                    "<li><code>Bor_resp_rep</code> indique si l'arrondissement de la caserne responsable et répondante sont identiques. </li>"
                    "<li>Enfin, <code>Bor_inc_rep</code> indique si l'arrondissement de l'incident et celui de la caserne répondante sont identiques.</li>"
                "</ul>"
                )
                , unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(texte_justifie(
            "Une autre manière d'étudier les variables explicatives importantes et de déterminer leur influence (positive ou négative) sur les prédictions est "
            "de visualiser les <b>shap-values</b>."
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
                    "<li> La distance standardisée (<code>distStd</code>) est la variable la plus importante. Si la distance est faible"
                    " (SHAP values négatives), la valeur prédite l'est aussi ce qui correspond à un temps de réponse inférieur"
                    " à 6 min. On constate aussi l'inverse. Il est cohérent qu'une distance plus longue implique un temps"
                    " de trajet plus long.</li>"
                    "<li>Graphiquement, les valeurs fortes de <code>Stat_resp_rep</code> sont associées à de faibles valeurs SHAP."
                    " Autrement dit, lorsque la caserne responsable est celle qui répond à l'incident (<code>Stat_resp_rep=1</code>), "
                    "il y a plus de chance que le temps de réponse soit inférieur à 6 minutes. Cette influence s'explique"
                    " car si la caserne déployée (répondante) n'est pas la caserne responsable, cela implique sûrement une "
                    "distance plus importante.</li>"
                    "<li>Les observations où <code>H1117=1</code> / <code>H26=1</code> sont associées à des valeurs SHAP élevées."
                    " Autrement dit, il y a plus de chance que le temps de réponse soit supérieur à 6 minutes si l'incident "
                    "a lieu sur les plages horaires [2 - 6] et [11 - 17]. Pour la plage horaire nocturne, cela s'explique par"
                    " une faible mobilisation (heures creuses, moins de pompiers présents en caserne). Pour l'autre plage,"
                    " on peut supposer que la densité importante du trafic routier augmente le temps de trajet.</li>"
                    "<li>Des valeurs fortes de <code>ratioStd</code> sont associées à des valeurs SHAP élevées. Pour rappel "
                    "<code>ratioStd</code> représente le ratio entre la superficie d'un arrondissement et son nombre"
                    " de casernes. Il y a donc plus de chance que le temps de réponse soit supérieur"
                    " à 6 minutes quand ce ratio est fort. On peut supposer que moins il y a de casernes au kilomètre"
                    " carré (ratio fort), plus la caserne a de distance à parcourir pour agir et donc plus le temps de trajet"
                    " est long.</li>"                    
                "</ul>"
                ), unsafe_allow_html=True)

        with st.expander("⚠️ Différences entre features_importances et shape_values "):
            st.markdown("""
            | Méthode | Comment est-ce calculé ? | Points forts | Limites |
            |---------|-------------------------|--------------|-------------|
            | **feature_importances_** | Basé sur la **réduction de de la pseudo-erreur** dans les arbres de décision. Plus une variable explicative réduit l'erreur en séparant les données, plus elle est importante. | Rapide à calculer, facile à interpréter. | Biaisé : favorise les variables explicatives avec plus de valeurs uniques (ex. variables quantitatives vs. catégorielles). |
            | **SHAP values**  | Basé sur la **théorie des jeux** : une contribution individuelle est attribuée à chaque variable explicative en tenant compte de toutes les combinaisons possibles de variables. | Plus fiable, prend en compte les interactions entre variables explicatives. | Plus lent à calculer, nécessite plus de ressources. |
            """)

    with tab2:
        st.subheader("Explicabilité")

        st.markdown(texte_justifie(
            "L'explicabilité permet de comprendre comment, pour une observation, le modèle a calculé sa prédiction. Cela indique les variables qui ont"
            "le plus influencé la prédiction.<br>"
            "Pour illustrer l'explicabilité, nous avons choisi quatre incidents dans le dataset test, deux de chaque catégorie, ayant une prédiction identique ou non à l’observation." 
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
                    " ne soit pas la caserne responsable influence la prédiction vers la valeur positive (<code>ResponseTimeBinary</code> prédit à 1).</li>"
                    "<li><b>Incident n°0 :</b> observation = temps d'intervention supérieur à 6 minutes, prédiction incorrecte.<br>"
                    "Les variables <code>distStd=-0.1353</code>, <code>Stat_resp_rep=1</code>, <code>H26=0</code> et <code>H1117=0</code>"
                    " ont une contribution négative suffisante pour que la prédiction soit négative (temps d'intervention inférieur à"
                    " 6 minutes) alors que la valeur observée est positive.</li>"
                    "<li><b>Incident n°2 :</b> observation = prédiction = temps d'intervention inférieur à 6 minutes.<br>"
                    "La contribution négative des variables <code>distStd=-0.01524</code> et <code>H1117=0</code> est suffisante"
                    " pour contrebalancer la contribution positive des variables <code>H26=1</code>, <code>Stat_resp_rep=0</code>"
                    " et <code>Borough_E09000028=1</code>.</li>"
                    "<li><b>Incident n°15 :</b> observation = temps d'intervention inférieur à 6 minutes, prédiction incorrecte.<br>"
                    "La contribution négative de la variable <code>H1117=0</code> n'est pas suffisante pour contrebalancer la contribution"
                    " positive des variables <code>distStd=0.6656</code>, <code>Stat_resp_rep=0</code>, <code>Bor_inc_rep=0</code>,"
                    " <code>Bor_resp_rep=0</code>.</li>"
                "</ul>"
                ), unsafe_allow_html=True)
