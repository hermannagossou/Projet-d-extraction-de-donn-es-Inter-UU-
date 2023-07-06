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
            for bpe in PDS:
                if str(bpe).startswith('BPEU'):
                    BPE.append(bpe)
        
            # Récupération Champ Adresse
            ADRESSE_CHAINE=PDS[PDS.str.contains('[0-9]+\s+[A-Za-z0-9ÉÈéè-]+\s+\/\s+[A-Z0-9_]+',na=False)]
            for adresse in ADRESSE_CHAINE:
                ADRESSE.append(adresse.split('/')[0].strip())
        
            # Récupération Champ Chambre
            for index_chambre,chambre in enumerate(PDS):
                if index_chambre not in range(len(PDS)):
                    continue
                elif str(chambre)=='ADRESSE / N° CHAMBRE':
                    CHAMBRE.append(PDS[index_chambre+1].split('/')[1].strip())
        
            # Récupération Champ Type BPE
            for index_type,type in enumerate(PDS):
                if index_type not in range(len(PDS)):
                    continue
                elif str(type)=='TYPE DE BPE':
                    TYPE.append(PDS[index_type+1])
        
            # Récupération Champ Satut
            for index_statut,statut in enumerate(PDS):
                if index_statut not in range(len(PDS)):
                    continue
                elif str(statut)=='CSE_01' and PDS[index_statut+1]=='EPISSUREE':
                    STATUT.append('JOINT DROIT')
                elif str(statut)=='CSE_24' and PDS[index_statut+1]=='PASSAGE':
                    STATUT.append('PASSAGE')
        
            # Récupération Champ Cable
            for index_cable,cable in enumerate(PDS):
                if index_cable not in range(len(PDS)):
                    continue
                elif str(cable)=='Câble':
                    CABLE.append(PDS[index_cable+2])
    
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
