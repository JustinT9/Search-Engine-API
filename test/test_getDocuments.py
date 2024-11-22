import unittest
from src.api import getDocuments 

"""
Unit Tests for getDocuments()
"""
class TestGetDocuments(unittest.TestCase):
    """
    Test basic functionality with a non-empty .txt document.
    """
    def test_get(self):
        example_id = 'upsd05ospdtlypl29ayzqhez'
        doc = getDocuments(example_id);
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
        doc = getDocuments(empty_id)
        self.assertTrue(doc != None)
        self.assertTrue(doc['_id'] == empty_id)
        self.assertTrue(doc['url'] != None)
        self.assertTrue(len(doc['text']) == 0)
        self.assertTrue(len(doc['text']) == doc['text_length'])

    """
    Test fetching a document that is not a txt document, but is an HTML document.
    """
    def test_html(self):
        html_id = 'id_for_html'
        doc = getDocuments(html_id)
        self.assertTrue(doc != None)
        self.assertTrue(doc['_id'] == html_id)
        self.assertTrue(doc['url'] != None)
        self.assertTrue(len(doc['text']) == doc['text_length'])
        self.assertTrue(doc['type'] != 'txt')
        self.assertTrue(doc['type'] == 'html')

if __name__ == "__main__":
    unittest.main()