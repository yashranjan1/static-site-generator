import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        
        # no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
        # node with one prop
        node = HTMLNode(
            tag="a",
            value="Example",
            children=[],
            props={
                "href": "https://example.com"
            }
        )
        
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
        # node with multiple props
        node = HTMLNode(
            tag="a",
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
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
        node = LeafNode(None, "This is just some random text.")
        self.assertEqual(node.to_html(), "This is just some random text.")
    
    def test_parent_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        
        node = ParentNode(
            "div",
            [
                LeafNode("b", "This is a bold leaf node"),
                ParentNode(
                    "div",
                    [
                        LeafNode("i", "This is an italics leaf node"),
                    ],
                    {
                        "class": "flex gap-2"
                    }
                )
            ],
            {
                "class": "flex flex-col gap-5"
            }
        )
        
        self.assertEqual(node.to_html(), '<div class="flex flex-col gap-5"><b>This is a bold leaf node</b><div class="flex gap-2"><i>This is an italics leaf node</i></div></div>')
        
        node = ParentNode(
            "div",
            [],
            {
                "id": "empty-div"
            }
        )
        self.assertEqual(node.to_html(), '<div id="empty-div"></div>')
        
        # ignoring the below checks because they are supposed to fail
        node = ParentNode(
            "div",
            None, # type: ignore
        )
        
        with self.assertRaises(ValueError):
            node.to_html()           
        
        node = ParentNode(
            None, # type: ignore
            [
                LeafNode("b", "This is a bold leaf node"),
            ],
        )
        
        with self.assertRaises(ValueError):
            node.to_html()           