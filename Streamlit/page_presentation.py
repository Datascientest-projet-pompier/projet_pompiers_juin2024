import streamlit as st
from fonctions import texte_justifie

def presentation():
    st.title("Présentation des données")
    st.markdown(texte_justifie(
    "L'ensemble des données est divisé en deux sous-dossiers. Le premier sous-dossier permet d'obtenir "
    "les informations relatives aux incidents "
    "(disponible <a href=\"https://data.london.gov.uk/dataset/london-fire-brigade-incident-records\">ICI</a>). "
    "Le second sous-dossier permet d'obtenir les informations relatives à la mobilisation des casernes (disponible "
    "<a href=\"https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records\">ICI</a>). "
  ), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Etude des données initiales")

    st.markdown(texte_justifie(
        "Que ce soit pour les données <b>Incident</b> ou les données <b>Mobilisation</b> les jeux de données possèdent une"
        " variable <b>IncidentNumber</b> qui permettra de faire la jointure entre les deux tableaux")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "L'ensemble des données de tous types et de tous ordres, on peut les regrouper en quatre catégories :"
        "<ul><li><b>données temporelles :</b> qui permettent de situer dans le temps l'incident (année, date et heure).</li>"
        "<li><b>données géographique :</b> qui permettent de situer l'incident géographiquement (latitude, longitude, "
        "code postal ...)</li>"
        "<li><b>données relatives à l'incident :</b> qui permettent de caractériser l'incident (caserne responsable/déployée,"
        " type d'incident, nombre de camion, coût ...)</li>"
        "<li><b>données cibes :</b> qui représentent les temps de réaction, de trajet et total</li></ul>")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Gestion des valeurs manquantes")

    st.markdown("#### Sur les fichiers incidents")
    
    st.markdown(texte_justifie(
        "Les données manquantes apparaissent sur :"
        "<ul><li><b>les données géographiques exactes :</b> principalement pour garantir l'anonymat. "
        "Les données géographiques approchées sont toujours présentes (données BNG) </li>"
        "<li><b>la variable <code>SpecialServiceType</code> :</b> qui n'est renseignée que si la variable "
        "<code>StopCodeDescription</code> a pour valeur \"Spécial Service\"</li>"
        "<li><b>les informations</b> (temps de présence et nom) <b>sur le premier (ou deuxième) camion arrivé sur site</b>"
        " ses informations sont pour nous connues a postério donc sans importance.</li></ul>")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### Sur les fichiers mobilisations")

    st.markdown(texte_justifie(
        "Les données manquantes apparaissent sur :"
        "<ul><li><b>Heures de retour :</b> qui ne sont plus renseignées.</li>"
        "<li><b>Raison du retard :</b> qui n'est renseignée que dans 25% des cas.</li>"
        "<li> <b>Date et heure de départ sur certains incidents :</b> cette information est crucial "
        "pour notre modèle, nous avons donc supprimé les lignes correspondantes (supression de moins de 1.5% des lignes)"
        "</li></ul>")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Nétoyage et jointure")

    st.markdown(texte_justifie(
        "Le 9 janvier 2014 les autorités londoniennes ont fermés 10 casernes. Nous avons donc choisis de ne"
        " conserver que les événements passés après cette date.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        " ??? p 7 ")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(texte_justifie(
        "Nous avons aussi remarqué des incohérences entre certaines variables, certaines étaient temporelles "
        "(heure d'arrivée < heure de départ) d'autre d'ordre technique (caserne des camions affectés différentes dans "
        "incidents et mobilisation)... Si la ligne correspondante à un incident contenait une incohérence elle à été supprimée.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(texte_justifie(
        "Pour notre étude nous avons eu besoin de joindre les fichiers incidents et mobilisations."
        " La jointure à été effectuée sur <b>IncidentNumber</b> qui est le numéro unique décrivant l'incident."
        " De plus certains incidents n'étaient présents que dans un des deux fichiers, ils ont été supprimés,"
        " car ne représentent que des événements à la marge (7,7% des données incidents et 0.4% des données"
        " mobilisations). De plus nous n'avons conservée que les informations relatives au premier camion arrivé"
        "sur place.")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(texte_justifie(
        "Après nettoyage, le dataframe joint contient des données sur 1 037 713 incidents gérés par la Brigade"
        " des Pompiers de Londres sur une période de plus de 10 ans (10 Janvier 2014 au 30 Septembre 2024).")
        , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    


    st.markdown("### Création des nouvelles variables")
    st.markdown(texte_justifie(
        "Pour simplifier notre jeu de données nous avons chercher à diminuer le nombre de variables en en regroupant certaines, "
        " elles correspondent uniquement aux deux dernières catégories."
        "<br>"
        "<ul>"
          "<li><b>données relatives à l'incident :</b>"
          
          "<ul>"
          "<li>Type d'incidents :"
          
            "<ul>"
              "<li><code>DetailedIncidentGroup</code> : qui correspond à une simplification de la description de l'incident. "
              "Elle rassemble les variables <code>StopCodeDescription</code> et <code>SpecialServiceType</code>, c'est une variable"
              " catégorielle contenant 9 modalités.</li>"
              "<li><code>Fire</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident est de"
              " type feu ou autre.</li>"
            "</ul></li>"

          "<li>Types de lieu affecté :"
          
            "<ul>"
              "<li><code>HighPropertyType</code> : qui représente une simplification de la variable <code>PropertyType</code>. "
              "Elle permet de passer d'une variable catégorielle à 293 modalités à une variable à 47 modalités</li>"
              "<li><code>GoodLocation</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident"
              " a été correctement localisé</li>"
            "</ul></li>"

          "<li> Données temporelles :"
            "<ul>"
              "<li><code>DayOfWeek</code> : représentant le jour de la semaine de l'incident.</li>"
              "<li><code>Month</code> : représentant le mois de l'incident.</li>"              
            "</ul></li>"

          "<li> Données géographiques :"
            "<ul>"
              "<li><code>Borough</code> : donnant l'arrondissement de la caserne</li>"
              "<li><code>RatioSC</code> : représentant la superficie affectée a une caserne (distinction par arrondissement)</li>"
              "<li><code>Distance</code> : représentant la distance à vol d'oiseau entre la caserne et l'incident</li>"
            "</ul></li>"

          "<li> Variables Booléennes :"
            "<ul>"
              "<li><code>Bor_resp_rep</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information "
              "si la caserne répondante est la même que la caserne responsable.</li>"
              "<li><code>Bor_inc_rep</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident "
              "et la casserne répondante sont dans le même arrondissement.</li>"
              "<li><code>Bor_inc_resp</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident "
              "et la caserne responsable sont dans le même arrondissement.</li>"
            "</ul></li>"
        "</ul>")
        , unsafe_allow_html=True)
