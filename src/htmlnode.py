from typing import Optional, List, Dict

class HTMLNode():
    """
        Class used to create HTML node objects

        Args:
            - `tag : HTMLNodeType` => The type of tag, eg `a`, `h1`
            - `value : str` => The contents of the node
            - `children : HTMLNode[]` => An array of HTMLNode containing child nodes of this node
            - `props : { key: value }` => A dict containing key value pairs, where keys are the attributes that the html node can take and the values are the values of those attributes
    """
    def __init__(self, tag:Optional[str]=None, value: Optional[str]=None, children: Optional[List["HTMLNode"]]=None, props: Optional[Dict[str, str]]=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError("still needs an implementation")
    
    def props_to_html(self) -> str:
        
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
    def __init__(self, tag: Optional[str]=None, value: Optional[str]=None, props: Optional[Dict[str, str]]=None):
        self.tag = tag
        self.value = value
        self.children = None
        self.props = props
    
    def to_html(self) -> str:
        if (self.value == None):
            raise ValueError("leaf nodes require a value")
        if (self.tag == None):
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        
        if self.props == None:
            return ""

        props = ""

        for prop in self.props:
            props += f' {prop}="{self.props[prop]}"'

        
        return props
    
    def __repr__(self):
        return super().__repr__()
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, str]]=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node needs a tag")
        if self.children == None:
            raise ValueError("parent node must have children")
        children = ""
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"

    