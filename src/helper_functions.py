from textnode import TextNode, TextType
import re
from htmlnode import LeafNode
from typing import List, Tuple

def text_node_to_html_node(text_node: TextNode ):
    """
        Takes a `TextNode` and converts it into an HTMLNode.

        Args:
        `text_node: TextNode` => a textnode that you want converted
        
        Returns:
        `HTMLNode`
    """
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
    """
        Takes a list of `TextNode`s and seperates them based on a defined delimiter

        Args:
        `old_nodes: List[TextNode]` => a list of nodes that you want seperated
        `delimiter: str` => a delimiter that you want to use for seperation
        `text_type: TextType` => the type of the text that isnt surrounded by the delimiter
        
        Returns:
        `List[TextNode]`
    """
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

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
        Takes text formatted in Markdown and extracts images from it and returns them in a list of tuples
        
        Args:
        `text: str` => a string of text formatted in markdown

        Returns:
        `List[Tuple[alt_text, link_to_image]]`
    """
    
    alt_text_pattern = r"\!\[(.*?)\]"
    link_pattern = r"\!\[[\s\w\d]*\]\((.*?)\)"
    
    alt_text_list = re.findall(alt_text_pattern, text)
    link_list = re.findall(link_pattern, text)
    
    return list(zip(alt_text_list, link_list))

def extract_markdown_links(text):
    """
        Takes text formatted in Markdown and extracts links from it and returns them in a list of tuples
        
        Args:
        `text: str` => a string of text formatted in markdown

        Returns:
        `List[Tuple[text, link]]`
    """
    
    text_pattern = r"[^\!]\[(.*?)\]"
    link_pattern = r"\[[\s\w\d]*\]\((.*?)\)"

    text_list = re.findall(text_pattern, text)
    link_list = re.findall(link_pattern, text)
    
    return list(zip(text_list, link_list))