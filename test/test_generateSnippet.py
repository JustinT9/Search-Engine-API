import unittest
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from src.api import generateSnippet, parseSearchQuery

# Function to convert string into tokenized query for testing
def tokenize(query):
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


# Unit Tests for Parse Search Query
class TestSnippetGeneration(unittest.TestCase):
    # test finding a snippet when the entire query string can be found in the middle of the document
    def test_full_query(self):
        text = "Here is a bunch of text. This is where you find the words from the query. Here is more text."
        query = tokenize("find the words from the query")
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "This is where you find the words from the query.")

    """
    Test a query wherein a stemmed version of a root word is found within the text;
    """
    def test_stemming(self):
        # Test a partial match: predicted sales vs predict sale
        text = ("Document will describe marketing strategies carried out by U.S. companies for their agricultural "
                    "chemicals, report predictions for market share of such chemicals, or report market statistics for "
                    "agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, "
                    "stimulate demand, price cut, volume of sales")
        query = tokenize("predict sale market share")
        snippet = generateSnippet(text, query)
        # Report snippet as full sentence
        self.assertTrue(snippet == text)
        text = "fish fishing fisherman fishes"
        query = tokenize(text)
        self.assertTrue(generateSnippet(text, query) == text)
        text = "fish fishes fisherman. fisherman"
        query = tokenize("fish fish fisherman")
        self.assertTrue(generateSnippet(text, query) == "fish fishes fisherman.")
        text = "fish fishes fisherman. fishes"
        self.assertTrue(generateSnippet(text, query) == "fish fishes fisherman.")

    """
    Test queries longer than crawled text
    """
    def test_long_query(self):
        text = "This is really short!"
        query = tokenize("this sentence is really really long but matches the text")
        self.assertTrue(generateSnippet(text, query) == text)
        query = tokenize("Long sentence doesn't match the text")
        self.assertTrue(generateSnippet(text, query) == "")

    """
    Test snippet generation with no provided text or query
    """
    def test_fully_empty(self):
        self.assertTrue(generateSnippet("", tokenize("")) == "")

    """
    Test for null values
    """
    def test_null(self):
        generateSnippet(None, None)
        self.assertTrue(1 == 1) # Test that the program has not crashed on generateSnippet

    # test finding a snippet where some words from the query string are close together at the end of the text
    def test_some_words(self):
        text = "Here is a bunch of text. Here is more text. Here are some query words to find."
        query = tokenize("find the words from the query")
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "Here are some query words to find.")

    # test finding a snippet where only one word from the query string is found at the beginning of the text
    def test_one_word(self):
        text = "This sentence says query. Here is some text. Here is more text."
        query = tokenize("find the words from the query")
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "This sentence says query.")
        
    # test with empty text string (return empty string)
    def test_empty_text(self):
        text = ""
        query = tokenize("a query")
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "")

    # test with empty query string (return empty string)
    def test_empty_query(self):
        text = "some text"
        query = tokenize("")
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "")

if __name__ == "__main__":
    unittest.main(verbosity=2)