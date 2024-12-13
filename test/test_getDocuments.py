import unittest
from src.api import getDocuments 

"""
Unit Tests for getDocuments()
"""
class TestGetDocuments(unittest.TestCase):
    """
    Test basic functionality with a non-empty .txt document.
    """
    def test_get_txt(self):
        example_id = 'qv8i3qmok5l2v61jwwvdn08o'
        document = getDocuments(example_id);
        doc = document[0]
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
        document = getDocuments(empty_id)
        if len(document) != 0:
            doc = document[0]
            self.assertTrue(doc)
            self.assertTrue(doc != None)
            self.assertTrue(doc['_id'] == empty_id)
            self.assertTrue(doc['url'] != None)
            self.assertTrue(len(doc['text']) == 0)
            self.assertTrue(len(doc['text']) == doc['text_length'])

    """
    Test fetching a document that is not a txt document, but is an HTML document.
    """
    def test_html(self):
        html_id = 'ytx5t1mrf9noebwtbjfl7cjw'
        document = getDocuments(html_id)
        doc = document[0]
        self.assertTrue(doc != None)
        self.assertTrue(doc["_id"] == html_id)
        self.assertTrue(doc['url'] != None)
        self.assertTrue(len(doc['text']) == doc['text_length'])
        self.assertTrue(doc['type'] != 'txt')
        self.assertTrue(doc['type'] == 'html')
        
    """
    Test fetching a document ID that does not exist
    """
    def test_bad_id(self):
        bad_id = 'id_that_doesnt_match_anything'
        self.assertTrue(getDocuments(bad_id) == [])

if __name__ == "__main__":
    unittest.main()