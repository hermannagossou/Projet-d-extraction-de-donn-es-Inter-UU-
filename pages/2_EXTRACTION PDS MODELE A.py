import streamlit as st
import pandas as pd
import numpy as np

#st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title('EXTRACTION PDS MODELE A')

uploaded_file = st.file_uploader("Choisissez un fichier")

if uploaded_file is not None:
    df_dict = pd.read_excel(uploaded_file,sheet_name=None)

    ADRESSE=[]
    CHAMBRE=[]
    TYPE=[]
    STATUT=[]
    CABLE=[]
    BPE=[]
    ELEMENT=[]
    BPENO=['BPESOUI','BPESNON','BPEDOUI','BPEDNON','BPEAOUI','BPEANON']
    
    for frame in df_dict:
        PDS=df_dict[frame].unstack().dropna().reset_index(drop=True)
        if frame in BPENO:
            continue
        else:
            # Récupération Champ Element
            for index_element,element in enumerate(PDS):
                if index_element not in range(len(PDS)):
                  continue
                elif str(element)=='Elément':
                  ELEMENT.append(PDS[index_element+1])
                elif str(element)=='Lien Inter-UU':
                  ELEMENT.append(PDS[index_element+1])
            
            #Récupération du champ BPE
            BPE.append(PDS[PDS.str.contains('BPEU[0-9]|BPEA[0-9]|BPEI[0-9]',na=False)].iloc[0])
        
            # Récupération Champ Adresse
            for index_adresse, adresse in enumerate(PDS):
                if index_adresse not in range(len(PDS)):
                    continue
                elif str(adresse)=='ADRESSE / N° CHAMBRE' and '/' in PDS[index_adresse+1]:
                    ADRESSE.append(PDS[index_adresse+1].split('/')[0].strip())
        
            # Récupération Champ Chambre
            for index_chambre, chambre in enumerate(PDS):
                if index_chambre not in range(len(PDS)):
                    continue
                elif str(chambre)=='ADRESSE / N° CHAMBRE' and '/' in PDS[index_chambre+1]:
                    CHAMBRE.append(PDS[index_chambre+1].split('/')[1].strip())
                elif str(chambre)=='ADRESSE / N° CHAMBRE' and '/' not in PDS[index_chambre+1]:
                    CHAMBRE.append(PDS[index_chambre+1])
        
            # Récupération Champ Type BPE
            TYPE_CHAINE=PDS[PDS.str.contains('HD\s*$|FR6\s*$',na=False)]
            for type in TYPE_CHAINE:
                TYPE.append(type.strip())
        
            # Récupération Champ Satut
            STATUT_CHAINE=PDS[PDS.str.contains('EPISSURE|EPISSUREE|PASSAGE',na=False)].drop_duplicates()
            for statut in STATUT_CHAINE:
                if statut=='EPISSURE':
                    STATUT.append('JOINT DROIT')
                elif statut=='EPISSUREE':
                    STATUT.append('JOINT DROIT')
                elif statut=='PASSAGE':
                    STATUT.append('PASSAGE')
        
            # Récupération Champ Cable
            CABLE_CHAINE=PDS[PDS.str.contains('CIU|CDP|CIC',na=False)]
            for cable in CABLE_CHAINE:
                CABLE.append(cable.strip())
    
    ADRESSE_serie=pd.Series(ADRESSE).reset_index(drop=True)
    CHAMBRE_serie=pd.Series(CHAMBRE).reset_index(drop=True)
    TYPE_serie=pd.Series(TYPE).reset_index(drop=True)
    STATUT_serie=pd.Series(STATUT).reset_index(drop=True)
    CABLE_serie=pd.Series(CABLE).drop_duplicates().reset_index(drop=True)
    BPE_serie=pd.Series(BPE).reset_index(drop=True)
    ELEMENT_serie=pd.Series(ELEMENT).reset_index(drop=True)
        
    df_out=pd.concat([ELEMENT_serie,BPE_serie,CHAMBRE_serie,ADRESSE_serie,TYPE_serie,STATUT_serie,CABLE_serie],axis=1)
    df_out=df_out.rename(columns={0:'Element',1:'BPEU',2:'CHAMBRE',3:'ADRESSE',4:'TYPE',5:'STATUT',6:'CABLE'})
    
    st.subheader('PLAN DE SOUDURE')
    st.write(df_out)
    csv=convert_df(df_out)
    
    st.download_button(
        label='Télécharger',
        data=csv,
        file_name='PDS_out.csv',
        mime='text/csv'
    )
