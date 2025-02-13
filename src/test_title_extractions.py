import unittest

from main import extract_title

class TestTitleExtractions(unittest.TestCase):
    def test_extract_title(self):
        case = './content/index.md'
        title = extract_title(case)
        self.assertEqual(title, 'Tolkien Fan Club')

        case = './content/should_fail.md'
        self.assertRaises(Exception, extract_title(case))
