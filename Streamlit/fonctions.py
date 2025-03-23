import pandas as pd
import streamlit as st

def recup_df(nom,separateur = ','):
    try:
        df = pd.read_csv(f"Donnees/Doc csv/{nom}",sep = separateur ) 
        return df
    except FileNotFoundError:
        st.error(f"Le fichier {nom} n'a pas été trouvé.")
        return
    
def texte_justifie(texte):
    """Justifie le texte donné."""
    return f"""
    <div style="text-align: justify;">
    {texte}
    </div>
    """