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
    return nlp(query)

    
