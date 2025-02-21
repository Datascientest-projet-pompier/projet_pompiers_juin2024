import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


from page_intro import page_intro
from page1 import page1
from page2 import page2

def main():
    # Sidebar
    pages = {
        "Presentation":page_intro,
        "Presentation des données": page1,
        "Visualisation géographique des données": page2,
        "Visualisation des données": page1,
        "Prétraitement des données": page1,
        "Modélisation 1 - prédiction variable continue": page1,
        "Modélisation 2 - prédiction variable discrète": page1,
        "Conclusion et prespective": page1
    }

    # Barre latérale avec des boutons radio pour chaque page
    selected_page = st.sidebar.radio("Choisis une page", list(pages.keys()))

    # Appeler la fonction correspondant à la page sélectionnée
    pages[selected_page]()

    st.sidebar.write("""Auteurs : \n
    * Anne DUBOIS \n
    * Christelle TESSIER \n
    * Hao LA
    """)

if __name__ == "__main__":
    main()