from textnode import TextNode, TextType
from htmlnode import LeafNode
from typing import List

def text_node_to_html_node(text_node: TextNode ):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("invalid type")
        
def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        node_text = node.text.split(delimiter)
        for i in range(len(node_text)):
            if len(node_text[i]) == 0:
                continue
            if i % 2 == 0:
                new_node = TextNode(node_text[i], node.text_type)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(node_text[i], text_type)
                new_nodes.append(new_node)
    return new_nodes
