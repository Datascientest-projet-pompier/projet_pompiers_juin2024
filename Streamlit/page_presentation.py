import streamlit as st

def presentation():
    st.title("Présentation des données")
    st.write(
        "L'ensemble des données est divisé en deux sous-dossiers. Le premier sous-dossier permet d'obtenir "
        "les informations relatives aux incidents (disponible [ICI](https://data.london.gov.uk/dataset/london-fire-brigade-incident-records)). "
        "Le second sous-dossier permet d'obtenir les informations relatives à la mobilisation des casernes (disponible [ICI](https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records)). "
    )

    st.markdown("### Etude des données initiales")

    st.write("Que ce soit pour les données *Incident* ou les données *Mobilisation* les jeux de données possèdent une variable *IncidentNumber*"
             " qui permettra de faire la jointure entre les deux tableaux")

    st.write("L'ensemble des données de tous types et de tous ordres, on peut les regrouper en quatre catégories :")
    st.markdown("- **données temporelles :** qui permettent de situer dans le temps l'incident (année, date et heure).")
    st.markdown("- **données géographique :** qui permettent de situer l'incédent géographiquement (latitude, longitude, code postal ...)")
    st.markdown("- **données relatives à l'incident :** qui permettent de caractériser l'incident (caserne responsable/déployée, type d'incident, nombre de camion, coût ...)")
    st.markdown("- **données cibes :** qui représentent les temps de réaction, de trajet et total")

    st.markdown("### Gestion des valeurs manquantes")

    st.markdown("### Jointure")

    st.markdown("### Création des nouvelles variables")
    st.markdown("""
Pour simplifier notre jeu de données nous avons chercher à diminuer le nombre de variables en en regroupant certaines, elles correspondent uniquement aux deux dernières catégories.

<ul>
  <li><b>données relatives à l'incident :</b>
    <ul>
      <li>DetailedIncidentGroup : qui correspond à une simplification de la description de l'incident. Elle rassemble les variables StopCodeDescription et SpecialServiceType, c'est une variable catégorielle contenant 9 modalités</li>
      <li>Bor_inc_rep : qui correspond à un indicateur (vrai ou faux) donnant l'information si l'incident et la casserne responsable
                sont dans le même arrondissement.</li>
      <li>Bor_resp_rep : qui correspond à un indicateur (vrai ou faux) donnant l'information si la caserne responsable et la 
                caserne déployée sont dans le même arrondissement.</li>
      <li>Stat_resp_rep : qui correspond à un indicateur (vrai ou faux) donnant l'information si la caserne responsable et la 
                cassrne déployée sont identiques.</li>
      <li>Distance : qui  correspond à la distance (à vol d'oiseau) entre l'incident et la caserne déployée.</li> 
    </ul>
  </li>
  <li><b>données cibes :</b>
    <ul>
       <li>TotalResponseTime : qui correspond au temps total à savoir temps de réaction et temps de trajet.</li>                
  </li>
</ul>
""", unsafe_allow_html=True)


    st.markdown("### Variables consersvées pour l'étude")
