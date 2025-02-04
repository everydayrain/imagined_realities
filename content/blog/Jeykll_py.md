---
title: 
date: 
draft: true
tags:
  - jekyll
  - python
  - 11ty
---

## 
I ran into a few challenges migrating from Jekyll to 11ty.

One challenge I ran into transitioning my posts from Jekyll was the Layout property in the frontmatter.  My 11ty theme didn't require a layout property and was confused by it, so at the very least it had to come out.

I'm posting these as a model.  Bear in mind that I'm self-taught in Python, so if they appear inelegant, please feel free to offer suggestions by DMing me at my {% linkprimary "Mastodon account", "https://infosec.exchange/@anthro_packets" %}.

I used these on Debian Linux with Python3.11


You could combine the two if you so desired.

I strongly recommend you make copies of the files you intend to run these on before running them on your final.

## Removing the Layout Property


First we import the path module from pathlib in order to have clean directory pointers.

Then I set the source directory as a variable and follow that with a variable that searches the source directory for all files.

Next I 
```python
#!/bin/python3

# Import modules
from pathlib import Path

src_dir = Path("/home/sociodicy/imagined_realities/content/blog/")
files = src_dir.glob("*")

## Find the frontmatter category "layout" and delete it.
try:
    for search in files:
        with open(search, "r") as fileread:
            lines = fileread.readlines()

            with open(search, "w") as filewrite:
                for line in lines:

                    # strip() is used to remove '\n'
                    # present at the end of each line
                    if line.strip("\n") != "layout: post":
                        filewrite.write(line)
except:
    print("Oops! Something went wrong.")
```


## 
```python
#!/bin/python3

# Import modules
import re
from pathlib import Path

# Set target directory
# src_dir = "/home/sociodicy/scripts/python/website_migration/test/"
src_dir = "/home/sociodicy/imagined_realities/content/blog/"

# Create a regex to identify the wikilinks image syntax
identify_image = re.compile(
    r"(!\[.*?\]\(\/assets\/img\/)(.*\.png|.*\.jpeg|.*\.jpg)(\))",
    re.I,
)


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
            # blogpost.truncate()

    return "Text replaced"


find_images(src_dir)
```