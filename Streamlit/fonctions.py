import pandas as pd
import streamlit as st

def recup_df(nom,separateur = ','):
    try:
        df = pd.read_csv(f"Donnees/{nom}",sep = separateur ) 
        return df
    except FileNotFoundError:
        st.error(f"Le fichier {nom} n'a pas été trouvé.")
        return