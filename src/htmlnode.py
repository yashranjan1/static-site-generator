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
        if (tag != None): self.tag = tag.value
        else: self.tag = tag
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
            props += f' {prop}="{self.props[prop]}"'

        
        return props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
        Class used to create HTML Leaf node objects

        Args:
            - `tag: HTMLNodeType` => The type of tag, eg `a`, `h1`
            - `value: str` => The contents of the node
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
            props += f' {prop}="{self.props[prop]}"'

        
        return props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)
        
    def to_html(self):
        if (self.value == None):
            raise ValueError("leaf nodes require a value")
        if (self.tag == None):
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)
        
    def to_html(self):
        if (self.value == None):
            raise ValueError("leaf nodes require a value")
        if (self.tag == None):
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"