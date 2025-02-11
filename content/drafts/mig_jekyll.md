---
title: Migrating Posts to 11ty with Python
date: 
draft: true
tags:
  - jekyll
  - python
  - 11ty
---

#### Overview in Brief
- {% linkprimary "Migrating Jekyll Posts", "https://christopherbauer.org/blog/mig_jekyll/#Migrating-Jekyll-Posts" %}


### Migrating Jekyll Posts
I recently recreated my website using 11ty and ran into a few challenges transitioning my posts from Jekyll.  Before I dig into those, allow me to recap my reasons for switching.  My realization came when I upgraded my home machine and had to install backports on Debian to obtain a load of outdated software and dependencies to recreate the local build flow.  Just getting Jekyll to simply build required so much that wasn't well maintained anymore.  Also, I never got ruby.  I'm not throwing shade, I just don't run into ruby all that much outside of Jekyll.  Lastly, when I started experimenting, 11ty demonstrated more flexibility around markdown's hybrid forms than Jekyll did and it used npm with which I am a bit more familiar.  

One challenge with the migration was that the layout property in the frontmatter of my Jekyll formatted posts.  My new 11ty theme didn't require a layout property and the 11ty engine was utterly confused by it, so at the very least it had to come out.  I didn't want to do that manually for two dozen back-posts.

The second challenge was more formidable.  I'd been using a markdown links style of referencing local image locations. For example: `![Alt text](URL or file path)`. My new 11ty theme used a Nunjucks shortcode style.  Jekyll too offered the ability to use shortcodes in Liquid, though I always found it easier to use the markdown style.  So my posts were littered with the markdown syntax.

Rather than address my two dozen back-posts manually, this seemed like a classic example of a job for python.  I wrote up some python scripts that I'm posting here as a model for others in a similar situation.  Bear in mind that I'm self-taught in Python, so if they appear inelegant, please feel free to offer suggestions by DMing me at my {% linkprimary "Mastodon account", "https://infosec.exchange/@anthro_packets" %}.

I used these scripts on Debian Linux with Python3.11 and markdown files for the blog posts.  I strongly recommend you make copies of the files you intend to run these on before running them on your origianls to ensure that they do what you expect.


### Removing the Layout Property

First I imported the path module from pathlib in order to point the commands to a properly formatted directory location.

Then I set the source directory as a variable. I followed that with a glob search to identify the files in the source directory and to set them to a variable called "files."

Next, I created a try and except structure to resolve errors gracefully.  

I then started the proper iteration with a for statement to loop over the files variable.  For each file in the loop I next instructed python to open the file as *read*, and store that text as a variable "lines."

Once python had stored the text as lines, I coded another open method, this time as *write* for each file in the loop.  Next, I created a nested loop to iterate over the stored text in the "lines" variable.  The nested loop had a conditional method to remove any line in the stored text that matched the layout frontmatter property and its newline character.  If that condition was met the code then wrote this "new" textual arrangement to the stored text in the "lines" variable.  And with that I'd erased the frontmatter layout property in two dozen posts.

```python
#!/bin/python3

# Import modules
from pathlib import Path

# Set the source directory and find all the files within it.
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


### Rewriting Image Links
To translate the markdown image format to Nunjucks shortcode I used the same search using a glob pattern but made it into a simple function to handle the source directory as a parameter.  However to identify and change the text, I deviated and used a regex search/substitute method.  The hardest part was fine-tuning the regex to capture the entirety of the markdown link.  I learned that the regex substitution can accept regex groups, and that turned out to be pretty handy.

I started by imported the re module for regex and the Path module.

Like above, I set the working directory to a variable.  Next I created a regex pattern object that would search for the markdown syntax and set it to a variable.

I then created a function, "find_images" that accepted a parameter.  First the function would create a variable to store all the files of the source directory.  

Next I'd begin the iteration process on the files by opening each file as *read and write*, and storing that text as a variable "md."  Then for the variable "md" I ran a substitute regex.  The regex looked for the markdown syntax and a few different extensions and created a few groups.  It'd then replace the markdown syntax and using the groups, preserve the image file name within the new Nunjucks syntax.  The function then sought out the beginning of the text and wrote the changed text structure to each file.

```python
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
```


## Conclusion
You could combine the two if you so desired.