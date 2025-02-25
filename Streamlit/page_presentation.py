import streamlit as st

def presentation():
    st.title("Présentation des données")
    st.write(
        "L'ensemble des données est divisé en deux sous-dossiers. Le premier sous-dossier permet d'obtenir "
        "les informations relatives aux incidents (disponible [ICI](https://data.london.gov.uk/dataset/london-fire-brigade-incident-records)). "
        "Les principales informations sont la date et l'heure, la position de l'incident (latitude, longitude), la caserne responsable, le type d'incident. "
        "Le second sous-dossier permet d'obtenir les informations relatives à la mobilisation des casernes (disponible [ICI](https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records)). "
        "Les principales informations sont la première caserne déployée, le temps de réaction (temps entre appel et départ de la caserne) le temps de travail (temps entre le départ de la caserne "
        "et l'arrivée sur les lieu de l'incident), le temps total (temps de réponse et temps de trajet)"
    )

    st.markdown("## Etude des données")

    st.markdown("### Les données Incidents")

    st.write("L'ensemble des données incidents contient 39 variables de tous types et de tous ordres, on peut les regrouper en "
             "... catégories :")
    st.markdown("- **données temporelles :** qui permettent de situer dans le temps l'incident")
    st.markdown("- **données géographique :** qui permettent de situer l'incédent géographique")
    st.markdown("- **données ")