#!/bin/python3

# Import modules
import re
from pathlib import Path

# Set target directory
src_dir = "/home/sociodicy/imagined_realities/content/blog/"


def find_images(file_variable):
    files = Path(file_variable).glob("*")
    for filename in files:
        with open(filename, "r+", encoding="utf-8") as blogpost:
            md = blogpost.read()
            md = re.sub(
                r"!\[.*?\]\(\/assets\/img\/(.*\.png|.*\.JPG|.*\.jpg)\)",
                r"{% imagesmall '/img/\g<1>', '' %}",
                md,
            )
            blogpost.seek(0)
            blogpost.write(md)

    return print("Text replaced")


find_images(src_dir)
