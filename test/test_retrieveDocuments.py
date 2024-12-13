import unittest
from src.api import retrieveDocuments

"""
Unit Tests for getDocuments()
"""
class TestGetDocuments(unittest.TestCase):
    """
    Test functionality with a singular valid document ID
    """
    def test_get(self):
        example_id = ['upsd05ospdtlypl29ayzqhez']
        docs = (example_id)
        doc = docs[0]
        self.assertTrue(doc != None)
        self.assertTrue(doc['_id'] == example_id)
        self.assertTrue(doc['url'] != None)
        self.assertTrue(doc['type'] == 'txt')
        self.assertTrue(doc['text'] != None)
        self.assertTrue(len(doc['text']) == doc['text_length'])

    """
    Test fetching a document that has an empty text section.
    """
    def test_empty(self):
        empty_id = 'id_for_empty_doc'
        doc = retrieveDocuments(empty_id)
        self.assertTrue(doc != None)
        self.assertTrue(doc['_id'] == empty_id)
        self.assertTrue(doc['url'] != None)
        self.assertTrue(len(doc['text']) == 0)
        self.assertTrue(len(doc['text']) == doc['text_length'])

    """
    Test fetching a document that is not a txt document, but is an HTML document.
    """
    def test_html(self):
        html_id = ['id_for_html']
        doc = retrieveDocuments(html_id)
        self.assertTrue(doc != None)
        self.assertTrue(doc['_id'] == html_id)
        self.assertTrue(doc['url'] != None)
        self.assertTrue(len(doc['text']) == doc['text_length'])
        self.assertTrue(doc['type'] != 'txt')
        self.assertTrue(doc['type'] == 'html')
        
    """
    Test fetching a document ID that does not exist
    """
    def test_bad_id(self):
        bad_id = ['id_that_doesnt_match_anything']
        self.assertTrue(retrieveDocuments(bad_id) == None)

if __name__ == "__main__":
    unittest.main()