import logging
import queue
import threading
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import json
import time

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a processing queue
processingQueue = queue.Queue()

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def receiveQuery(query, userId=None):
    """
    Receives a search query string from the user, logs it, and adds it to the processing queue.

    Args:
        query (str): The search query string from the user.
        userId (optional): User identifier for tracking.

    Returns:
        None
    """
    try:
        # Log the received query
        logging.info(f"Received query from user {userId}: {query}")

        # Add the query to the processing queue
        processingQueue.put((query, userId))

    except Exception as e:
        logging.error(f"Error in receiveQuery: {str(e)}")


def parseSearchQuery(query):
    """
    Processes the raw query string, tokenizes it, removes stop words and punctuation,
    and applies stemming or lemmatization.

    Args:
        query (str): Raw query string from receiveQuery().

    Returns:
        tokenizedQuery (list): Cleaned and normalized tokens for the next step.
    """
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

        # Proceed to the next step
        generateQueries(tokens)

        return tokens

    except Exception as e:
        logging.error(f"Error in parseSearchQuery: {str(e)}")
        return []


def generateQueries(tokenizedQuery):
    """
    Formats the tokenized query into structured queries for ranking.

    Args:
        tokenizedQuery (list): Tokenized and preprocessed query from parseSearchQuery().

    Returns:
        structuredQuery (dict): Formatted query ready for ranking.
    """
    try:
        # Create a structured query
        structuredQuery = {
            "operation": "AND",
            "terms": tokenizedQuery
        }

        # Simulate interaction with the Ranking API
        rankedDocumentIds = rankingAPI(structuredQuery)

        # Proceed to retrieveDocuments()
        retrieveDocuments(rankedDocumentIds)

        return structuredQuery

    except Exception as e:
        logging.error(f"Error in generateQueries: {str(e)}")
        return {}


def retrieveDocuments(rankedDocumentIds):
    """
    Retrieves documents based on ranked document IDs.

    Args:
        rankedDocumentIds (list): A list of document IDs from the Ranking API.

    Returns:
        retrievedDocuments (list): Contains document metadata, titles, links, and text content.
    """
    try:
        startTime = time.time()

        # Fetch documents from the Document Data Store API
        retrievedDocuments = []
        for docId in rankedDocumentIds:
            document = documentDataStoreAPI(docId)
            if document:
                retrievedDocuments.append(document)

        # Log document retrieval times
        retrievalTime = time.time() - startTime
        logging.info(f"Document retrieval time: {retrievalTime:.2f} seconds")

        # Proceed to sendDocuments()
        sendDocuments(retrievedDocuments)

        return retrievedDocuments

    except Exception as e:
        logging.error(f"Error in retrieveDocuments: {str(e)}")
        return []


def sendDocuments(processedDocuments):
    """
    Sends the processed documents to the UI/UX for display.

    Args:
        processedDocuments (list): Processed documents with title, snippet, and link.

    Returns:
        None
    """
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


def processQueue():
    """
    Processes queries from the processing queue.
    """
    while True:
        try:
            # Get the next query from the queue
            query, userId = processingQueue.get()

            # Process the query
            parseSearchQuery(query)

            # Mark the task as done
            processingQueue.task_done()
        except Exception as e:
            logging.error(f"Error in processQueue: {str(e)}")


def rankingAPI(structuredQuery):
    """
    Mock function to simulate interaction with the Ranking API.

    Args:
        structuredQuery (dict): Structured query from generateQueries().

    Returns:
        rankedDocumentIds (list): A list of ranked document IDs.
    """
    # Mock document IDs
    rankedDocumentIds = [1, 2, 3, 4, 5]
    return rankedDocumentIds


def documentDataStoreAPI(docId):
    """
    Mock function to simulate fetching document metadata and content from the Document Data Store API.

    Args:
        docId (int): Document ID.

    Returns:
        document (dict): Contains document metadata, title, link, and text content.
    """
    # Mock document
    document = {
        "id": docId,
        "title": f"Document Title {docId}",
        "link": f"http://example.com/doc/{docId}",
        "content": f"This is the content of document {docId}."
    }
    return document


# Start the processing thread
processingThread = threading.Thread(target=processQueue, daemon=True)
processingThread.start()

# Example usage
if __name__ == "__main__":
    # Simulate receiving queries from users
    receiveQuery("OpenAI develops advanced AI models.", userId=1)
    receiveQuery("Python programming language tutorial.", userId=2)

    # Wait for the processing queue to be empty
    processingQueue.join()