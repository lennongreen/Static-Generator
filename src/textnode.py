from enum import Enum

class NodeType(Enum):
    HTML = "html"
    LEAF = "leaf"
    TEXT = "text"

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text ,text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (
            self.text_type == value.text_type and
            self.url == value.url and 
            self.text == value.text
        )

    def __repr__(self):
        return f"TextNode({self.text} {self.text_type} {self.url})"
