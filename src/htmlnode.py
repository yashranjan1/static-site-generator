from enum import Enum

class HTMLNodeType(Enum):
    LINK = "a"
    PTEXT = "p"
    HEADER1 = "h1"
    IMAGE = "img"
    CODE = "code"
    BOLD = "b"
    ITALICS = "i"

class HTMLNode():
    """
        Class used to create HTML node objects

        Args:
            - `tag: HTMLNodeType` => The type of tag, eg `a`, `h1`
            - `value: str` => The contents of the node
            - `children: HTMLNode[]` => An array of HTMLNode containing child nodes of this node
            - `props: { key: value }` => A dict containing key value pairs, where keys are the attributes that the html node can take and the values are the values of those attributes
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("still needs an implementation")
    
    def props_to_html(self):
        
        if self.props == None:
            return ""

        props = ""

        for prop in self.props:
            props += f'{prop}="{self.props[prop]}" '

        
        return props[:-1]
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"