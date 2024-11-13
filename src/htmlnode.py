from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # string
        self.value = value # string
        self.children = children if children is not None else []# list
        self.props = props if props is not None else {} # dict

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""

        prop_string = ""
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"'
        return prop_string
    
    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and 
            self.children == other.children and
            self.props == other.props 
        )
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag} value={self.value} children={self.children} props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        SELF_CLOSING_TAGS = ["img", "br", "hr", "input", "link", "meta"]

        if self.value == None:
            raise ValueError ("Leaf nodes need value")
        
        if self.tag == None:
            return self.value
        
        if self.tag in SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()}/>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self):
        if self.tag == None:
            raise ValueError ("Tag is empty")

        if self.children == None or len(self.children) == 0:
            raise ValueError ("Can't be parent with no children")

        child_string = ""
        for child in self.children:
            child_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"

def text_node_to_html(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url , "alt": text_node.text })
        case _:
            raise Exception ("not valid text node")
        
        