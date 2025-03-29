import streamlit as st

import plotly.express as px
import matplotlib.pyplot as plt

def graph_countIncident(df, variable):
    """
    Affiche un barplot comptant le nombre d'incidents en fonction d'une variable catégorielle dans un DataFrame.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """
    df_count = df[['IncidentNumber', variable]].groupby(variable).agg(['count']).reset_index()
    
    # Création du graphique
    fig, ax = plt.subplots()
    ax.bar(list(df_count[variable]), list(df_count.IncidentNumber['count']))
    ax.set_ylabel("Nombre d'incidents")
    ax.set_xlabel(variable)
    ax.set_title(f"Nombre d'incidents pour les valeurs de {variable}")
    
    # Affichage du graphique dans Streamlit
    st.pyplot(fig)

def graphQuali_countPlot(df, variable):
    """
    Affiche un histogramme interactif de la distribution d'une variable catégorielle dans un DataFrame.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """
    fig = px.histogram(df, x=variable, nbins=30, title=f"Distribution de {variable}")
    
    # Personnaliser le layout
    fig.update_layout(
        height=600,
        width=800,
        barmode='group'  # Pour grouper les barres si nécessaire
    )
    
    # Affichage du graphique dans Streamlit
    st.plotly_chart(fig)
