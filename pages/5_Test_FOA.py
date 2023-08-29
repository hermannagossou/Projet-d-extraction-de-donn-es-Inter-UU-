import streamlit as st
import pandas as pd
import numpy as np
import os

st.write(os.getcwd())

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write(bytes_data)


