from helper_functions import text_node_to_html_node
import unittest
from textnode import TextNode, TextType

class TestHelperFuntions(unittest.TestCase):
    def test_conversion_function(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag is None
        assert html_node.value == "Hello, world!" 
        
        text_node = TextNode("This is some bold text!", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "This is some bold text!"
        
        text_node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.props == {
            "href": "https://example.com",
        }
        
        text_node = TextNode("This is an image", TextType.IMAGE, "https://www.iana.org/_img/2025.01/iana-logo-header.svg")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"   
        assert html_node.props == {
            "src": "https://www.iana.org/_img/2025.01/iana-logo-header.svg",
            "alt": "This is an image"
        }
        assert html_node.props != {
            "src": "https://www.iana.org/_img/2025.01/iana-logo-header.svg",
            "alt": "This is an image",
            "href": "https://example.com",
        }
        
        