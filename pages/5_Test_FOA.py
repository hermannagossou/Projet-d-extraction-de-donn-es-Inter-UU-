import streamlit as st
import pandas as pd
import numpy as np
import os
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  string_data = stringio.read()
  st.write(string_data)
