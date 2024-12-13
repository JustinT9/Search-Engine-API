import unittest
from src.api import receiveQuery

class TestReceiveQuery(unittest.TestCase):
    def test_retrieveQuery(self):
        self.assertTrue(receiveQuery("hello", "user1") == True)
        self.assertTrue(receiveQuery("hello world", "user2") == True)
        self.assertTrue(receiveQuery("HelLo", "user1") == True)
        self.assertTrue(receiveQuery("HeLLo WorLd", "user3") == True)
        self.assertTrue(receiveQuery("to", "user4") == True)
        self.assertTrue(receiveQuery("To be, or not to be", "user5") == True)
        self.assertTrue(receiveQuery("C++ programming guide: variables & pointers (2024)!", "user5") == True)
        self.assertTrue(receiveQuery("there are fishies in the pond", "user5") == True)
        self.assertTrue(receiveQuery("\"exact phrase search\"", "user6") == True)
        self.assertTrue(receiveQuery("", "user7") == True)
        self.assertTrue(receiveQuery("a", "user8") == True)
        self.assertTrue(receiveQuery("   cat and dog   ", "user8") == True)

if __name__ == "__main__":
    unittest.main()