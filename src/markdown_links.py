import re
from .textnode import *
from .split_delim import *

def extract_markdown_images(text):
    # Check for image with no link
    if re.search(r"!\[([^\[\]]*)\](?!\()", text):
        raise Exception("missing image link attribute")
    
    # Check (empty alt, empty url) and (empty alt, with URL)
    if re.search(r"!\[\]\([^\(\)]*\)", text):
        raise Exception("missing image alt attribute")
    
    # Check for partial parentheses
    if re.search(r"!\[([^\[\]]*)\]\((?![^\(\)]+\))", text):
        raise Exception("open parentheses after image alt")
    
    # Check for open square Brackets
    if text.count('[') != text.count(']'):
        raise Exception("mismatched square brackets")
    
    # If all validation passes, proceed with your existing pattern
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    # Check for link with no URL
    if re.search(r"\[([^\[\]]+)\](?!\()", text):
        raise Exception("missing link url attribute")
    
    # Check for link with no text (both empty URL and with URL)
    if re.search(r"\[\]\([^\(\)]*\)", text):
        raise Exception("missing link text attribute")
        
    # Check for partial parentheses
    if re.search(r"\[([^\[\]]+)\]\((?![^\(\)]+\))", text):
        raise Exception("open parentheses after link text")
    
    # Check for open square Brackets
    if text.count('[') != text.count(']'):
        raise Exception("mismatched square brackets")

    # If all validation passes, proceed with your existing pattern
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    final_list = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue

        text = node.text    
        image_sections = extract_markdown_images(text)
        

        if not image_sections:
            final_list.append(TextNode(text, TextType.TEXT))
            continue
        
        remaining_text = text
        for image in image_sections:
            image_alt, image_link = image
                
            image_section, remaining_text = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if image_section:
                final_list.append(TextNode(image_section, TextType.TEXT))
            
            final_list.append(TextNode(image_alt, TextType.IMAGE, image_link))

        if remaining_text:
            final_list.append(TextNode(remaining_text, TextType.TEXT))

    return final_list

def split_nodes_link(old_nodes):
    final_list = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue

        text = node.text
        link_sections = extract_markdown_links(text)
        remaining_text = text

        if not link_sections:
            final_list.append(TextNode(text, TextType.TEXT))
            continue

        for link in link_sections:
            link_text, link_url = link

            text_section, remaining_text = remaining_text.split(f"[{link_text}]({link_url})", 1)

            if text_section:
                final_list.append(TextNode(text_section, TextType.TEXT))

            final_list.append(TextNode(link_text, TextType.LINK, link_url))

        if remaining_text:
            final_list.append(TextNode(remaining_text, TextType.TEXT))

    return final_list


