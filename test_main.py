from main import *
import unittest

class TestMainFunctions(unittest.TestCase):

    # test extract_title
    def test_eq(self):
        test_string = """

            Some text here 
            # Then a heading
            Maybe some more text here

        """
        expected = "Then a heading"
        self.assertEqual(extract_title(test_string), expected)

    def test_exception_handling(self):
        with self.assertRaises(Exception):
            title = extract_title("Some text, but not heading")
        
    def test_multiple_headings(self):
        test_string = """

            Some text here 
            # Then a heading
            ## Now another heading

        """
        expected = "Then a heading"
        self.assertEqual(extract_title(test_string), expected)





 