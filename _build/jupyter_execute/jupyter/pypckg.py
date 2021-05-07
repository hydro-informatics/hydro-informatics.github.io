#!/usr/bin/env python
# coding: utf-8

# (sec-pypckg)=
# # Packages, Modules and Libraries
# 
# Summary: Import external libraries and organize your code into functional chunks.
# 
# For interactive reading [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter).
# 
# ## Import Packages or Modules
# 
# Importing a package or module in *Python* makes external functions and other elements (such as objects) of modules accessible in a script. The functions and other elements are stored within another *Python* file (`.py`) in some */site_packages/* folder of the interpreter environments. Thus, in order to use a non-standard package, it needs to be downloaded and installed first. Standard packages (e.g., `os`, `math`) are always accessible and other can be added with *conda* ([read the installation instructions](pyinstall.html#install-pckg)).
# 
# ```{note}
# There is a **difference between modules and packages**. Modules are single or multiple files that can be imported as one import (e.g., `import a_module`). Packages are a collection of modules in a directory with a defined package hierarchy, which enables the import of individual modules (e.g. `from a_package.module import a_function`). Packages are therefore also modules, but with a hierarchy definition (i.e., a `__path__` attribute and a `__init__.py` file). Sounds fuzzy? Read this page down to the bottom and come back here to re-read this note.
# ```
# 
# The `os` package provides some useful system-terminal like commands, for example, to manage folder directories. So let's import this essential package.

# In[ ]:


import os
print(os.getcwd()) # print current working directory
print(os.path.abspath('')) # print directory of script running


# ### Overview of Import Options
# 
# Here is an overview of options to import packages or modules (hierarchical parts of packages):
# 
# | Command | Description | Usage of attributes |
# |---------|-------------|---------------------|
# | `import package-name` | Import an original module | `package.item()` |
# | `import package-name as nick-name` | Import module and rename (alias) it in the script |  `nick-name.item()` |
# | `from package-name import item` | Import only a function, class or other items |  `item()` |
# | `from package-name import *` | Import all items |  `item()` |
# 

# ### Example

# In[ ]:


import matplotlib.pyplot as plt # import pyplot from the matplotlib module and alias it with plt
import math as m

x = []
y = []

for e in range(1, 10):
    x.append(e)
    y.append(e**2)

plt.plot(x, y)


# ### What is the best way to import a package or module?
# There is no global answer to this questions. However, be aware that `from package-name import *` overwrites any existing variable or other item in the script. Thus, only use `*` when you are aware of all contents of a module.

# In[ ]:


pi = 9.112 # define a float called pi 
print("Pi is not %1.3f." % pi)

from math import pi # this overwrites the before defined variable pi
print("Pi is %1.3f." % pi)


# ```{tip}
# Define default import packages for *JupyterLab*'s *IPython* kernel (read more on the [*Python* installation page](pyinstall.html#ipython)).
# ```

# ### What items (attributes, classes, functions) are in a module?
# Sometimes we want to explore modules or to check variable attributes. This is achieved with the `dir()` command:

# In[ ]:


import sys
print(sys.path)
print(dir(sys.path))

a_string = "zabaglione"
print(", ".join(dir(a_string)))


# (make-mod)=
# ## Create a Module 
# 
# In object-oriented programming and code factorization, writing own, new modules is an essential task. In order to write a new module, first create a new script. Then, open the new script and add some parameters and functions.

# In[ ]:


# icecreamdialogue.py
flavors = ["vanilla", "chocolate", "bread"]
price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
welcome_msg = "Hi, I only have " + flavors[0] + ". How many scoops do you want?"


# [`icecreamdialogue.py`](https://github.com/hydro-informatics/icecream/raw/master/single-scripts/icecreamdialogue.py) can now either be executed as script (nothing will happen visibly) or imported as module to access its variables (e.g., `icecreamdialogue.flavors`).

# In[ ]:


import icecreamdialogue as icd
print(icd.welcome_msg)
scoops_wanted = 2
print("That makes {0} please".format(icd.price_scoops[scoops_wanted]))


# (standalone)=
# ### Make a script stand-alone 
# 
# As an alternative, we can append the call to items in [`icecreamdialogue.py`](https://github.com/hydro-informatics/icecream/raw/master/single-scripts/icecreamdialogue.py) in the script and run it as a stand-alone script by adding the called item in to a `if (__name__ == '__main__'):` statement:

