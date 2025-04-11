import streamlit as st
from fonctions import texte_justifie

def presentation():
    st.title("Présentation des données")
    st.markdown(texte_justifie(
    "Les jeux de données sur les <b>incidents</b> et les <b>mobilisations</b> sont mis à jour tous les mois "
    "sur le site de la Brigade des Pompiers de Londres. "
    "La base de données sur les incidents est "
    "disponible <a href=\"https://data.london.gov.uk/dataset/london-fire-brigade-incident-records\">ICI</a>. "
    "Celle sur la mobilisation des camions de secours est disponible "
    "<a href=\"https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records\">ICI</a>. "
  ), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Création des onglets
    tab1, tab2, tab3, tab4 = st.tabs(["Etude des données initiales", "Gestion des valeurs manquantes","Nettoyage et jointure",
    "Création de variables"])

    with tab1:
      st.subheader("Etude des données initiales")

      st.markdown(texte_justifie(
        "Nous avons chargé les données depuis la base publique pour la dernière fois le 12/11/2024 "
        "(2 fichiers incidents et 3 mobilisations). "
        "Pour analyser ces données, nous avons utilisé python, comme pour tout l’ensemble du projet. "
        "Après chargement de chaque fichier dans un dataframe, nous avons concaténé les données incidents d'une part "
        " et mobilisations d'autre part."
        "<br>"
        " La variable <b>IncidentNumber</b> a ensuite permis de faire la jointure entre les deux dataframes."
        )
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

      st.markdown(texte_justifie(
        "L'ensemble des variables des deux bases peut être regroupé en quatre catégories :"
        "<ul><li><b>variables temporelles :</b> elles situent l'incident dans le temps (année, date et heure).</li>"
        "<li><b>variables géographiques :</b> elles situent l'incident dans l'espace (latitude, longitude, "
        "Borough, Ward, code postal ...)</li>"
        "<li><b>variables caractérisant l'incident :</b> elles définissent les circonstances et les moyens liés à  l'incident (type d'incident,"
        " caserne responsable et déployée, nombre de camions mobilisés, type de bâtiment impacté, coût, ...)</li>"
        "<li><b>variables cibles :</b> il s'agit du temps total de réaction des pompiers qui est la somme de leur temps de réaction et de trajet </li></ul>")
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

    with tab2:
      st.subheader("Gestion des valeurs manquantes")

      st.markdown("#### Sur les fichiers incidents")

      st.markdown(texte_justifie(
        "Les valeurs manquantes concernent principalement :"
        "<ul>"
          "<li><b>les données géographiques exactes.</b> Pour garantir l'anonymat, "
         "elles sont supprimées avant publication de la base de données. "         
          "Les coordonnées géographiques approximées utilisant le système national britannique (British National Grid ou BNG) sont toujours renseignées. "
          "Nous les avons utilisées si les données géographiques exactes sont manquantes afin de calculer une latitude et longitude approximées.</li>"
          "<li><b>la variable <code>SpecialServiceType</code> </b> est renseignée uniquement si la variable "
          "<code>StopCodeDescription</code> a pour valeur \"<it>Special Service</it>\".</li> "
          "<li><b>les informations sur le premier et second camion arrivé sur site</b>. "
          " Il peut n’y avoir qu’un voire aucun camion déployé. Ces lignes sont supprimées lors de la jointure.</li></ul>")
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

      st.markdown("#### Sur les fichiers mobilisations")

      st.markdown(texte_justifie(
        "Les valeurs manquantes concernent :"
        "<ul><li><b>l’heure de retour du camion à la caserne.</b> Elle n'est plus renseignée depuis une dizaine d'années.</li>"
        "<li><b>la raison d'un retard de trajet </b>(comme le trafic routier). Elle est renseignée dans 25% des cas.</li>"
        "<li> <b>la date et heure de départ du camion.</b> Cette information est indispensable "
        "pour le calcul de la variable cible. Nous avons donc supprimé les lignes correspondantes (moins de 1.5% des lignes avant jointure)."
        "</li></ul>")
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

    with tab3:
      st.subheader("Nettoyage et jointure")

      st.markdown(texte_justifie(
        "Le 9 janvier 2014 les autorités londoniennes ont fermés 10 casernes. Nous avons donc choisis de ne"
        " conserver que les événements passés après cette date.")
        , unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

      st.markdown(texte_justifie(
        "Nous avons aussi remarqué des incohérences entre certaines variables, certaines étaient temporelles "
        "(heure d'arrivée < heure de départ) d'autre d'ordre technique (caserne des camions affectés différentes dans "
        "incidents et mobilisation)...<br>Si la ligne correspondante à un incident contenait une incohérence elle à été supprimée.")
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

    with tab4:
      st.subheader("Création des nouvelles variables")


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
              "<li><code>inner</code> : donnant l'information si l'arrondissement est dans le \"Londres Interieur\" "
              "ou le \"Londres Extérieur\" (définition donnée par l'Office for National Statistics (ONS))</li>"
              "<li><code>RatioSC</code> : représentant la superficie affectée a une caserne (distinction par arrondissement)</li>"
              "<li><code>Distance</code> : représentant la distance à vol d'oiseau entre la caserne et l'incident</li>"
            "</ul></li>"

          "<li> Variables Booléennes :"
            "<ul>"
              "<li><code>Stat_resp_rep</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information "
              "si la caserne répondante est la même que la caserne responsable.</li>"
              "<li><code>Bor_resp_rep</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information "
              "si la caserne répondante est dans le même arrondissement que la même que la caserne responsable.</li>"
              "<li><code>Bor_inc_rep</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident "
              "et la casserne répondante sont dans le même arrondissement.</li>"
              "<li><code>Bor_inc_resp</code> : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident "
              "et la caserne responsable sont dans le même arrondissement.</li>"
            "</ul></li>"
        "</ul>")
        , unsafe_allow_html=True)
