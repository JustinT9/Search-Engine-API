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

processingQueue = queue.Queue()

def getNLTKData(): 
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')

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
            # Get the next query from the queue
            query, userId = processingQueue.get()

            # Process the query
            parseSearchQuery(query, userId)

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
        processingQueue.put((query, userId))
        
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
        None 

    Returns:
        rankedDocumentIds (list): A list of ranked document IDs.
"""
def mockRankingAPI():
    userId, query = processingQueue.get()
    x = requests.get(f"http://lspt-index-ranking.cs.rpi.edu:6060/getDocumentScores?id={userId}&text={query}")
    print(x)
    return x;

"""
    Function to fetch document metadata and content from the Document Data Store API.

    Args:
        docId (int): Document ID.

    Returns:
        document (dict): Contains document metadata, title, link, and text content.
"""
def documentDataStoreAPI(docId):
    # processingQueue.join()
    client = MongoClient("mongodb://128.113.126.79:27017")
    db = client.test
    collection = db.RAW
    result = collection.find()
    for i in result:
        print(i)
    return result

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
        for docID in mockRankingAPI():
            document = documentDataStoreAPI(docID)
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

def receiveQueryTest(): 
    assert receiveQuery("hello", "user1") == True  
    assert receiveQuery("hello world", "user2") == True 
    assert receiveQuery("HelLo", "user1") == True 
    assert receiveQuery("HeLLo WorLd", "user3") == True
    assert receiveQuery("to", "user4") == True 
    assert receiveQuery("To be, or not to be", "user5") == True
    assert receiveQuery("C++ programming guide: variables & pointers (2024)!", "user5") == True
    assert receiveQuery("there are fishies in the pond", "user5") == True 
    assert receiveQuery("\"exact phrase search\"", "user6") == True 
    assert receiveQuery("", "user7") == True
    assert receiveQuery("a", "user8") == True 
    assert receiveQuery("   cat and dog   ", "user8") == True 

def parseSearchQueryTest():
    assert parseSearchQuery("hello") == ["hello"]
    assert parseSearchQuery("HeLLo WorLd") == ["hello", "world"]
    assert parseSearchQuery("HeLlo") == ["hello"]
    assert parseSearchQuery("HeLLo WorLd") == ["hello", "world"]
    assert parseSearchQuery("to") == []
    assert parseSearchQuery("To be, or not to be") == []
    assert parseSearchQuery("C++ programming guide: variables & pointers (2024)!") == ["program", "guid", "variabl", "pointer", "2024"]
    assert parseSearchQuery("there are fishies in the pond") == ["fishi", "pond"]
    assert parseSearchQuery("\"exact phrase search\"") == ["exact", "phrase", "search"]
    assert parseSearchQuery("") == []
    assert parseSearchQuery("a") == []
    assert parseSearchQuery("   cat and dog   ") == ["cat", "dog"] 

def runTest(): 
    receiveQueryTest() 
    parseSearchQueryTest()

# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Start the processing thread
    processingThread = threading.Thread(target=processQueue, daemon=True)
    processingThread.start()    

    # getNLTKData()
    processingQueue.put((1, ""))
    mockRankingAPI()
    # runTest()

    #documentDataStoreAPI('xddqb140kx4q4i0qisodfm12')