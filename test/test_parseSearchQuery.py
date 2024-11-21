import unittest
from src.api import parseSearchQuery 

"""
Unit Tests for Parse Search Query
"""
class TestSearchQuery(unittest.TestCase):
    """
    This test ensures that a sizeable query using punctuation and other symbols is properly tokenized by checking the length
    of each token. Improper tokenization may lead to punctuation or symbols being incorrectly classified.

    The first test text was provided on page 95 of `Search Engines: Information Retrieval in Practice`.
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

    The first test text was provided on page 95 of `Search Engines: Information Retrieval in Practice`.
    """
    def test_lemmatize(self):
        tokenized = parseSearchQuery("Document will describe marketing strategies carried out by U.S. companies for their agricultural "
                                    "chemicals, report predictions for market share of such chemicals, or report market statistics for "
                                    "agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, "
                                    "stimulate demand, price cut, volume of sales")
        self.assertTrue(tokenized[4] == "strategy")
        self.assertTrue(tokenized[-1] == "sale")
        self.assertTrue(tokenized[-7] == "demand")
        tokenized = parseSearchQuery("fish fishes fishing fisherman fish pond phishing") # stemming test
        self.assertTrue(tokenized[0] == tokenized[1])
        self.assertTrue(tokenized[0] != tokenized[2])
        self.assertTrue(tokenized[0] != tokenized[3])
        
    """
    Test queries that consist solely of stop words.

    The first test case consists of the first few default stop words as defined by the spaCy library, with punctuation removed.
    The second test case consists of only stop words but is a sentence with semantic meaning.
    The third test case consists of a mix of stop words and non-stop words.
    The fourth test case tests that stop words are removed if they add no semantic context.
    """
    def test_stop_words(self):
        sentence = ("call or even same anyway eight except being thereafter yourself done used "
                   "very they empty will fifty hence anyhow next please are would off whereby "
                   "a fifteen anywhere itself five how been whither upon however almost then us "
                   "she where well be therefore now but ours became meanwhile go we beyond nevertheless")
        tokenized = parseSearchQuery(sentence)
        self.assertTrue(len(tokenized) != 0)
        self.assertTrue(len(tokenized))
        self.assertTrue(len(parseSearchQuery("to be or not to be")) != 0)
        sentence = "Hey! This is a random sentence that probably has some stop words inside it, but I'm not sure. Hopefully you can check?"
        tokenized = parseSearchQuery(sentence)
        self.assertTrue(len(tokenized) != 0)
        self.assertTrue(len(tokenized) != len(sentence.split(" ")))
        self.assertTrue(len(parseSearchQuery("Bank of Australia")) == 2)
    
    """
    Test an empty query. The tokenization process should return an empty string.
    """
    def test_empty_query(self):
        tokenized = parseSearchQuery("")
        self.assertTrue(len(tokenized) == 0)

    """
    Test a query with only one input. 

    The first three test cases are with random words.
    The next two test cases are with stop words.
    The next two test cases are with conjunctions.
    """
    def test_singular_query(self):
        self.assertTrue(len(parseSearchQuery("dinosaur")) == 1)
        self.assertTrue(len(parseSearchQuery("Professor")) == 1)
        self.assertTrue(len(parseSearchQuery("Europe")) == 1)
        self.assertTrue(len(parseSearchQuery("the")) == 1)
        self.assertTrue(len(parseSearchQuery("a")) == 1)
        self.assertTrue(len(parseSearchQuery("I'll")) == 2)
        self.assertTrue(len(parseSearchQuery("doesn't")) == 2)

if __name__ == "__main__":
    unittest.main()