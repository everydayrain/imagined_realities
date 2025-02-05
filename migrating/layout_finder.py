#!/bin/python3

# Import modules
from pathlib import Path

# src_dir = Path("/home/sociodicy/scripts/python/test")
src_dir = Path("/home/sociodicy/imagined_realities/content/blog/")
files = src_dir.glob("*")

## Find the frontmatter category "layout" and delete it.
try:
    for search in files:
        with open(search, "r") as fr:
            lines = fr.readlines()

            with open(search, "w") as fw:
                for line in lines:

                    # strip() is used to remove '\n'
                    # present at the end of each line
                    if line.strip("\n") != "layout: post":
                        fw.write(line)
except:
    print("Oops! Something went wrong.")
