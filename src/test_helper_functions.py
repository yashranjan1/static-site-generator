from helper_functions import *
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
    

    def test_image_extractor(self):
        text = "This is a ![random image](https://doesntexist.com) i found"
        result = extract_markdown_images(text)
        assert len(result) == 1
        assert result[0][0] == "random image"
        assert result[0][1] == "https://doesntexist.com"
        
        text = "This is a ![random image](https://doesntexist.com) and ![another random image](https://doesntexist2.com) i found"
        result = extract_markdown_images(text)
        assert len(result) == 2
        assert result[0][0] == "random image"
        assert result[0][1] == "https://doesntexist.com"
        assert result[1][0] == "another random image"
        assert result[1][1] == "https://doesntexist2.com"

        text = "This is sentence has a [random link](https://doesntexist.com) so it shouldnt not return anything."
        result = extract_markdown_images(text)
        assert len(result) == 0

        text = "This is sentence has a [random link](https://doesntexist.com) but also a ![random image](https://doesntexist.com) and both have the same link"
        result = extract_markdown_images(text)
        assert len(result) == 1

        text = "This is sentence has a ![random image with a few numb3r5](https://doesntexist.com) so it should return something"
        result = extract_markdown_images(text)
        assert len(result) == 1

        text = "This is sentence has a !]broken image](https://doesntexist.com) so it shouldnt not return anything."
        result = extract_markdown_images(text)
        assert len(result) == 0

        text = "This is sentence has a ![broken image])https://doesntexist.com) so it shouldnt not return anything."
        result = extract_markdown_images(text)
        assert len(result) == 0

    def test_link_extractor(self):
        text = "This is a [random link](https://doesntexist.com) i found"
        result = extract_markdown_links(text)
        assert len(result) == 1
        assert result[0][0] == "random link"
        assert result[0][1] == "https://doesntexist.com"
        
        text = "This is a [random link](https://doesntexist.com) and [another random link](https://doesntexist2.com) i found"
        result = extract_markdown_links(text)
        assert len(result) == 2
        assert result[0][0] == "random link"
        assert result[0][1] == "https://doesntexist.com"
        assert result[1][0] == "another random link"
        assert result[1][1] == "https://doesntexist2.com"

        text = "This is sentence has a ![random image](https://doesntexist.com) so it shouldnt not return anything."
        result = extract_markdown_links(text)
        assert len(result) == 0

        text = "This is sentence has a [random link](https://doesntexist.com) but also a ![random image](https://doesntexist.com) and both have the same link"
        result = extract_markdown_links(text)
        assert len(result) == 1

        text = "This is sentence has a [random link with a few numb3r5](https://doesntexist.com) so it should return something"
        result = extract_markdown_links(text)
        assert len(result) == 1

        text = "This is sentence has a ]broke link](https://doesntexist.com) so it shouldnt return anything"
        result = extract_markdown_links(text)
        assert len(result) == 0

        text = "This is sentence has a [broke link])https://doesntexist.com) so it shouldnt return anything"
        result = extract_markdown_links(text)
        assert len(result) == 0
    
    def test_link_splitter(self):
        text = "This is a [random link](https://doesntexist.com) i found"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 3
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.LINK
        assert result[2].text_type == TextType.TEXT

        text = "This is a [random link](https://doesntexist.com) and [another random link](https://doesntexist2.com) i found"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 5
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.LINK
        assert result[2].text_type == TextType.TEXT
        assert result[3].text_type == TextType.LINK
        assert result[4].text_type == TextType.TEXT

        text = "This is sentence has a [random link](https://doesntexist.com) but also a ![random image](https://doesntexist.com) and both have the same link"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 3
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.LINK
        assert result[2].text_type == TextType.TEXT
        
        text = "This is sentence has a ]broke link](https://doesntexist.com) so it shouldnt return anything"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 1
        assert result[0].text_type == TextType.TEXT

        text = "This is sentence has a not links so it shouldnt return anything"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 1
        assert result[0].text_type == TextType.TEXT

        text = "[random link](https://doesntexist.com) This sentence starts with a link and has a [random link](https://doesntexist.com) but also a ![random image](https://doesntexist.com) and both have the same link"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 4
        assert result[0].text_type == TextType.LINK
        assert result[1].text_type == TextType.TEXT
        assert result[2].text_type == TextType.LINK
        assert result[3].text_type == TextType.TEXT

        text = "This sentence has two back to back links, [random link](https://doesntexist.com) [random link](https://doesntexist.com) but also a ![random image](https://doesntexist.com) and both have the same link"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_link([node])
        assert len(result) == 4
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.LINK
        assert result[2].text_type == TextType.LINK
        assert result[3].text_type == TextType.TEXT
        
        
