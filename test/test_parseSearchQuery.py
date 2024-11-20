import unittest
from src.parseSearchQuery import parseSearchQuery 

"""
Unit Tests for Parse Search Query
"""
class TestSearchQuery(unittest.TestCase):
    """
    This test ensures that a sizeable query using punctuation and other symbols is properly tokenized by checking the length
    of each token. Improper tokenization may lead to punctuation or symbols being incorrectly classified.

    The first test text was provided on page 92 of `Search Engines: Information Retrieval in Practice`.
    The second and third texts were provided by https://spacy.io/usage/spacy-101.
    """
    def test_query_length(self):
        self.assertTrue(56, len(parseSearchQuery("Document will describe marketing strategies carried out by U.S. companies for their agricultural "
                                "chemicals, report predictions for market share of such chemicals, or report market statistics for "
                                "agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, "
                                "stimulate demand, price cut, volume of sales")))
        self.assertTrue(10, len(parseSearchQuery("Apple is looking at buying U.K. startup for $1 billion")))
        self.assertTrue(6, len(parseSearchQuery("Let's go to N.Y.!")))
    
    """
    This test ensures that similar words are correctly lemmatized without losing their original meaning, including words with multiple
    stems (fishes, fishing, fisherman, etc).

    The first test text was provided on page 92 of `Search Engines: Information Retrieval in Practice`.
    """
    def test_multiple_stems(self):
        tokenized = parseSearchQuery("Document will describe marketing strategies carried out by U.S. companies for their agricultural "
                                    "chemicals, report predictions for market share of such chemicals, or report market statistics for "
                                    "agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, "
                                    "stimulate demand, price cut, volume of sales")
        self.assertTrue(tokenized[4] == "strategy")
        self.assertTrue(tokenized[-1] == "sale")
        self.assertTrue(tokenized[-8] == "demand")
        tokenized = parseSearchQuery("I'm going to go fishing this Saturday with the boys.")
        self.assertTrue(tokenized[0] == "I")
        self.assertTrue(tokenized[2] == "go")
        self.assertTrue(tokenized[4] == "go")
        tokenized = parseSearchQuery("fish fishes fishing fisherman fish pond phishing")
        self.assertTrue(tokenized[0] == tokenized[1])
        self.assertTrue(tokenized[0] != tokenized[2])
        self.assertTrue(tokenized[0] != tokenized[3])
        
        ### TODO: further commenting on tests, we should have a test for stop words (may need to look at spaCy docs), a test with empty query, and a test with a single query, at least

if __name__ == "__main__":
    unittest.main()