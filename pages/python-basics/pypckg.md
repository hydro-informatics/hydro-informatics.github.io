---
title: Python Basics - Packages
keywords: git
sidebar: mydoc_sidebar
permalink: hypy_pckg.html
folder: python-basics
---

## Import packages

Importing a package in *Python* makes external functions and other elements (such as objects) of modules accessible in a script. The functions and other elements are stored within another *Python* file (`.py`) in some */site_packages/* folder of the interpreter environments. Thus, in order to use a non-standard package, it needs to be downloaded and installed first. Standard packages (e.g., `os`, `math`) are always accessible and other can be added with *conda* ([read the installation instructions](hypy_install.html#install-pckg)).

The `os` package provides some useful system-terminal like commands, for example, to manage folder directories. So let's import this essential package.



```python
import os
print(os.getcwd()) # print current working directory

```

    \...\jupyter\hypy
    
