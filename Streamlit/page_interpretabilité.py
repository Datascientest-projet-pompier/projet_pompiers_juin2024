import streamlit as st

from fonctions import texte_justifie

def interpretabilite():
    st.title("Interpretabilité du modèle")

    st.markdown(texte_justifie(
        "Dans cette partie nous monterons l'interprétabilité(global) et l'explicabilité(local) du modèle.")
    , unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)