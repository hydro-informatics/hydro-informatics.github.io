---
title: Python Basics - Packages and Modules
keywords: git
sidebar: mydoc_sidebar
permalink: hypy_pckg.html
folder: python-basics
---

## Import packages or modules

Importing a package or module in *Python* makes external functions and other elements (such as objects) of modules accessible in a script. The functions and other elements are stored within another *Python* file (`.py`) in some */site_packages/* folder of the interpreter environments. Thus, in order to use a non-standard package, it needs to be downloaded and installed first. Standard packages (e.g., `os`, `math`) are always accessible and other can be added with *conda* ([read the installation instructions](hypy_install.html#install-pckg)).

{% include note.html content="**The difference between modules and packages**. Modules are single or multiple files that can be imported as one import (e.g., `import a_module`). Packages are a collection of modules in a directory with a defined package hierarchy, which enables the import of individual modules (e.g. `from a_package.module import a_function`). Packages are therefore also modules, but with a hierarchy definition (i.e., a ` __path__` attribute and a `__init__.py` file). Sounds fuzzy? Read this page down to the bottom and come back here to re-read this note." %}

The `os` package provides some useful system-terminal like commands, for example, to manage folder directories. So let's import this essential package.



```python
import os
print(os.getcwd()) # print current working directory

```

    C:\Users\schwindt\jupyter\hypy
    

### Overview of import options

Here is an overview of options to import packages or modules (hierarchical parts of packages):

| Command | Description | Usage of attributes |
|---------|-------------|---------------------|
| `import package-name` | Import an original module | `package.item()` |
| `import package-name as nick-name` | Import module and rename (alias) it in the script |  `nick-name.item()` |
| `from package-name import item` | Import only a function, class or other items |  `item()` |
| `from package-name import *` | Import all items |  `item()` |


### Example


```python
import matplotlib.pyplot as plt # import pyplot from the matplotlib module and alias it with plt
import math as m

x = []
y = []

for e in range(1, 10):
    x.append(e)
    y.append(e**2)

plt.plot(x, y)
```

### What is the best way to import a package or module?
There is no global answer to this questions. However, be aware that `from package-name import *` overwrites any existing variable or other item in the script. Thus, only use `*` when you are aware of all contents of a module.


```python
pi = 9.112 # define a float called pi 
print("Pi is not %1.3f." % pi)

from math import pi # this overwrites the before defined variable pi
print("Pi is %1.3f." % pi)
```

    Pi is not 9.112.
    Pi is 3.142.
    

{% include tip.html content="Define default import packages for *JupyterLab*'s *IPython* kernel (read more on the [*Python* installation page](hypy_install.html#ipython))." %}

### What items (attributes, classes, functions) are in a module?
Sometimes we want to explore modules or to check variable attributes. This is achieved with the `dir()` command:


```python
import sys
print(sys.path)
print(dir(sys.path))

a_string = "zabaglione"
print(", ".join(dir(a_string)))
```

## Create a module {#make-mod}
In object-oriented programming and code factorization, writing own, new modules is an essential task. In order to write a new module, first create a new script. Then, open the new script and add some parameters and functions.


```python
## icecreamdialogue.py
flavors = ["vanilla", "chocolate", "bread"]
price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
welcome_msg = "Hi, I only have " + flavors[0] + ". How many scoops do you want?"
```

`icecreamdialogue.py` can now either be executed as script without returning anything or imported.


```python
import icecreamdialogue as icd
print(icd.welcome_msg)
scoops_wanted = 2
print("That makes {0} please".format(icd.price_scoops[scoops_wanted]))
```

    Hi, I only have vanillaleft. How many scoops do you want?
    That makes three euros please
    

### Make a script stand-alone {#standalone}
As an alternative, we can append the call to items in `icecreamdialogue.py` in the script and run it as a stand-alone script by adding the called item in to a `if (__name__ == '__main__'):` statement:


```python
## icecreamdialogue_standalone.py
flavors = ["vanilla", "chocolate", "bread"]
price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
welcome_msg = "Hi, I only have " + flavors[0] + ". How many scoops do you want?"


if (__name__ == '__main__'):
    print(welcome_msg)
    scoops_wanted = 2
    print("That makes {0} please".format(price_scoops[scoops_wanted]))
```

Now we can run `icecreamdialogue_standalone.py` in the terminal.
C:\temp\ python3 icecreamdialogue_standalone.py
### Make standalone script with input parameter
To make the script more flexible, we can define `scoops_wanted` as an input variable of a function.


```python
## icecreamdialogue_standalone_withinput.py
flavors = ["vanilla", "chocolate", "bread"]
price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
welcome_msg = "Hi, I only have " + flavors[0] + ". How many scoops do you want?"

def dialogue(scoops_wanted): #formerly in the __main__ statement
    print(welcome_msg)
    print("That makes {0} please".format(price_scoops[scoops_wanted]))

if (__name__ == '__main__'):
    import sys  # we need sys here
    if len(sys.argv) > 1: # make sure input is provided
        # if true: call the dialogue function with the input argument
        dialogue(int(sys.argv[1]))
```

Now we can run `icecreamdialogue_standalone_withinput.py` in the terminal.
C:\temp\ python3 icecreamdialogue_standalone.py 2
### Initialization of a package (hierarchically organized module) {#make-pckg}
Good practice involves that one script does not exceed 50-100 lines of code. In consequence, a package will most likely consist of multiple scripts that are stored in one folder and one master script serves for the initiation of the scripts. This master script is called `__init__.py` and *Python* will always invoke this script name in a package folder. Example structure of a module called `icecreamery`:

 * `icecreamery` (folder name)
     - `__init__.py`   - package initiation *Python* script 
     - `icecreamdialogue.py`   - dialogue producing *Python* script
     - `icecream_maker.py`   - virtual ice cream producing *Python* script

In order to automatically invoke the two relevant scripts (sub-modules) of the `icecreamery` module, the `__init__.py` needs to include the following:


```python
## __init__.py
print(f'Invoking __init__.py for {__name__}') # not absolutely needed ..
import icecreamery.icecreamdialogue, icecreamery.icecream_maker
```


```python
# example usage of the icecreamery package
import icecreamery
print(icecreamery.icecreamdialogue.welcome_msg)
```

    Invoking __init__.py for icecreamery
    Hi, I only have vanilla. How many scoops do you want?
    

Do you remember the `dir()` function? It is intended to list all modules in a package, but it does not do so unless we defined an `__all__` list in the `__init__.py`. 


```python
## __init__.py with __all__ list
__all__ = ['icecreamdialogue', 'icecream_maker']
import *
```


```python
# example usage of the icecreamery package
import icecreamery_all
print(icecreamery_all.icecreamdialogue.welcome_msg)
```

    Hi, I only have vanilla. How many scoops do you want?
    

### Package creation summary
A hierachically organized package contains a `__init__.py` file with an `__all__` list to invoke relevant module scripts. The structure of a module can be more complex than the above example list (e.g., with sub-folders). When you write a package, remember to use meaningful script and variable names, and to document it.

## Reload (re-import) a package or module

Since *Python3* reloading a module requires to import the `importlib` module first. Reloading makes only sense if you are actively writing a new module. To reload any module type:


```python
import importlib
importlib.reload(my-module)
```
