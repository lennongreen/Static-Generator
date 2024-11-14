from static import *
import os
import shutil
from src.markdown_to_html import *
from src.htmlnode import *

def copy_content(item_path, destination_dir):
    # check if destination exists, if not create
    if not os.path.exists(destination_dir): 
        os.mkdir(destination_dir)

    #create current item path
    base_name = os.path.basename(item_path)

    # Create destination to copy to 
    destination_path = os.path.join(destination_dir, base_name)

    # Copy based on if file or directory
    if os.path.isfile(item_path):
        shutil.copy(item_path, destination_path)
    else: 
        # Clean up destination before copy
        if os.path.exists(destination_path) and os.path.isdir(destination_path):
            shutil.rmtree(destination_path)

        os.mkdir(destination_path)
        for sub_item in os.listdir(item_path):
            sub_path = os.path.join(item_path, sub_item)
            copy_content(sub_path, destination_path)
        

def extract_title(markdown):
    # pull h1 header from mamrkdown file
    # if no h1 raise exception
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception ("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    #base_name = os.path.basename(from_path)
    #base_name_new = base_name.replace(".md", ".html")
    #from_path = from_path.replace(base_name, base_name_new)

    with open(from_path, "r", encoding="utf-8") as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r", encoding="utf-8") as template_path_file:
        template_content = template_path_file.read()
    
    html_node = markdown_to_html_node(markdown_content)
    markdown_html = html_node.to_html()
    title = extract_title(markdown_content)

    content = template_content.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", markdown_html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(content)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):

    dir_list = os.listdir(dir_path_content)

    for file in dir_list:

        full_path = os.path.join(dir_path_content , file)
        base_name = os.path.basename(full_path)
        destination_path = os.path.join(dest_dir_path, base_name)

        if os.path.isfile(full_path):
            if base_name.endswith(".md"):
                print(f"passing {full_path} as file")
                destination_path = destination_path.replace(".md", ".html")
                generate_page(full_path, template_path, destination_path)
        elif os.path.isdir(full_path):
            if not os.path.exists(destination_path):
                os.makedirs(destination_path, exist_ok=True)
            generate_page_recursive(full_path, template_path, destination_path)
          


def main():

    if not os.path.exists("static"):
        print("Source directory does not exist.") 
        return

    for item in os.listdir("static"):
        item_path = os.path.join("static", item)
        copy_content(item_path, "public")

    generate_page_recursive("content", "template.html", "public")
    print(f"Page generated at public")


if __name__ == "__main__":
    main()