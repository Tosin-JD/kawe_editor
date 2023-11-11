import unittest
from unittest.mock import patch, MagicMock
from app import TextEditor 


class TestTextEditor(unittest.TestCase):

    def setUp(self):
        self.editor = TextEditor()

    def test_count_words(self):
        # Test with a simple string
        text = "This is a test."
        result = self.editor.count_words(text)
        self.assertEqual(result, 4)

        # Test with an empty string
        empty_text = ""
        result_empty = self.editor.count_words(empty_text)
        self.assertEqual(result_empty, 0)

        # Test with a more complex string
        complex_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        result_complex = self.editor.count_words(complex_text)
        self.assertEqual(result_complex, 8)

    # Add more test methods for other functions or methods in your TextEditor class

if __name__ == '__main__':
    unittest.main()
