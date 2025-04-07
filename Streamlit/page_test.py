import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

def test():
    st.write("Test de la page")

    components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <script>
                console.log('Test JavaScript dans Streamlit!');
            </script>
        </head>
        <body>
            <h1>Test HTML</h1>
        </body>
        </html>
        """, height=200)
