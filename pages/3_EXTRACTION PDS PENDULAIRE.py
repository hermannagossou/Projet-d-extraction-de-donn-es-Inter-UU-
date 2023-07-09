import streamlit as st
import pandas as pd
import numpy as np

#st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title('EXTRACTION PDS PENDULAIRE')

uploaded_file = st.file_uploader("Choisissez un fichier")

if uploaded_file is not None:
    df_dict = pd.read_excel(uploaded_file,sheet_name=None)

    ADRESSE=[]
    CHAMBRE=[]
    TYPE=[]
    STATUT=[]
    CABLE=[]
    BPE=[]
    
    for frame in df_dict:
        PDS=df_dict[frame].unstack().dropna().reset_index(drop=True)
        
        #Récupération du champ BPE
        BPE.append(PDS[PDS.str.contains('BPEU[0-9]|BPEA[0-9]',na=False)])
        
        st.write(PDS)
        st.wrtite(PDS.loc[1])

st.write(BPE)
