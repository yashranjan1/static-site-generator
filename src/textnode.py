from enum import Enum
from typing import Optional, Any

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    """
        Used for setting up an HTML text node.

        Args:
            text: `string` => The string content of the TextNode
            text_type: `TextType` => The type of content the node represent, should use a type available in the `TextType` enum
            url (optional): `string` => URL for cases where the element needs a url (links or images)
    """
    def __init__(self, text: str, text_type: TextType, url: Optional[str]=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_node: Any) -> bool:
        if not isinstance(other_node, TextNode):
            return False
        if (other_node.text == self.text and other_node.text_type == self.text_type and other_node.url == self.url):
           return True
        return False 
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
