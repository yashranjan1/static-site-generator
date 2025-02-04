import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # when both are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        # when the content is not the name
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a slightly different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
        # when the type is not the same
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)
        
        # when both have links but the link is not the same 
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, url="https://notexample.com")
        self.assertNotEqual(node, node2)
    
        # when the link for one is defined but isnt for the other 
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)
        
if __name__ == "__main__":
    unittest.main()