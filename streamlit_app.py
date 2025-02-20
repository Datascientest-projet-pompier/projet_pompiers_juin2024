import streamlit as st
import streamlit.components.v1 as components

def lire_html(chemin_fichier):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier HTML : {e}")
        return None

def main():
    st.title("Affichage de Cartes HTML")

    # Sélection de la carte à afficher
    carte_choisie = st.selectbox("Choisissez une carte :", ["BARKING AND DAGENHAM", "BEXLEY"])

    # Lire et afficher la carte HTML choisie
    if carte_choisie == "BARKING AND DAGENHAM":
        html_carte = lire_html("BARKING AND DAGENHAM.html")
    elif carte_choisie == "BEXLEY":
        html_carte = lire_html("BEXLEY.html")
    else:
        html_carte = None

    if html_carte:
        components.html(html_carte, height=600)  # Ajustez la hauteur selon vos besoins
    else:
        st.error("Carte HTML non trouvée.")

if __name__ == "__main__":
    main()