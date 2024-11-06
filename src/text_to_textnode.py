from markdown_links import *
from split_delim import *
from textnode import *

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_block(markdown):
    lines = markdown.splitlines()
    blocks = []
    current_block = []

    for line in lines:
         # strip leading/trailing whitespace from each block
        line = line.strip()

        # Remove any "empty" blcoks due to excessive newlines
        # Add current block to blocks, reset current
        if not line:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
            continue

        # Add to current block
        current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))
        
    return blocks

def block_to_block_type(block):
    
    if re.match(r"^#{1,6} .+", block):
        return "heading"

    if re.match(r"^\`{3}[\s\S]*\`{3}$", block):
        return "code"

    lines = block.split("\n")
    is_quote = False
    is_unordered = False
    is_ordered = False

    for line in lines:
        if re.match(r"^>", line):
            is_quote = True
        else:
            is_quote = False
            break
    
    if is_quote:
        return "quote"
    
    for line in lines:
        if re.match(r"^(\*|\-) .+", line):
            is_unordered = True
        else:
            is_unordered = False
            break
    
    if is_unordered:
        return "unordered_list"
    
    past_num = "0"
    for line in lines:
        if re.match(r"^[1-9]\. .+", line) and int(line[0]) == int(past_num) + 1:
            is_ordered = True
            past_num = line[0]
        else:
            is_ordered = False
            break

    if is_ordered:
        return "ordered_list"
    
    #return paragraph if nothing else was detected
    return "paragraph"
