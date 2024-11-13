from htmlnode import *
from text_to_textnode import *
from textnode import *

def text_to_tag(text, is_child=False):

    match text:
        case "heading 1":
            return "h1"
        case "heading 2":
            return "h2"        
        case "heading 3":
            return "h3"        
        case "heading 4":
            return "h4"        
        case "heading 5":
            return "h5"       
        case "heading 6":
            return "h6"
        
        case "code":
            return "pre"

        case "quote":
            return "blockquote"

        case "unordered_list" | "ordered_list":
            if is_child:
                return "li"
            return "ul" if text == "unordered_list" else "ol"
    
        case _:
            return "p"

def markdown_to_leafnodes(text):

    leaf_list = []
    for node in text_to_textnodes(text):
        leaf_list.append(text_node_to_html(node))
    return leaf_list


def trim_blocks(block, tag):

    if tag == "ul" or tag == "ol":
        temp_list = block.split("\n")
        trimmed_block = []

        for item in temp_list:
            if tag == "ul":
                item = item[2:]
            else:
                item = item[item.find(' ') + 1:]
            trimmed_block.append(item)
        return "\n".join(trimmed_block)
    
    elif re.match(r"h[1-6]", tag):
        return block[int(tag[1]) + 1:]
    elif tag == "blockquote":
        return block[2:]
    elif tag == "pre":
        return block[3:-3]
    else:
        return block
    

def create_child_list(custom_list, parent_block_type):

    children_list = []
    for item in custom_list:
        children_list.append(ParentNode(text_to_tag(parent_block_type, True), markdown_to_leafnodes(item)))
    return children_list

def markdown_to_html_node(markdown):
    # split markdown into blocks using markdown_to_blocks
    blocks = markdown_to_block(markdown)

    grand_parent = ParentNode("div", [])

    # loop over each block child
    for block in blocks:
        # determine type using block to block_type
        block_type = block_to_block_type(block)
        tag = text_to_tag(block_type)

        # Trim off block keys
        trimmed_block = trim_blocks(block.strip(), tag)

        # create HtmlNode with proper type and data
        if block_type == "unordered_list" or block_type == "ordered_list":
            temp_list = trimmed_block.split("\n")
            child = ParentNode(tag, create_child_list(temp_list, block_type))
        elif block_type == "code":
            child = ParentNode(tag ,[ParentNode("code", markdown_to_leafnodes(trimmed_block))])
        else: 
            child = ParentNode(tag, markdown_to_leafnodes(trimmed_block))
        
        # Assign proper child HTMLNode objects to block node
        grand_parent.children.append(child)

    # make sure all block nodes children are under a single parent HTML node (should be div) and return it
    return grand_parent