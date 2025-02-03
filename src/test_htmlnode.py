import unittest
from htmlnode import HTMLNode, LeafNode, HTMLNodeType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        
        # no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
        # node with one prop
        node = HTMLNode(
            tag=HTMLNodeType.LINK,
            value="Example",
            children=[],
            props={
                "href": "https://example.com"
            }
        )
        
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
        # node with multiple props
        node = HTMLNode(
            tag=HTMLNodeType.LINK,
            value="Example",
            children=[],
            props={
                "href": "https://example.com",
                "class": "some-css-classname",
                "target": "_blank"
            }
        )
        
        self.assertEqual(node.props_to_html(), ' href="https://example.com" class="some-css-classname" target="_blank"')
        
    def test_leaf_to_html(self):
        node = LeafNode(HTMLNodeType.PTEXT, "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        
        node = LeafNode(HTMLNodeType.LINK, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
        
