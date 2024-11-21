"""
The objective of this program is to model the
`parseSearchQuery()` API provided by text transformation.

Requirements for spaCy:
pip install -U spacy
python -m spacy download en_core_web_sm
"""
import spacy

nlp = spacy.load("en_core_web_sm")

def parseSearchQuery(query):
    doc = nlp(query)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop or not token.pos_ == "ADP"]
    #print(lemmatized) # Uncomment this line to view the text after being lemmatized.
    return lemmatized