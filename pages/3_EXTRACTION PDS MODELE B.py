import streamlit as st
import pandas as pd
import numpy as np

#st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title('EXTRACTION PDS MODELE B')

uploaded_file = st.file_uploader("Choisissez un fichier")

if uploaded_file is not None:
    df_dict = pd.read_excel(uploaded_file,sheet_name=None)

    ADRESSE=[]
    TYPE=[]
    STATUT=[]
    CABLE=[]
    BPE=[]
    
    for frame in df_dict:
        PDS=df_dict[frame].unstack().dropna().reset_index(drop=True)
        
        #Récupération du champ BPE
        BPE.append(PDS[PDS.str.contains('BPEU[0-9]|BPEA[0-9]',na=False)].iloc[0])

        #Récupération Champ Adresse
        ADRESSE.append(str(PDS[2].strip())+' '+str(PDS[3])+' '+str(PDS[4].strip()))

        # Récupération Champ Type BPE
        TYPE_CHAINE=PDS[PDS.str.contains('HD\s*$|FR6\s*$',na=False)]
        for type in TYPE_CHAINE:
            TYPE.append(type)

        # Recupération Champ Statut
        STATUT_CHAINE=PDS[PDS.str.contains('EPISSURE|EPISSUREE|PASSAGE',na=False)].drop_duplicates()
        for statut in STATUT_CHAINE:
            STATUT.append(statut)

        # Récupération Champ Cable
        CABLE_CHAINE=PDS[PDS.str.contains('CIU|CDP|CAD',na=False)]
        for cable in CABLE_CHAINE:
            CABLE.append(cable)

    ADRESSE_serie=pd.Series(ADRESSE).reset_index(drop=True)
    TYPE_serie=pd.Series(TYPE).reset_index(drop=True)
    STATUT_serie=pd.Series(STATUT).reset_index(drop=True)
    CABLE_serie=pd.Series(CABLE).drop_duplicates().reset_index(drop=True)
    BPE_serie=pd.Series(BPE).reset_index(drop=True)

    df_out=pd.concat([BPE_serie,ADRESSE_serie,TYPE_serie,STATUT_serie,CABLE_serie],axis=1)
    df_out=df_out.rename(columns={0:'BPEU',1:'ADRESSE',2:'TYPE',3:'STATUT',4:'CABLE'})
    
    st.subheader('PLAN DE SOUDURE')
    st.write(df_out)
    csv=convert_df(df_out)
    
    st.download_button(
        label='Télécharger',
        data=csv,
        file_name='PDS_out.csv',
        mime='text/csv'
    )
