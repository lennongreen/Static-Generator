from markdown_links import *
from split_delim import *
from textnode import *

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    #print("After initial:", nodes)

    nodes = split_nodes_image(nodes)
    #print("After image:", nodes)

    nodes = split_nodes_link(nodes)
    #print("After link:", nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    #print("After bold:", nodes)

    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    #print("After italic:", nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    #print("After code:", nodes)

    return nodes
