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

    image_url = "https://s3-eu-west-1.amazonaws.com/tpd/logos/5defb89bc1213200011e72d5/0x0.png"
    #st.image(image_url, width=None) # Affiche l'image à sa taille originale pour obtenir les dimensions.

    # Obtenir les dimensions de l'image (nécessite une requête HTTP)
    import requests
    from PIL import Image
    from io import BytesIO

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    original_width, original_height = img.size

    # Calculer la nouvelle largeur (20% de la largeur originale)
    new_width = int(original_width * 0.20)

    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="{image_url}" width="{new_width}">
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()