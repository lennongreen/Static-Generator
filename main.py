
from static import *
import os
import shutil

def copy_content(item_path, destination_dir):
    # check if destination exists, if not create
    if not os.path.exists(destination_dir):
        print("deleting existing path") 
        os.mkdir(destination_dir)

    #create current item path
    base_name = os.path.basename(item_path)
    print(f"base name: {base_name}")
    # Create destination to copy to 
    destination_path = os.path.join(destination_dir, base_name)
    print(f"destination_path {destination_path}")

    # Copy based on if file or directory
    if os.path.isfile(item_path):
        print(f"Copying: {item_path} to {destination_dir}")
        shutil.copy(item_path, destination_path)
    else: 

        print(f"Handling directory: {item_path} -> {destination_path}")
        # Clean up destination before copy
        if os.path.exists(destination_path) and os.path.isdir(destination_path):
            print(f"{destination_path} already existed, deleting")
            shutil.rmtree(destination_path)

        os.mkdir(destination_path)
        for sub_item in os.listdir(item_path):
            sub_path = os.path.join(item_path, sub_item)
            print(f"calling copy_content for {sub_path} and {destination_path}")
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
    
    with open(from_path, "r", )

def main():

    if not os.path.exists("static"):
        print("Source directory does not exist.") 
        return

    for item in os.listdir("static"):
        item_path = os.path.join("static", item)
        print(f"Processing item: {item_path}")
        copy_content(item_path, "public")


if __name__ == "__main__":
    main()