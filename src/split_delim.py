from textnode import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            edit = node.text.replace(delimiter, "")
            new_nodes.append(TextNode(edit, node.text_type))
        else:
            remaining_text = node.text
            while remaining_text:
                first_delim = remaining_text.find(delimiter)

                if first_delim == -1:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                    break
                else:

                    edit = remaining_text[first_delim + len(delimiter):]
                    second_delim = edit.find(delimiter)

                    if second_delim == 0:
                        raise Exception(f'"{delimiter}" delimiter came too soon in {node}')

                    if second_delim == -1:
                        raise Exception (f'"{delimiter}" delimiter not found in {node}')

                    mid = edit[:second_delim]

                    if not mid.strip():
                        raise Exception("Empty content between delimiters")

                    before = remaining_text[:first_delim] 
                    after = edit[second_delim + len(delimiter):]

                    if len(before) > 0:
                        new_nodes.append(TextNode(before, TextType.TEXT))

                    new_nodes.append(TextNode(mid, text_type))
                    remaining_text = after
    return new_nodes