# In[ ]:


# icecreamdialogue_standalone.py
flavors = ["vanilla", "chocolate", "bread"]
price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
welcome_msg = "Hi, I only have " + flavors[0] + ". How many scoops do you want?"


if (__name__ == '__main__'):
    print(welcome_msg)
    scoops_wanted = 2
    print("That makes {0} please".format(price_scoops[scoops_wanted]))


# Now we can run [`icecreamdialogue_standalone.py`](https://github.com/hydro-informatics/icecream/raw/master/single-scripts/icecreamdialogue_standalone.py) in the terminal (e.g., *PyCharm*'s *Terminal* tab at the bottom of the window).

# ```
# C:\temp\ python icecreamdialogue_standalone.py
# ```

# ```{note}
# Sepending on the definition of system variables used in the *Terminal* environment, the *Python* must be called with a different variable name then `python` (e.g., `python3` on many *Linux* platforms).
# ```

# (standaloneplus)=
# ### Standalone Scripts with Input Parameters
# 
# To make the script more flexible, we can define `scoops_wanted` as an input variable of a function.

# ```python
# # icecreamdialogue_standalone_withinput.py
# flavors = ["vanilla", "chocolate", "bread"]
# price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
# welcome_msg = "Hi, I only have " + flavors[0] + ". How many scoops do you want?"
# 
# def dialogue(scoops_wanted): #formerly in the __main__ statement
#     print(welcome_msg)
#     print("That makes {0} please".format(price_scoops[scoops_wanted]))
# 
# if (__name__ == '__main__'):
#     # import the terminal function emulator sys
#     import sys
#     if len(sys.argv) > 1: # make sure input is provided
#         # if true: call the dialogue function with the input argument
#         dialogue(int(sys.argv[1]))
# ```

# Now we can run `icecreamdialogue_standalone_withinput.py` in the terminal.
# 

# ```
# C:\temp\ python3 icecreamdialogue_standalone.py 2
# ```

# (make-pckg)=
# ### Initialization of a Package (Hierarchically Organized Module)
# 
# Good practice involves that one script does not exceed 50-100 lines of code. In consequence, a package will most likely consist of multiple scripts that are stored in one folder and one master script serves for the initiation of the scripts. This master script is called `__init__.py` and *Python* will always invoke this script name in a package folder. Example structure of a module called `icecreamery`:
# 
#  * `icecreamery` (folder name)
#      - `__init__.py`   - package initiation *Python* script 
#      - `icecreamdialogue.py`   - dialogue producing *Python* script
#      - `icecream_maker.py`   - virtual ice cream producing *Python* script
# 
# In order to automatically invoke the two relevant scripts (sub-modules) of the `icecreamery` module, the `__init__.py` needs to include the following:

# In[ ]:


# __init__.py
print(f'Invoking __init__.py for {__name__}') # not absolutely needed ..
import icecreamery.icecreamdialogue, icecreamery.icecream_maker


# In[ ]:


# example usage of the icecreamery package
import icecreamery
print(icecreamery.icecreamdialogue.welcome_msg)


# Do you remember the `dir()` function? It is intended to list all modules in a package, but it does not do so unless we defined an `__all__` list in the `__init__.py`. 

# ```python
# # __init__.py with __all__ list
# __all__ = ['icecreamdialogue', 'icecream_maker']
# ```

# The full example of the `icecreamery_all` package is available in the [*icecream*](https://github.com/hydro-informatics/icecream) repository.

# In[ ]:


# example usage of the icecreamery package
from icecreamery_all import *
print(icecreamdialogue.welcome_msg)


# ### Package Creation Summary
# 
# A hierachically organized package contains a `__init__.py` file with an `__all__` list to invoke relevant module scripts. The structure of a module can be more complex than the above example list (e.g., with sub-folders). When you write a package, remember to use [meaningful script and variable names](pystyle.html#libs), and to document it.
# 
# ```{tip}
# Implement a custom [logger](pyerror.html#logging) in your module with `logger = logging.getLogger(__name__)` (replace `__name__` with for example `my-module-log`).
# ```

# ## Reload (Re-import) a Package or Module
# 
# Since *Python3* reloading a module requires to import the `importlib` module first. Reloading makes only sense if you are actively writing a new module. To reload any module type:

# ```python
# import importlib
# importlib.reload(my-module)
# ```

# In[ ]:




