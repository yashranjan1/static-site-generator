from helper_functions import text_node_to_html_node, split_nodes_delimiter
from typing import List
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
    
    def test_split_by_delimiter(self):
        node = TextNode("This text has some `code` in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE) 
        assert len(new_nodes) == 3
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text_type == TextType.TEXT

        node = TextNode("This text has some `code` in it.", TextType.TEXT)
        node2 = TextNode("This text has some `more code` in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node2, node], "`", TextType.CODE) 
        assert len(new_nodes) == 6
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text_type == TextType.TEXT
        assert new_nodes[4].text_type == TextType.CODE
        assert new_nodes[5].text_type == TextType.TEXT
        
        node = TextNode("This text has some **bold text** in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD) 
        assert len(new_nodes) == 3
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text_type == TextType.TEXT

        node = TextNode("This text has some *italics text* in it.", TextType.TEXT)
        node2 = TextNode("This text has some *more italics text* in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node, node2], "*", TextType.ITALIC) 
        assert len(new_nodes) == 6
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text_type == TextType.ITALIC
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text_type == TextType.TEXT
        assert new_nodes[4].text_type == TextType.ITALIC
        assert new_nodes[5].text_type == TextType.TEXT

        node = TextNode("This text has no delimiters in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node], "*", TextType.ITALIC) 
        assert len(new_nodes) == 1
        assert new_nodes[0].text_type == TextType.TEXT