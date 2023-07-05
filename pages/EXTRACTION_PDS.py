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
    ELEMENT=[]
    LIEN=[]
    ADRESSE=[]
    CHAMBRE=[]
    TYPE=[]
    POCHE=[]
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
            for index_bpe,bpe in enumerate(PDS):
                if index_bpe not in range(len(PDS)):
                    continue
                elif bpe=='ADRESSE / N° CHAMBRE':
                    BPE.append(PDS[index_bpe-1])
        
            # Récupération Champ Element
            for index_element,element in enumerate(PDS):
                if index_element not in range(len(PDS)):
                    continue
                elif str(element)=='Elément':
                    ELEMENT.append(PDS[index_element+1])
        
            # Récupération Champ Lien
            for index_lien,lien in enumerate(PDS):
                if index_lien not in range(len(PDS)):
                    continue
                elif str(lien)=='Lien':
                    LIEN.append(PDS[index_lien+1])
        
            # Récupération Champ Adresse
            for index_adresse,adresse in enumerate(PDS):
                if index_adresse not in range(len(PDS)):
                    continue
                elif str(adresse)=='ADRESSE / N° CHAMBRE':
                    ADRESSE.append(PDS[index_adresse+1].split('/')[0].strip())
        
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
        
            # Récupération Champ Poche
            for index_poche,poche in enumerate(PDS):
                if index_poche not in range(len(PDS)):
                    continue
                elif str(poche)=='POCHE':
                    POCHE.append(PDS[index_poche+1])
        
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
      
        ELEMENT=pd.Series(ELEMENT).reset_index(drop=True)
        LIEN=pd.Series(LIEN).reset_index(drop=True)
        ADRESSE=pd.Series(ADRESSE).reset_index(drop=True)
        CHAMBRE=pd.Series(CHAMBRE).reset_index(drop=True)
        TYPE=pd.Series(TYPE).reset_index(drop=True)
        POCHE=pd.Series(POCHE).reset_index(drop=True)
        STATUT=pd.Series(STATUT).reset_index(drop=True)
        CABLE=pd.Series(CABLE).drop_duplicates().reset_index(drop=True)
        BPE=pd.Series(BPE).reset_index(drop=True)
        
        df_out=pd.concat([ELEMENT,LIEN,POCHE,BPE,CHAMBRE,ADRESSE,TYPE,STATUT,CABLE],axis=1)
        df_out=df_out.rename(columns={0:'ELEMENT',1:'LIEN',2:'POCHE',3:'BPEU',4:'CHAMBRE',5:'ADRESSE',6:'TYPE',7:'STATUT',8:'CABLE'})
    
        st.subheader('PLAN DE SYNOPTIQUE')
        st.write(df_out)
        csv=convert_df(df_out)
    
        st.download_button(
            label='Télécharger',
            data=csv,
            file_name='PDS_out.csv',
            mime='text/csv'
        )
