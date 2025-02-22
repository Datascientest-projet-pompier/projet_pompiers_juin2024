import streamlit as st

def page1():
    st.title("Présentation des données")
    st.write(
        "L'ensemble des données est divisé en deux sous-dossiers. Le premier sous-dossier permet d'obtenir "
        "les informations relatives aux incidents (disponible [ICI](https://data.london.gov.uk/dataset/london-fire-brigade-incident-records)). "
        "Les principales informations sont la date et l'heure, la position de l'incident (latitude, longitude), la caserne responsable, le type d'incident. "
        "Le second sous-dossier permet d'obtenir les informations relatives à la mobilisation des casernes (disponible [ICI](https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records)). "
        "Les principales informations sont la première caserne déployée, le temps de réaction (temps entre appel et départ de la caserne) le temps de travail (temps entre le départ de la caserne "
        "et l'arrivée sur les lieu de l'incident), le temps total (temps de réponse et temps de trajet)"
    )