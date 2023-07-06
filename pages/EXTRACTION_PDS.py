import streamlit as st
import pandas as pd
import numpy as np

#st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title('EXTRACTION PDS')

uploaded_file = st.file_uploader("Choisissez un fichier")

if uploaded_file is not None:
    df_dict = pd.read_excel(uploaded_file,sheet_name=None)

    ADRESSE=[]
    CHAMBRE=[]
    TYPE=[]
    STATUT=[]
    CABLE=[]
    BPE=[]
    BPENO=['BPESOUI','BPESNON','BPEDOUI','BPEDNON','BPEAOUI','BPEANON']
    
    for frame in df_dict:
        PDS=df_dict[frame].unstack().dropna().reset_index(drop=True)
        if frame in BPENO:
            continue
        else:
            #Récupération du champ BPE
            BPE_CHAINE=PDS[PDS.str.contains('BPEU[0-9]',na=False)]
            for bpe in BPE_CHAINE:
                BPE.append(bpe)
        
            # Récupération Champ Adresse
            ADRESSE_CHAINE=PDS[PDS.str.contains('[^ADRESSE][^CITE A][A-Za-z0-9ÉÈéè-]+\s*\/\s*[A-Z0-9_]+',na=False)]
            for adresse in ADRESSE_CHAINE:
                ADRESSE.append(adresse.split('/')[0].strip())
        
            # Récupération Champ Chambre
            CHAMBRE_CHAINE=PDS[PDS.str.contains('[^ADRESSE][A-Za-z0-9ÉÈéè-]+\s*\/\s*[A-Z0-9_]+',na=False)]
            for chambre in CHAMBRE_CHAINE:
                CHAMBRE.append(chambre.split('/')[1].strip())
        
            # Récupération Champ Type BPE
            TYPE_CHAINE=PDS[PDS.str.contains('FR6',na=False)]
            for type in TYPE_CHAINE:
                TYPE.append(type)
        
            # Récupération Champ Satut
            STATUT_CHAINE=PDS[PDS.str.contains('EPISSURE|EPISSUREE|PASSAGE',na=False)].drop_duplicates()
            for statut in STATUT_CHAINE:
                if statut=='EPISSURE':
                    STATUT.append('JOINT DROIT')
                elif statut=='PASSAGE':
                    STATUT.append('PASSAGE')
        
            # Récupération Champ Cable
            CABLE_CHAINE=PDS[PDS.str.contains('CIU',na=False)]
            for cable in CABLE_CHAINE:
                CABLE.append(cable)
    
    ADRESSE_serie=pd.Series(ADRESSE).reset_index(drop=True)
    CHAMBRE_serie=pd.Series(CHAMBRE).reset_index(drop=True)
    TYPE_serie=pd.Series(TYPE).reset_index(drop=True)
    STATUT_serie=pd.Series(STATUT).reset_index(drop=True)
    CABLE_serie=pd.Series(CABLE).drop_duplicates().reset_index(drop=True)
    BPE_serie=pd.Series(BPE).reset_index(drop=True)
        
    df_out=pd.concat([BPE_serie,CHAMBRE_serie,ADRESSE_serie,TYPE_serie,STATUT_serie,CABLE_serie],axis=1)
    df_out=df_out.rename(columns={0:'BPEU',1:'CHAMBRE',2:'ADRESSE',3:'TYPE',4:'STATUT',5:'CABLE'})
    
    st.subheader('PLAN DE SYNOPTIQUE')
    st.write(df_out)
    csv=convert_df(df_out)
    
    st.download_button(
        label='Télécharger',
        data=csv,
        file_name='PDS_out.csv',
        mime='text/csv'
    )
