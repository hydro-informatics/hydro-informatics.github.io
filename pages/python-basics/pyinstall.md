---
title: Install Python
tags: [python, ipython, jupyter, pycharm, anaconda, conda, interface, install]
keywords: python, ipython, jupyter, pycharm
sidebar: mydoc_sidebar
permalink: hypy_install.html
folder: python-basics
---


*Python*'s two-fold development (*Python2* and *Python3*) and other parallel versions of *Python* (e.g., ESRI's ArcGIS or Nvidia's cuda *Python* versions) may cause that multiple versions of *Python* are installed on your computer. As a consequence packages might have been unintentionally or unknowingly installed for another *Python* than used for a project. However, the parallel existence of multiple *Python* interpreters that may access packages may be beneficial (e.g., when packages are installed that are not compatible with each other). So, **how to deal with the challenge of having multiple *Python* interpreters installed?**

***Conda* environments** are the solution to this challenge: A *Conda Environment* is a directory on your computer that represents a virtual environment with a particular *Python* interpreter (e.g., a Python2 or Python3 executable) and packages. The directory is typically named `env` (or `venv` for virtual environment) and Anaconda will control automatically where the environment directories (folders) are stored on your computer. On Windows, the typical directory is `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`. Note that *AppData* is a hidden folder ([view hidden folders on Windows](https://support.microsoft.com/en-us/help/4028316/windows-view-hidden-files-and-folders-in-windows-10)). Only change the default directory for Conda Environment directories, if you exactly know what you are doing.

{% include tip.html content="Before you continue, **make sure that *Anaconda* is installed** according to the [descriptions in the *Get Started*](hy_ide.html#anaconda) section." %}

## Create and install conda environments 
To install an environment that suites most of the needs for codes and analyses shown on these pages, apply our provided `environment.yml`:

1. Download the environment file [here](https://github.com/hydro-informatics/materials-py-install/blob/master/environment.yml) (if needed: copy the file contents of `environment.yml` in a local text editor tool such as [Notedpad++](https://notepad-plus-plus.org/) ([alternatives](hy_others.html#npp)) and save the file for example in a directory called *C:/temp/*)
1. Open Anaconda prompt (`Windows` key > type `Anaconda prompt` > hit `Enter`)
1. Navigate to the download directory where `environment.yml` is located (use   [`cd`](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands)   to navigate for example to *C:/temp/*)
1. Enter `conda env create -f environment.yml` (this creates an environment called `hypy`)

## Install additional *Python* packages in a *conda* environment {#install-pckg}
To install more [*Python* packages](hypy_pckg.html): 

1. Open *Anaconda Prompt* (`Windows` key or click on the start menu of your operating system > type `anaconda prompt` > hit `Enter` key on your keyboard)
1. Activate environment `conda activate hypy`
1. Install package `conda install PACKAGE_NAME` (if the package cannot be found, try `conda install -c conda-forge PACKAGE_NAME`)

Alternatively, press the `Windows` key (or click on the start menu of your operating system) > type `Anaconda Navigator` > got to the `Environments` tab > select the `hypy` environment (or create another environment) > install & install packages. 

## Setup Interfaces and IDEs

To follow the course content and run code cells, it is recommended to use [*JupyterLab*](hy_ide.html#jupyter). To create projects, develop programs, or simply to complete course assignments, it is recommended to use an Integrated Development Environment (*IDE*) such as [*PyCharm*](hy_ide.html#pycharm).
    
### *JupyterLab*

The descriptions on the *Get started* for installing and launching [*JupyterLab*](hy_ide.html#jupyter), where *Jupyter* notebooks (*.ipynb* files), *Python* scripts (*.py* files), folders and more can be created from the *File* menu. The *Kernel* menu runs the defined programming language (*Python 3* in the example below). The *Settings* menu provides options to configure styles (e.g., choose the *JupyterLab Dark* theme shown in the below figure). 
*JupyterLab* runs on a local server (typically on `localhost:XXPORTXX/lab`), which is why it is just like an interactive website in your browser. At the beginning it takes some getting used to, but one gets quickly familiar with it and there are many advantages such as the inline use of online graphics.

{% include image.html file="jupyter-illu.png" alt="pyc-prj-setup" caption="JupyterLab in Dark theme appearance with a Jupyter notebook (xml.ipynb) opened showing the combination of a markdown cell (Charts(plots)) and a Python 3 cell." %}

*Jupyter* is a spin-off of [*IPython*](https://ipython.org/), which is "a rich architecture for interactive computing". Therefore, when we start a *Python* kernel in *JupyterLab*, an *IPython* kernel is started. This is different from a *conda* environment, but it can still access packages installed in the *conda* `base` environment. So if you need to install a package for usage in *JupyterLab*, follow the [above instructions](##install-pckg), but make sure that the `base` environment is activated.

{#ipython}
*Python* cells in *Jupyter* notebooks often require certain packages, which must be reloaded for each cell after each kernel start (we will learn more about packages later on the [Modules and packages](hypy_pckg.html) page). So it can be useful to define default imports for *IPython* and this works as follows.

1. Look for the `.ipython` folder on your computer
    * In *Windows*, this ist typically in your user folder (`C:\Users\your-name\.ipython\`)
    * In *Linux* (or other *Unix*-based system such as *macOS*), files beginning with a `.` are hidden and *IPython* is typically located in `/usr/local/etc/ipython/` or `/usr/local/etc/.ipython/`
1. In the `.ipython` or `ipython` folder, create a sub-directory called `/profile_default/startup/` (if not yet present).
1. In the `*ipython/profile_default/startup/` directory, create a *Python* file called `ipython_config.py` (if not yet present).
1. Open `ipython_config.py` (right-click > edit - do not run the file) and add default import packages.
1. For the Python (basics) course it is recommended to define the following default imports in `ipython_config.py` (add modifications, then save and close the file):

```python
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as plt
import tkinter as tk
from tkinter import ttk
```

{% include note.html content="The `default_profile` is part of the default *Jupyter* installation and it is normally not necessary to create it manually. The [*IPython* docs](https://ipython.org/ipython-doc/stable/config/intro.html) provide more detail about custom settings and modifying profiles on any platform." %}


### *PyCharm* {#ide-setup}
After the successful installation of [*PyCharm*](hy_ide.html#ide) within *Anaconda*, use the just created *conda* environment as interpreter. The following steps guide through the setup of *PyCharm* for using *conda* environments.

1. Launch *PyCharm* and create a new project. 
    {% include image.html file="pyc-project.png" alt="pyc-prj" max-width="500px" caption="Create a new project in PyCharm." %}
1. Define The new `hypy` environment as *Pure Python* project interpreter:
    * Select *New environment using `Conda`
    * In the *Location* box select the new `hypy` environment
    * Click *Create* to create the new project.
    {% include image.html file="pyc-prj-setup.png" alt="pyc-prj-setup" caption="Setup the hypy conda environment for the new project." %}
1. Verify that the project interpreter is correctly defined:
    * Click on *PyCharm*'s `File` menu and select `Settings...` 
    * In the *Settings* window go to `Project: [NAME]` > `Project Interpreter` 
    * Make sure that the above-created `hypy` *conda* environment is defined as *Project Interpreter*.
    {% include image.html file="pyc-prj-interp.png" alt="pyc-prj-interp" caption="Verify the correct setup of the Project Interpreter." %}