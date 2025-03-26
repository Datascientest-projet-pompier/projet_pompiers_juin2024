import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def tab_stat(df):
    variables = ["TurnoutTimeSeconds", "TravelTimeSeconds", "TotalResponseTime", "distance","ratioSC"]

    # Calculer les statistiques
    stats = df[variables].describe()

    # Extraire les statistiques spécifiques
    moyenne = stats.loc["mean"].values
    ecart_type = stats.loc["std"].values
    minimum = stats.loc["min"].values
    q1 = stats.loc["25%"].values
    mediane = stats.loc["50%"].values
    q3 = stats.loc["75%"].values
    maximum = stats.loc["max"].values

    # Créer le DataFrame récapitulatif
    data = {
    "Mobilisation\n(Turnout)\n(s)": [moyenne[0], ecart_type[0], minimum[0], q1[0], mediane[0], q3[0], maximum[0]],
    "Trajet\n(Travel)\n(s)": [moyenne[1], ecart_type[1], minimum[1], q1[1], mediane[1], q3[1], maximum[1]],
    "Total\n(Turnout + Travel)\n(s)": [moyenne[2], ecart_type[2], minimum[2], q1[2], mediane[2], q3[2], maximum[2]],
    "Distance\n(mètre)": [moyenne[3], ecart_type[3], minimum[3], q1[3], mediane[3], q3[3], maximum[3]],
    "Ratio\n(m² par caserne)" :[moyenne[4], ecart_type[4], minimum[4], q1[4], mediane[4], q3[4], maximum[4]],
    }

    index = ["Moyenne", "Ecart-type", "Minimum", "1er interquartile", "Médiane", "3ème interquartile", "Maximum"]

    df_recap = pd.DataFrame(data, index=index)

    return df_recap
