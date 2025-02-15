import unittest

from main import extract_title

class TestTitleExtractions(unittest.TestCase):
    def test_extract_title(self):
        case = '# Tolkien Fan Club'
        title = extract_title(case)
        self.assertEqual(title, 'Tolkien Fan Club')

        case = '## hello tro'
        with self.assertRaises(Exception):
            extract_title(case)
