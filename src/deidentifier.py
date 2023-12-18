#Importeren Modules

#Deduce
from deduce import Deduce
deduce = Deduce()
import pandas as pd

#Streamlit
import streamlit as st


# Voeg een titel toe aan je Streamlit-app
st.title("Anonimiseringstool voor Consultatievragen")

# Voeg een bestand uploader toe
uploaded_file = st.file_uploader("Importeer hier het CSV-bestand met consultatievragen", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,sep=';')
    st.write(df)
    
    # Voer de anonimisering uit
    deduce = Deduce()
        
    kolomnaam = st.text_input("Voer de naam van de kolom in waar de consultatievraag in staat en druk op enter (HOOFDLETTERGEVOELIG):")
    
    vragen_deduce = []
    anonimized_texts = []
    
    for vraag in df[kolomnaam]:
        # Deduce anonimisering
        doc_deduce = deduce.deidentify(vraag)
        vragen_deduce.append(doc_deduce.deidentified_text)
        

    # Voeg geanonimiseerde kolommen toe aan het DataFrame
    geanonimiseerd_deduce_df = pd.DataFrame({'Vragen Geanonimiseerd Deduce': vragen_deduce})
       
    # Maak downloadbare knoppen voor de geanonimiseerde vragen
    csv_deduce = geanonimiseerd_deduce_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download geanonimiseerde vragen (Deduce) als CSV",
        data=csv_deduce,
        file_name='Geanonimiseerde_vragen_deduce.csv',
        mime='text/csv'
    )
else:
    st.warning("Je moet een CSV-bestand uploaden. Het bestandstype is nu niet herkend.")
