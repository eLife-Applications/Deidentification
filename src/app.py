import streamlit as st
from deidentify.util import mask_annotations
from deidentify.base import Document
from deidentify.taggers import CRFTagger, DeduceTagger, FlairTagger
from deidentify.tokenizer import TokenizerFactory

# Voeg een titel toe aan je Streamlit-app
st.title("Anonimiseringstool voor Consultatievragen")

# Voeg een bestand uploader toe
uploaded_file = st.file_uploader("Importeer hier het CSV-bestand met consultatievragen", type=["csv"])
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file,sep=';')
    st.write(df)
    kolomnaam = st.text_input("Voer de naam van de kolom in waar de consultatievraag in staat en druk op enter (HOOFDLETTERGEVOELIG):")

    # Convert the Series to strings
    df_string = ';'.join(df.Consultatievraag.astype(str))

    # Wrap text in document
    documents_dummy = [
    Document(name='doc_01', text=df_string)
    ]

    # Select downloaded model
    model = 'model_bilstmcrf_ons_fast-v0.2.0'

    # Instantiate tokenizer
    tokenizer = TokenizerFactory().tokenizer(corpus='ons', disable=("tagger", "ner"))

    # Load tagger with a downloaded model file and tokenizer
    tagger = FlairTagger(model=model, tokenizer=tokenizer, verbose=False)

    # Annotate your documents
    annotated_docs_flair = tagger.annotate(documents_dummy)
        
    # Mask annotations of FlairTagger
    masked_doc_flair = mask_annotations(first_doc_flair)

    # Split the input string into a list using semicolons as the delimiter
    values = masked_doc_flair.text.split(";")

    # Create a DataFrame with a single column named 'Values'
    df['Flair (fast)'] = values
       
    # Maak downloadbare knoppen voor de geanonimiseerde vragen
    csv_deduce = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download geanonimiseerde vragen (Deduce) als CSV",
        data=csv_deduce,
        file_name='Geanonimiseerde_vragen_deduce.csv',
        mime='text/csv'
    )
else:
    st.warning("Je moet een CSV-bestand uploaden. Het bestandstype is nu niet herkend.")