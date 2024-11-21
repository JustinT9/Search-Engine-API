"""
The objective of this program is to model the real API calls
that the Querying module will handle.

Requirements for spaCy:
pip install -U spacy
python -m spacy download en_core_web_sm
"""
import spacy

nlp = spacy.load("en_core_web_sm")


"""
parseSearchQuery(String str)

Provided by Text Transformation Module
"""
def parseSearchQuery(query):
    doc = nlp(query)
    return doc

"""
getDocuments(string id)

provided by Document Data Store
"""
def getDocuments():
    pass