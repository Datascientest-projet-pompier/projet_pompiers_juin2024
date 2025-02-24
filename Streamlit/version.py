import streamlit as st
import numpy as np
import sklearn
import pandas as pd
import scipy
import skimage
import lime

st.write("NumPy version:", np.__version__)
st.write("Scikit-learn version:", sklearn.__version__)
st.write("Pandas version:", pd.__version__)
st.write("SciPy version:", scipy.__version__)
st.write("Scikit-image version:", skimage.__version__)
    
import pkg_resources

lime_version = pkg_resources.get_distribution("lime").version
st.write("Lime version:", lime_version)

st.write("Streamlit version :",st.__version__)