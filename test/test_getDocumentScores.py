import unittest
from src.api import getDocumentScores, parseSearchQuery

"""
Unit Tests for getDocuments()
"""
class TestDocumentScores(unittest.TestCase):
    """
    Tokenize a standard query and test received documents
    """
    def test_get(self):
        docs = getDocumentScores("RPI")
        # confirm that documents have been received back
        self.assertTrue(docs != None)
        self.assertTrue(len(docs) > 0)

    """
    Attempt getting documents with empty query
    """
    def test_empty(self):
        docs = getDocumentScores("")
        # Behavior, as defined by requirements, should be that all documents are returned
        self.assertTrue(docs != None)
        self.assertTrue(len(docs) > 0)

    """
    Attempt to get documents with misleading query
    """
    def test_misleading(self):
        docs = getDocumentScores("Raspberry Pi")
        self.assertTrue(docs != None)
        self.assertTrue(len(docs) < 100) 
        docs = getDocumentScores("R.pi")
        self.assertTrue(docs != None)
        self.assertTrue(len(docs) < 500) 

    """
    Attempt to get documents with ridiculous query
    """
    def test_spam(self):
        docs = getDocumentScores("apwoeijapwoijpboia nwepoiawmpfoaiwejfp aoinmoiwjepoiawejpfaokmweoiapwlkaxzxaokzplawoeiupowiajv")
        self.assertTrue(docs != None)
        self.assertTrue(len(docs) == 0)


if __name__ == "__main__":
    unittest.main()