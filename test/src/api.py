import time
import queue
import threading
import json
import logging
import nltk
import requests
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pymongo import MongoClient
from fastapi import FastAPI

processingQueue = queue.Queue()
api = FastAPI()

def getNLTKData(): 
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
        nltk.download('wordnet')
        nltk.download('omw-1.4')

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

"""
    Processes queries from the processing queue.
"""
def processQueue():
    while True:
        try:
            userId, query = processingQueue.get()

            tokens = ' '.join(parseSearchQuery(query))
            print(tokens)

            getDocumentScores(userId, tokens)

            # Mark the task as done
            processingQueue.task_done()
        except Exception as e:
            logging.error(f"Error in processQueue: {str(e)}")

"""
    Receives a search query string from the user via UI/UX, logs it, and adds it to the 
    processing queue.

    Args:
        query (str): The search query string from the user.
        userId (optional): User identifier for tracking.

    Returns:
        True if query was successfully added; otherwise false. 
"""
def receiveQuery(query, userId=None):
    try:
        # Log the received query
        logging.info(f"Received query from user {userId}: {query}")

        # Add the query to the processing queue
        processingQueue.put((userId, query))
        
        return True 
    
    except Exception as e:
        logging.error(f"Error in receiveQuery: {str(e)}")

        return False

"""
    Processes the raw query string, tokenizes it, removes stop words and punctuation,
    and applies stemming or lemmatization.

    Args:
        query (str): Raw query string from receiveQuery().

    Returns:
        tokenizedQuery (list): Cleaned and normalized tokens for the next step.
"""
def parseSearchQuery(query):
    try:
        # Tokenize the query
        tokens = nltk.word_tokenize(query)

        # Remove punctuation and convert to lower case
        tokens = [word.lower() for word in tokens if word.isalnum()]

        # Remove stop words
        stopWords = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stopWords]

        # Apply stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]

        return tokens

    except Exception as e:
        logging.error(f"Error in parseSearchQuery: {str(e)}")
        return []

"""
    Formats the tokenized query into structured queries for ranking.

    Args:
        tokens (list): Tokenized and preprocessed query from parseSearchQuery().

    Returns:
        structuredQuery (dict): Formatted query ready for ranking.
"""
def generateQueries(tokens):
    try:
        # Create a structured query
        structuredQuery = {
            "operation": "AND",
            "terms": tokens
        }

        return structuredQuery

    except Exception as e:
        logging.error(f"Error in generateQueries: {str(e)}")
        return {}


"""
    Mock function to simulate interaction with the Ranking API.

    Args:
        userID - ID of user performing query
        query - tokenized string to rank documents

    Returns:
        rankedDocumentIds (list): A list of ranked document IDs.
"""
def getDocumentScores(userId, query):
    x = requests.get(f"http://lspt-index-ranking.cs.rpi.edu:6060/getDocumentScores?id={userId}&text={query}")
    # print(x)
    return x;

"""
    Function to fetch document metadata and content from the Document Data Store API.

    Args:
        docId (int): Document ID.

    Returns:
        document (dict): Contains document metadata, title, link, and text content.
"""
def getDocuments(docID):
    client = MongoClient("mongodb://128.113.126.79:27017")
    db = client.test
    collection = db.RAW
    result = collection.find()
    filtered = [i for i in result if i['_id'] == docID]
    MongoClient.close(client)
    return filtered 

"""
    Retrieves documents based on ranked document IDs.

    Args:
        rankedDocumentIds (list): A list of document IDs from the Ranking API.

    Returns:
        retrievedDocuments (list): Contains document metadata, titles, links, and text content.
"""
def retrieveDocuments():
    try:
        startTime = time.time()

        # Fetch documents from the Document Data Store API
        retrievedDocuments = []
        for docID in getDocumentScores():
            document = getDocuments(docID)
            if document:
                retrievedDocuments.append(document)

        # Log document retrieval times
        retrievalTime = time.time() - startTime
        logging.info(f"Document retrieval time: {retrievalTime:.2f} seconds")

        sendDocuments(retrievedDocuments)

        return retrievedDocuments

    except Exception as e:
        logging.error(f"Error in retrieveDocuments: {str(e)}")
        return []

"""
    Sends the processed documents to the UI/UX for display.

    Args:
        processedDocuments (list): Processed documents with title, snippet, and link.

    Returns:
        None
"""
def sendDocuments(processedDocuments):
    try:
        startTime = time.time()

        if not processedDocuments:
            logging.warning("No documents to send.")
            response = {
                "status": "No Results",
                "message": "No documents were found matching your query."
            }
        else:
            # Format data into JSON
            response = {
                "status": "Success",
                "documents": processedDocuments
            }

        # Simulate sending the response to UI/UX
        responseJson = json.dumps(response, indent=2)
        print(responseJson)

        # Log response times
        responseTime = time.time() - startTime
        logging.info(f"Response time: {responseTime:.2f} seconds")

    except Exception as e:
        logging.error(f"Error in sendDocuments: {str(e)}")
        response = {
            "status": "Error",
            "message": "An error occurred while processing your request."
        }
        responseJson = json.dumps(response, indent=2)
        print(responseJson)

"""
Generates snippet from document data
Args:
    documentContent: String containing the full content of the document.
    tokenizedQuery (list): Tokenized and preprocessed query from parseSearchQuery().
Returns:
    snippet: Snippet string for document
"""
def generateSnippet(documentContent, tokenizedQuery):
    try:
        snippet = ""
        maxWordCount = 0
        # Get each individual sentence in document
        sentences = nltk.sent_tokenize(documentContent)
        
        for sentence in sentences:
            wordCount = 0
            # tokenize sentence using same method as query
            words = nltk.word_tokenize(sentence)
            words = [word.lower() for word in words if word.isalnum()]
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]
            # Count how many words in the query are in the current sentence
            for queryWord in tokenizedQuery:
                for docWord in words:
                    if queryWord == docWord: 
                        wordCount = wordCount + 1
            # If sentence has more query words than current snippet, it is the new snippet
            if wordCount > maxWordCount:
                snippet = sentence
                maxWordCount = wordCount
        
        return snippet
    
    except Exception as e:
        logging.error(f"Error in generateSnippet: {str(e)}")
        return ""


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # setup text processing
    getNLTKData()

    # Start the processing thread
    #processingThread = threading.Thread(target=processQueue, daemon=True)
    #processingThread.start()    

    ### TODO: setup UI/UX; the following is mock data
    receiveQuery(1, "BIG CHUNGUS")
    receiveQuery(2, "Where is DCC?")
    receiveQuery(3, "I can't find West Hall.")
    receiveQuery(4, "Professor Goldschmidt OFfice hours")
    receiveQuery(5, "reddit.com")

    while True:
        try:
            userId, query = processingQueue.get()

            tokens = ' '.join(parseSearchQuery(query))
            print(tokens)

            getDocumentScores(userId, tokens)
        except Exception as e:
            logging.error(f"Error in processQueue: {str(e)}")
