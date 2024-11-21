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

Input: User-inputted query, as string
Output: Tokenized String

Provided by Text Transformation Module
"""
def parseSearchQuery(query):
    doc = nlp(query)
    tokens = [token for token in doc]
    ### Customization:
    ### tokens = [token for token in doc if not token.is_stop or not token.pos_ == "ADP"]
    return tokens 

"""
getDocuments(string id)

Input: String ID
Output: Document information in JSON

provided by Document Data Store
"""
def getDocuments(id):
    pass

"""
getDocumentScores(String query)

Input: Tokenized query as string
Output: Relevant document information

provided by Ranking
"""
def getDocumentScores(query):
    pass

"""
generateSnippet(String text, String query)

Input: Document's provided "text" field, and relevant query as String
Output: Snippet relevant to the provided query
"""
def generateSnippet(text, query):
    pass