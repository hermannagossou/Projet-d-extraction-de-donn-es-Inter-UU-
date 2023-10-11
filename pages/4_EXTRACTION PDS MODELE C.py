import streamlit as st
import pandas as pd
import numpy as np

#st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title('EXTRACTION PDS MODELE C')

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
    
    for frame in df_dict:
      PDS=df_dict[frame].unstack().dropna().reset_index(drop=True)

      #Récupération du champ BPE
      for index_bpe,bpe in enumerate(PDS):
          if bpe=='BPE Aval':
              BPE.append(PDS[index_bpe+1])
    
      #Récupération du champ Chambre
      CHAMBRE_CHAINE=PDS[PDS.str.contains('ORF_|BYT_|NXL_|COL_|OPE_|NEX_|POL|ATC_|OPT_',na=False)]
      CHAMBRE_CHAINE=CHAMBRE_CHAINE.reset_index(drop=True)
      print(CHAMBRE_CHAINE)
    
      #Récupération du champ Adresse
      ADRESSE_CHAINE=PDS[PDS.str.contains('[0-9]{5}\s+[A-Za-zÉÈéè-]+',na=False)]
      ADRESSE_CHAINE=ADRESSE_CHAINE.reset_index(drop=True)
      ADRESSE.append(ADRESSE_CHAINE.iloc[0])
    
      #Récupération du champ Type de boite
      TYPE_CHAINE=PDS[PDS.str.contains('HD\s*$|FR6\s*$',na=False)]
      TYPE_CHAINE=TYPE_CHAINE.reset_index(drop=True)
      TYPE.append(TYPE_CHAINE.iloc[0])
    
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
      for index_cable,cable in enumerate(PDS):
        if cable=='Câble Optique':
          CABLE.append(PDS[index_cable+1])
          CABLE.append(PDS[index_cable+2])

    #Conversion en series
    ADRESSE_serie=pd.Series(ADRESSE).reset_index(drop=True)
    CHAMBRE_serie=pd.Series(CHAMBRE).reset_index(drop=True)
    TYPE_serie=pd.Series(TYPE).reset_index(drop=True)
    STATUT_serie=pd.Series(STATUT).reset_index(drop=True)
    CABLE_serie=pd.Series(CABLE).drop_duplicates().reset_index(drop=True)
    BPE_serie=pd.Series(BPE).reset_index(drop=True)
        
    df_out=pd.concat([BPE_serie,CHAMBRE_serie,ADRESSE_serie,TYPE_serie,STATUT_serie,CABLE_serie],axis=1)
    df_out=df_out.rename(columns={0:'BPEU',1:'CHAMBRE',2:'ADRESSE',3:'TYPE',4:'STATUT',5:'CABLE'})
    
    st.subheader('PLAN DE SOUDURE')
    st.write(df_out)
    csv=convert_df(df_out)
    
    st.download_button(
        label='Télécharger',
        data=csv,
        file_name='PDS_out.csv',
        mime='text/csv'
    )
