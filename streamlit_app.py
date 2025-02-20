import streamlit as st
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

@st.cache_data
def chargement_csv(url, separateur):
    try:
        df = pd.read_csv(url, sep=separateur, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
        return None  # Retourner None en cas d'erreur

def main():
    url = "https://drive.google.com/uc?export=download&id=14AtjzxbAqGfcdFDtzwgLBwmOU1K7Nmi_"
    df_2024 = chargement_csv(url, ",")
    url = "https://drive.google.com/uc?export=download&id=1p3GJaRpEvPZzRP3PbjxB4zdQpVyNnHnG"
    stations = chargement_csv(url, ";")

    if df_2024 is None or stations is None:
        st.error("Erreur lors du chargement des données. Veuillez vérifier les URLs.")
        return

    stations = stations[["Station name", "Latitude", "Longitude"]]
    stations["Station name"] = stations["Station name"].str.upper()

    st.title("Carte Interactive des Incidents ")
    st.sidebar.header("Filtrer par Caserne")

    casernes = sorted(df_2024["IncGeo_BoroughName"].unique().tolist())
    choix_caserne = st.sidebar.selectbox("Choisissez une caserne :", casernes, index=0)
    df_filtered = df_2024[df_2024["IncGeo_BoroughName"] == choix_caserne]
    station_caserne = stations[stations["Station name"] == choix_caserne]

    m = folium.Map(location=[df_filtered["Latitude"].mean(), df_filtered["Longitude"].mean()], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_filtered.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=row["IncGeo_BoroughName"],
            tooltip="Cliquez pour voir"
        ).add_to(marker_cluster)

    if station_caserne.empty:
        st.warning(f"⚠️ Attention : La caserne '{choix_caserne}' n'a pas été trouvée dans la base des stations.")
    else:
        folium.Marker(
            location=[station_caserne["Latitude"].values[0], station_caserne["Longitude"].values[0]],
            popup=f"Caserne : {choix_caserne}",
            tooltip="Caserne",
            icon=folium.Icon(color="black", icon="home")
        ).add_to(m)

    st_folium(m)

if __name__ == "__main__":
    main()