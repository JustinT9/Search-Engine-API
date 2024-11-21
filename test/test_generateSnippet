import unittest
from src.api import generateSnippet 

# Unit Tests for Parse Search Query
class TestSnippetGeneration(unittest.TestCase):
    # test finding a snippet when the entire query string can be found in the middle of the document
    def test_full_query(self):
        text = "Here is a bunch of text. This is where you find the words from the query. Here is more text."
        query = "find the words from the query"
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "This is where you find the words from the query. Here is more text.")
    # test finding a snippet where some words from the query string are close together at the end of the text
    def test_some_words(self):
        text = "Here is a bunch of text. Here is more text. Here are some query words to find."
        query = "find the words from the query"
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "Here is more text. Here are some query words to find.")
    # test finding a snippet where only one word from the query string is found at the beginning of the text
    def test_one_word(self):
        text = "This sentence says query. Here is some text. Here is more text."
        query = "find the words from the query"
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "This sentence says query. Here is some text.")
    # test with empty text string (return empty string)
    def test_empty_text(self):
        text = ""
        query = "a query"
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "")
    # test with empty query string (return empty string)
    def test_empty_query(self):
        text = "some text"
        query = ""
        snippet = generateSnippet(text, query)
        self.assertTrue(snippet == "")

if __name__ == "__main__":
    unittest.main()