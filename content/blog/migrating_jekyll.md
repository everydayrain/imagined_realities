---
title: Migrating Posts from Jekyll to 11ty with Python
date: 2025-02-12
tags:
 - jekyll
 - python
 - 11ty
---

#### Overview in Brief
- {% linkprimary "Rationale for Switching", "https://christopherbauer.xyz/blog/migrating_jekyll/#rationale-for-switching" %}
- {% linkprimary "Migrating Jekyll Posts", "https://christopherbauer.xyz/blog/migrating_jekyll/#migrating-jekyll-posts" %}
- {% linkprimary "Removing the Layout Property", "https://christopherbauer.xyz/blog/migrating_jekyll/#removing-the-layout-property" %}
- {% linkprimary "Rewriting Image Links", "https://christopherbauer.xyz/blog/migrating_jekyll/#rewriting-image-links" %}
- {% linkprimary "Rewriting Self-Referring Links", "https://christopherbauer.xyz/blog/migrating_jekyll/#rewriting-self-referring-links" %}


### Rationale for Switching
I recently recreated my website using 11ty and ran into a few challenges transitioning my posts from Jekyll. Before I dig into how I solved them, allow me to recap my reasons for switching. 

I'd used Jekyll since 2020 and while there was a learning curve, Jekyll treated me well for the most part. My realization that I needed to make a change came when I recently upgraded my home machine. I had to install backports on Debian to obtain a load of outdated software and dependencies to just to recreate the simple local Jekyll build flow. That the primary task of a static site generator required so much that wasn't well maintained anymore was a sign that was hard to miss.

There were other ongoing issues as well. I never got ruby. I'm not throwing shade, I just never ran into ruby all that much outside of Jekyll. Then, when I started experimenting with 11ty, it's static site generator used npm with which I am a bit more familiar.  At that point I was sold and ready to make my first steps toward migration.

### Migrating Jekyll Posts
One challenge with the migration was the layout property in the frontmatter of my Jekyll formatted posts. My new 11ty theme didn't require a layout property and the engine was utterly confused by it at build, so it had to come out. I didn't want to do that manually for two dozen back-posts.

The second challenge seemed more formidable but turned out to be a regex problem. I'd been using a markdown links style of referencing local image locations. For example: `![Alt text](URL or file path)`. My new 11ty theme used a Nunjucks shortcode style (e.g. in squiggly brackets something like: % "image caption", "image link" %). Jekyll did offer the ability to use shortcodes in Liquid, though I always found it easier to use the markdown style. So my posts were littered with the markdown syntax. Another issue I didn't want to deal with manually for my back-posts.

Then there was the third problem of the format of self-referring links. Links embedded in my markdown text pointing to my own blog had a date format using forward slashes (e.g. year/month/day). The theme I'm using for 11ty paginates the blog posts using dashes (e.g. year-month-day). In other words, all the links on my blog pointing to my own blog posts were broken. So I would have to alter those to ensure the links referred to posts that actually exist by changing the date format while leaving the rest of the link intact.

Rather than address my two dozen back-posts manually, these issues seemed like python's bread and butter. I wrote up some python scripts that I'm posting here as a model for others in a similar situation. Bear in mind that I'm self-taught in Python, so if they appear inelegant, or I use inappropriate code, please feel free to offer suggestions by DMing me at my {% linkprimary "Mastodon account", "https://infosec.exchange/@anthro_packets" %}. The scripts appear here separately as I assume readers will not uniformly have the same requirements as I do and might wish to select them individually.

I used these scripts on Debian Linux with Python3.11 and markdown files for the blog posts. I strongly recommend you make copies of the markdown files you intend to run these on before for testing to ensure that they do what you expect.

### Removing the Layout Property

First I imported the path module from pathlib in order to point the commands to a properly formatted directory location.

Then I set the source directory as a variable. I followed that with a glob search to identify the files in the source directory and to set them to a variable called "files."

Next, I created a try and except structure to resolve errors gracefully. 

I then started the proper iteration with a for statement to loop over the files variable. For each file in the loop I next instructed python to open the file as *read*, and store that text as a variable "lines."

Once python had stored the text as lines, I coded another open method, this time as *write* for each file in the loop. Next, I created a nested loop to iterate over the stored text in the "lines" variable. The nested loop had a conditional method to remove any line in the stored text that matched the layout frontmatter property and its newline character. If that condition was met the code then wrote this "new" textual arrangement to the stored text in the "lines" variable. And with that I'd erased the frontmatter layout property in two dozen posts.

```python
#!/bin/python3

# Import modules
from pathlib import Path

# Set the source directory and find all the files within it.
src_dir = Path("/home/directory/of/your/blog/")
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


### Rewriting Image Links
To translate the markdown image format to Nunjucks shortcode I used the same search using a glob pattern but made it into a simple function to handle the source directory as a parameter. However to identify and change the text, I deviated and used a regex search/substitute method. The hardest part was fine-tuning the regex to capture the entirety of the markdown link. I learned that the regex substitution can accept regex groups, and that turned out to be pretty handy.

I started by importing the re module for regex and the Path module.

Like above, I set the working directory to a variable. 

I then created a function, "find_images" that accepted a parameter. First the function would create a variable to store all the files of the source directory. 

Next I wrote the iteration process on the files by opening each file as *read and write*, and storing that text as a variable "md." Then for the variable "md" I ran a substitute regex. The regex looked for the markdown syntax and a few different extensions and created a few groups. It'd then replace the markdown syntax and using the groups and preserve the image file name within the new Nunjucks syntax. The function then sought out the beginning of the text and wrote the changed text structure to each file.

```python
#!/bin/python3

# Import modules
import re
from pathlib import Path

# Set target directory
src_dir = "/home/directory/of/your/blog/"

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
```


### Rewriting Self-Referring Links
This script is virtually the same as the one above, it just uses a different regex to isolate links referring to https://christopherbauer.xyz and substitute the date format from forward slashes to dashes using groups. It has different variable names for the loops as well.

```python
#!/bin/python3

# Import modules
import re
from pathlib import Path

# Set target directory
src_dir = "/home/directory/of/your/blog/"


def find_images(file_variable):
  files = Path(file_variable).glob("*")
  for filename in files:
    with open(filename, "r+", encoding="utf-8") as blogpost:
      link = blogpost.read()
      link = re.sub(
        r"https\:\/\/christopherbauer\.org\/(\d{4})\/(\d{2})\/(\d{2})\/(\w.*)\.html",
        r"https://christopherbauer.xyz/blog/\1-\2-\3-\4",
        link,
      )
      blogpost.seek(0)
      blogpost.write(link)

  return print("Text replaced")


find_images(src_dir)
```

## Conclusion
I bet that these scripts won't be immediately useful to everyone transitioning from Jekyll to 11ty, given the idiosyncrasies of constructing static websites. Even websites with popular generators such as Jekyll vary quite a bit given theming and other custom configurations going on under the hood. Nevertheless, I hope these scripts will be useful.  Even if readers don't use them line for line, they can serve as inspiration for other bloggers to modify their posts and ease the transition process. 

Happy blogging!