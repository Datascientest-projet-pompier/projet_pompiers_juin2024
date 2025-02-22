import pandas as pd

df = pd.read_csv(r"C:\Users\33663\Desktop\Projet pompiers github\projet-pompiers\Data\ModelingDataset.csv", low_memory=False)
df2 = pd.read_csv(r"C:\Users\33663\Desktop\Projet pompiers github\projet-pompiers\Data\Data0\LFB incident et mobilisation data.csv", low_memory=False)

# Fusion des deux DataFrames sur 'IncidentNumber'
df_merged = pd.merge(df, df2, on='IncidentNumber', how='inner')

# Filtrer pour l'année 2024
df_2024 = df_merged[df_merged['CalYear_x'] == 2024]
print(df_2024)

# Select the desired columns and create df_carte
df_2024 = df_2024[['IncGeo_BoroughName','ResponseTimeBinary', 'inner', 'Latitude', 'Longitude']]

station = pd.read_csv(r'C:\Users\33663\Desktop\Projet pompiers github\projet-pompiers\Data\FireStationInfo_2.csv',sep = ";", low_memory=False)
# Sélection des colonnes souhaitées
station = station[["Station name", "Latitude", "Longitude"]]

# Conversion en majuscules de la colonne "Station name"
station["Station name"] = station["Station name"].str.upper()

print(df_2024['IncGeo_BoroughName'].unique)
print(station['Station name'].unique)
