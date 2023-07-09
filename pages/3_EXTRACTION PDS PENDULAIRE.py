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

        #Récupération Champ Adresse
        ADRESSE.append(str(PDS[2].strip())+' '+str(PDS[3])+' '+str(PDS[4].strip()))

        # Récupération Champ Type BPE
        TYPE_CHAINE=PDS[PDS.str.contains('HD\s*$|FR6\s*$',na=False)]
        for type in TYPE_CHAINE:
            TYPE.append(type)

        # Recupération Champ Statut
        STATUT_CHAINE=PDS[PDS.str.contains('EPISSURE|EPISSUREE|PASSAGE',na=False)].drop_duplicates()

        # Récupération Champ Cable
        CABLE_CHAINE=PDS[PDS.str.contains('CIU|CDP|CAD',na=False)]
        for cable in CABLE_CHAINE:
            CABLE.append(cable)


st.write(BPE)
st.write(ADRESSE)
st.write(TYPE)
