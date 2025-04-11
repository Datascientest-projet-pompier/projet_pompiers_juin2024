import streamlit as st

from fonctions import texte_justifie

def conclusion():
    st.title("Conclusion")

    st.markdown("##### Difficultés")
    st.markdown(texte_justifie(
        "<ul>"
            "<li> Communication avec le métier.<br>"
            "Même si nous avons pû échanger avec Sophie Prendergast, Business Intelligence Analyst, la communication "
            "avec le domaine métier est restée insuffisante ce qui a engendré des problème de compréhension sur l'enregistrement "
            "des variables et sur leur signification précise.</li>"
            "<li> Gestion du temps disponible.<br>"
            "La gestion du temps a été un défi permanent entre nos métiers respectifs, l'apprentissage théorique via les"
            "cours dispensés sur la plateforme de DataScienTest et le projet.</li>"
        "</ul>")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("##### Perspectives")
    st.markdown(texte_justifie(
        "Notre modèle n’est pas suffisamment performant pour être utilisé par la Brigade"
        " des Pompiers de Londres car il y a trop de cas (13,4% des incidents du jeu test) où il prédit, à tort, un temps"
        " de réponse inférieur à 6 minutes. Il y a plusieurs pistes d’amélioration possibles.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "<ul>"
            "<li> <b>Collaboration avec le métier</b>.<br>"
            "Nous avons déjà souligné dans la section précédente l’importance de la collaboration entre"
            " les data scientists et le métier. Nous sommes persuadés qu’une meilleure appréhension des étapes"
            " opérationnelles entre le déclenchement des secours et leur arrivée sur le lieu de l’incident "
            " nous permettrait de mieux comprendre les variables que nous avions à disposition mais aussi d’appréhender"
            " celles qui pourraient manquer dans notre modélisation.</li>"
            "<li> <b>Valeurs manquantes, extrêmes et aberrantes</b>.<br>"
            "Une meilleure compréhension des données et des conditions de leur enregistrement nous permettrait de distinguer"
            " plus facilement les valeurs aberrantes des valeurs extrêmes (faibles ou fortes). Par exemple, nous avons "
            "découvert que le temps de réponse était borné à 20 minutes maximum. Tout incident avec un temps de réponse"
            " supérieur est supprimé de la base de données avant sa publication. Il y a sans doute d’autres cas qui sont "
            "aberrants et qui sont pourtant enregistrés.<br>"
            "Nous avons ainsi identifié 820 incidents ayant un temps de réponse inférieur à 5 secondes et dont on connait "
            "pourtant la localisation exacte (pas d'imputation sur la latitude / longitude). Certains d’entre eux contiennent certainement des données inexactes, "
            "surtout si on considère que les pompiers auraient parcouru en moyenne 1,23 km en 5 secondes (soit une vitesse de plus de "
            "800 km/h) !<br>"
            "Nous n’avons pas identifié ce type de données lors du preprocessing. Leur suppression aurait très probablement "
            "amélioré les qualités prédictives du modèle.<br>"
            "Dans notre expérience métier, la variable cible est une donnée dont notre entreprise est propriétaire. "
            "Si nous avions accès à la base de données de la Brigade des Pompiers de Londres, et non uniquement à celle "
            "qui est publique, il y aurait sans doute d’autres informations nous permettant le traitement des données "
            "aberrantes. De plus, nous n’aurions peut-être pas eu à approximer 51,2% des coordonnées géographiques car "
            "nous aurions pu avoir accès à des données non (ou moins) anonymisées.</li>"
            "<li><b>Analyse des liens entre les variables géographiques</b>.<br>"
            "Comme déjà discuté plusieurs fois, nous avions à disposition de nombreuses variables liées à la localisation "
            "de l’incident et des secours associés. Nous avons fait le choix d’inclure "
            "uniquement l’arrondissement (<code>Borough</code>) sans inclure la caserne répondante. "
            "Ce choix se justifie à la fois pour une question « pratique » − il y a 102 casernes, "
            "les inclure augmente considérablement le temps d’exécution − et méthodologique − arrondissement et caserne "
            "contiennent au moins en partie le même type d’information. Nous avons pris en compte ces liens via les "
            "variables binaires <code>Bor_resp_rep</code>, <code>Bor_inc_rep</code>, <code>Bor_inc_resp</code> et "
            "<code>Stat_resp_rep</code> mais nous ne sommes pas convaincus qu’il s’agisse de la méthode optimale.<br>"
            "Une meilleure connaissance de la géographie de Londres et de l’organisation de la Brigade des Pompiers de "
            "cette ville permettrait sans doute un choix plus adapté et une meilleure combinaison des informations à "
            "notre disposition.</li>"
            "<li><b>Amélioration du calcul de la distance</b>.<br>"
            "Nous avons calculé la distance minimale entre le lieu de l’incident et la caserne répondante (autrement dit "
            "la distance à vol d’oiseau). Il existe des librairies python (OSMnx et Networkx) permettant de calculer la "
            "distance la plus courte en s’appuyant sur les données d’OpenStreetMap, une base de données qui représente "
            "notamment les réseaux routiers de Londres. Nous n’avons pas eu le temps d’explorer cette alternative. Sans "
            "surprise (c’est une hypothèse de « bon sens »), la distance est très importante dans la prédiction du temps "
            "de réponse. Toute amélioration de sa précision implique une amélioration de la qualité prédictive du modèle.</li>"
            "<li><b>Ajout de nouvelles variables explicatives</b>.<br>"
            "Même sans échange avec le métier, nous pensons que d’autres variables pourraient avoir un poids important "
            "dans la prédiction du temps de réponse de la Brigade des Pompiers de Londres et n’ont pas été inclus dans "
            "notre modèle :"
            "<ul>"
                "<li>Trafic routier en temps réel. Cette information fait d’ailleurs partie des raisons de retard "
                "consignées dans la variable <code>DelayCodeId</code>. C’est une conclusion de « bon sens ». Un fort trafic ralentira "
                "les Pompiers. Il pourra aussi influencer leur choix d’itinéraire (et donc la distance) pour parvenir sur "
                "les lieux de l’incident.</li>"
                "<li>Conditions météorologiques. A nouveau, il apparaît raisonnable de supposer que la conduite d’un pompier "
                "(et sa vitesse) sera différente sur une route verglacée ou sous la grêle que sous un soleil estival. Pour "
                "rappel, nous avons étudié la saisonnalité mais n’avons pas observé d’influence à ce niveau de détails.</li>"
                "<li>Disponibilité des ressources. La caserne répondante n’est pas toujours celle responsable du secteur où "
                "a lieu l’incident. Cette information est prise en compte dans notre modèle où elle est d’ailleurs la "
                "deuxième plus importante (après la distance). Connaître les disponibilités en temps réel de chaque caserne "
                "(que ce soit en termes de véhicules ou de personnel) permettrait sans doute d’améliorer la prédiction du "
                "modèle.</li></li>"
            "</ul>"
            "<li><b>Modèles de survie et réseau de neurones</b>.<br>"
            "La dernière piste d’amélioration concerne le type de modélisation que nous aurions pu tester. Deux familles "
            "de modèles pourraient être explorées :"
            "<ul>"
                "<li>Les modèles de survie. Initialement, ces modèles ont été développés pour étudier l’espérance de vie "
                "des organismes. Cela consiste à estimer la probabilité d’être encore en vie à un temps T. Cela pourrait "
                "être appliqué à notre base de données, la probabilité d’arrivée sur les lieux de l’incident remplaçant "
                "la probabilité de survie.</li>"
                "<li>Les réseaux de neurones.</li></li>"
            "</ul>"
        "</ul>")
        , unsafe_allow_html=True)
