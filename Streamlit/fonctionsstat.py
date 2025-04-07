import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def tab_stat(df):
    variables = ["TurnoutTimeSeconds", "TravelTimeSeconds", "TotalResponseTime", "distance", "ratioSC"]

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

    # Formatter les nombres avec deux chiffres après la virgule et la notation française
    def format_number(number):
        return "{:,.2f}".format(number).replace(",", " ").replace(".", ",")

    formatted_moyenne = [format_number(x) for x in moyenne]
    formatted_ecart_type = [format_number(x) for x in ecart_type]
    formatted_minimum = [format_number(x) for x in minimum]
    formatted_q1 = [format_number(x) for x in q1]
    formatted_mediane = [format_number(x) for x in mediane]
    formatted_q3 = [format_number(x) for x in q3]
    formatted_maximum = [format_number(x) for x in maximum]

    # Créer le DataFrame récapitulatif
    data = {
        "Mobilisation\n(Turnout)\n(s)": formatted_moyenne[0],
        "Trajet\n(Travel)\n(s)": formatted_moyenne[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_moyenne[2],
        "Distance\n(mètre)": formatted_moyenne[3],
        "Ratio\n(m² par caserne)": formatted_moyenne[4],
    }

    index = ["Moyenne", "Ecart-type", "Minimum", "1er interquartile", "Médiane", "3ème interquartile", "Maximum"]
    df_recap_moyenne = pd.DataFrame(data, index=["Moyenne"])

    data_ecart_type = {
        "Mobilisation\n(Turnout)\n(s)": formatted_ecart_type[0],
        "Trajet\n(Travel)\n(s)": formatted_ecart_type[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_ecart_type[2],
        "Distance\n(mètre)": formatted_ecart_type[3],
        "Ratio\n(m² par caserne)": formatted_ecart_type[4],
    }
    df_recap_ecart_type = pd.DataFrame(data_ecart_type, index=["Ecart-type"])

    data_min = {
        "Mobilisation\n(Turnout)\n(s)": formatted_minimum[0],
        "Trajet\n(Travel)\n(s)": formatted_minimum[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_minimum[2],
        "Distance\n(mètre)": formatted_minimum[3],
        "Ratio\n(m² par caserne)": formatted_minimum[4],
    }
    df_recap_min = pd.DataFrame(data_min, index=["Minimum"])

    data_q1 = {
        "Mobilisation\n(Turnout)\n(s)": formatted_q1[0],
        "Trajet\n(Travel)\n(s)": formatted_q1[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_q1[2],
        "Distance\n(mètre)": formatted_q1[3],
        "Ratio\n(m² par caserne)": formatted_q1[4],
    }
    df_recap_q1 = pd.DataFrame(data_q1, index=["1er interquartile"])

    data_mediane = {
        "Mobilisation\n(Turnout)\n(s)": formatted_mediane[0],
        "Trajet\n(Travel)\n(s)": formatted_mediane[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_mediane[2],
        "Distance\n(mètre)": formatted_mediane[3],
        "Ratio\n(m² par caserne)": formatted_mediane[4],
    }
    df_recap_mediane = pd.DataFrame(data_mediane, index=["Médiane"])

    data_q3 = {
        "Mobilisation\n(Turnout)\n(s)": formatted_q3[0],
        "Trajet\n(Travel)\n(s)": formatted_q3[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_q3[2],
        "Distance\n(mètre)": formatted_q3[3],
        "Ratio\n(m² par caserne)": formatted_q3[4],
    }
    df_recap_q3 = pd.DataFrame(data_q3, index=["3ème interquartile"])

    data_max = {
        "Mobilisation\n(Turnout)\n(s)": formatted_maximum[0],
        "Trajet\n(Travel)\n(s)": formatted_maximum[1],
        "Total\n(Turnout + Travel)\n(s)": formatted_maximum[2],
        "Distance\n(mètre)": formatted_maximum[3],
        "Ratio\n(m² par caserne)": formatted_maximum[4],
    }
    df_recap_max = pd.DataFrame(data_max, index=["Maximum"])

    df_recap = pd.concat([df_recap_moyenne, df_recap_ecart_type, df_recap_min, df_recap_q1, df_recap_mediane, df_recap_q3, df_recap_max])

    return df_recap


def tab_stat2(df):
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
