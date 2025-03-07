from helper_functions import *
from typing import List
import unittest
from textnode import TextNode, TextType

class TestHelperFuntions(unittest.TestCase):
    def test_conversion_function(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node: LeafNode = text_node_to_html_node(text_node)
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

        node = TextNode("This text has some _italics text_ in it.", TextType.TEXT)
        node2 = TextNode("This text has some _more italics text_ in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node, node2], "_", TextType.ITALIC) 
        assert len(new_nodes) == 6
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text_type == TextType.ITALIC
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text_type == TextType.TEXT
        assert new_nodes[4].text_type == TextType.ITALIC
        assert new_nodes[5].text_type == TextType.TEXT

        node = TextNode("This text has no delimiters in it.", TextType.TEXT)
        new_nodes: List[TextNode] = split_nodes_delimiter([node], "_", TextType.ITALIC) 
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
        
    def test_image_splitter(self):
        text = "This is a ![random image](https://doesntexist.com) i found"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 3
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.IMAGE
        assert result[2].text_type == TextType.TEXT

        text = "This is a ![random image](https://doesntexist.com) and ![another random image](https://doesntexist2.com) i found"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 5
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.IMAGE
        assert result[1].url != None
        assert result[2].text_type == TextType.TEXT
        assert result[3].text_type == TextType.IMAGE
        assert result[4].text_type == TextType.TEXT

        text = "This is sentence has a ![random image](https://doesntexist.com) but also a [random link](https://doesntexist.com) and both have the same link"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 3
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.IMAGE
        assert result[2].text_type == TextType.TEXT
        
        text = "This is sentence has a !]broke image](https://doesntexist.com) so it shouldnt return anything"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 1
        assert result[0].text_type == TextType.TEXT

        text = "This is sentence has a not links so it shouldnt return anything"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 1
        assert result[0].text_type == TextType.TEXT

        text = "![random image](https://doesntexist.com) This sentence starts with a link and has a ![random image](https://doesntexist.com) but also a [random link](https://doesntexist.com) and all have the same link"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 4
        assert result[0].text_type == TextType.IMAGE
        assert result[1].text_type == TextType.TEXT
        assert result[2].text_type == TextType.IMAGE
        assert result[3].text_type == TextType.TEXT

        text = "This sentence has two back to back images, ![random image](https://doesntexist.com) ![random image](https://doesntexist.com) but also a [random link](https://doesntexist.com) and all have the same link"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_image([node])
        assert len(result) == 4
        assert result[0].text_type == TextType.TEXT
        assert result[1].text_type == TextType.IMAGE
        assert result[2].text_type == TextType.IMAGE
        assert result[3].text_type == TextType.TEXT

    def test_text_to_textnodes(self):
        # Basic cases
        assert text_to_textnodes("Plain text") == [
            TextNode("Plain text", TextType.TEXT)
        ]

        assert text_to_textnodes("**Bold text**") == [
            TextNode("Bold text", TextType.BOLD)
        ]

        assert text_to_textnodes("_Italic text_") == [
            TextNode("Italic text", TextType.ITALIC)
        ]

        assert text_to_textnodes("`Code text`") == [
            TextNode("Code text", TextType.CODE)
        ]

        assert text_to_textnodes("[Link](https://boot.dev)") == [
            TextNode("Link", TextType.LINK, "https://boot.dev")
        ]

        assert text_to_textnodes("![Image](image.jpg)") == [
            TextNode("Image", TextType.IMAGE, "image.jpg")
        ]

        nodes = text_to_textnodes("Text with [link](url) and ![image](img.jpg)")
        assert len(nodes) == 4
        assert nodes[0] == TextNode("Text with ", TextType.TEXT)
        assert nodes[1] == TextNode("link", TextType.LINK, "url")
        assert nodes[2] == TextNode(" and ", TextType.TEXT)
        assert nodes[3] == TextNode("image", TextType.IMAGE, "img.jpg")

    
        nodes = text_to_textnodes("** **")
        assert len(nodes) == 1
        assert nodes[0] == TextNode(" ", TextType.BOLD)

        nodes = text_to_textnodes("**Bold** **More Bold**")
        assert len(nodes) == 3
        assert nodes[0] == TextNode("Bold", TextType.BOLD)
        assert nodes[1] == TextNode(" ", TextType.TEXT)
        assert nodes[2] == TextNode("More Bold", TextType.BOLD)
    
    def test_md_to_block(self):
        test = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        
        result = markdown_to_blocks(test)

        assert len(result) == 3
        

        test = """       # This is a heading


         This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


     * This is the first list item in a list block      
  * This is a list item        
    * This is another list item"""

        assert len(result) == 3
        for block in result:
            assert block[0] != " "


    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

