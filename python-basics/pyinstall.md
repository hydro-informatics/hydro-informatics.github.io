(install-python)=
# Install Python

*Python*'s two-fold development (*Python2* and *Python3*) and other parallel versions of *Python* (e.g., ESRI's ArcGIS or Nvidia's cuda *Python* versions) may cause that multiple versions of *Python* are installed on your computer (even though *Python2* is about to disappear). As a consequence packages might have been unintentionally or unknowingly installed for another *Python* interpreter than used in a project. However, the parallel existence of multiple *Python* interpreters is sometimes beneficial, for instance, when packages are installed that are not compatible with each other. So how to **deal with the challenge of having multiple *Python* interpreters (or environments) installed?**

There are multiple answers to this question and the best option depends, to some extent, to personal preferences and the **O**perating **S**ystem (**OS**) - also referred to as **platform**. For instance, *conda* environments might be preferable with *Windows* and *pip* environments with *Linux* (e.g., *Debian*/*Ubuntu*). Nevertheless, both *pip* and *conda* work well on both platforms (and also with *macOS*). Since *Python 3.4* (and *Python 2.7.9*), *pip* is installed with the basic {{ getpy }} installation. To work with *conda* environments, the installation of {ref}`anaconda` is required (no additional installation of *Python* is necessary in this case).

*Conda* environments
: A *conda environment* is a directory on your computer that represents a virtual environment with a particular *Python* interpreter (e.g., a Python2 or Python3 executable) and packages/libraries. The directory is typically named `env` (or `venv` for a virtual environment) and *Anaconda* will control automatically where the environment directories (folders) are stored on your computer. On *Windows*, the typical installation directory is `C:\users\<your-user-name>\AppData\Local\Continuum\anaconda3\envs\`. Note that *AppData* is a hidden folder ([view hidden folders on Windows](https://support.microsoft.com/en-us/help/4028316/windows-view-hidden-files-and-folders-in-windows-10)). Only change the default directory for *conda* environment directories, if you exactly know what you are doing.

pipenv / venv
: *pipenv* or *pip* environments are *Python* environments that can be created with *Python*s default [pip](https://pip.pypa.io/en/stable/) package-management system (default since *Python 2.7.9.* / *Python 3.4*). With pip, a virtual environment can be created (typically stored in a *venv* folder in the working directory).

This section guides through the installation of a computational environment that is tailored for working with contents in this ebook. The environment uses the **flusstools** pip-package, which provides many useful routines for river analyses.

## Get GDAL

*FlussTools* fundamentally depends on many *gdal* functions and scripts, but the installation of *gdal* involves dependencies that often break with new developments on different platforms.

### GDAL on Windows

Get the latest wheel (**whl**) from https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

### GDAL on Linux

Before getting ready to install *gdal* on *Linux*, make sure that all fundamental libraries are installed:

```
sudo apt install python3-pip python3-tk tk8.6-dev libgeos-dev
```

Then, install *QGIS* and *GDAL* for *Linux* (this should work with any *Debian* architecture) and make sure to use the correct `pip` command at the end (i.e., it might be necessary to replace `pip3` with `pip`):

```
 sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt update
 sudo apt install gdal-bin libgdal-dev
 export CPLUS_INCLUDE_PATH=/usr/include/gdal
 export C_INCLUDE_PATH=/usr/include/gdal
 pip3 install GDAL
 ```

To resolve any recent issues, check out comments about the latest *GDAL* release on the `GDAL website <https://gdal.org/download.html#current-releases>`_.

(pip-env)=
## pip and venv

Consider to install, create and activate a new virtual environment before installing the *flusstools* requirements (read more at {{ getpy }}) as follows:

````{tabbed} Linux
Install *virtualenv*:
```
python3 -m pip install --user virtualenv
```
Create a new virtual environment with *venv*:

```
python3 -m venv DIR/TO/ENV
```

Then activate the new environment:

```
source DIR/TO/ENV/bin/activate
```
Double-check that the environment is activated:
```
which python
.../DIR/TO/ENV/bin/python
```
````

````{tabbed} Windows
Install *virtualenv* (in the following, alternatively use `py` instead of `python`, if `python` returns errors):
```
python -m pip install --user virtualenv
```

Create a new virtual environment with *venv*:

```
python -m venv DIR\TO\ENV
```


Then activate the new environment:

```
.\DIR\TO\ENV\Scripts\activate
```

Double-check that the environment is activated:
```
where python
.../DIR/TO/ENV/bin/python.exe
```
````

Read more about virtual environments and pip at [https://packaging.python.org](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Next, install the *flusstools* requirements, either in a newly created and activated virtual environment (recommended) or in the system's *Python* installation:

* Download {{ ft_req }} (e.g., in the user `~/Downloads/` directory)
* Open *Terminal* and `cd` to the download directory (e.g., `~/Downloads/`)
* Install the *flusstools* requirements: `pip install -r requirements.txt`
* Install *flusstools*: `pip install flusstools`

```{admonition} Windows GDAL Error: `Setup script exited with error: Microsoft Visual C++ 14.0 ...`
:class: error, dropdown
 Currently, there is an issue with installing GDAL when *Microsoft Visual C++* is missing or outdated. Thus, to enable the installation of GDAL on *Windows*, first download and install **Microsoft Visual C++** from [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
```

(conda-env)=
## Conda Environments

### Quick Guide


1. Download the *flussenv* [environment file](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/environment.yml) (if needed: copy the file contents of `environment.yml` in a local text editor, such as {ref}`npp`, and save the file for example in a directory called *C:/temp/*).
1. Open *Anaconda Prompt* (`Windows` key > type `Anaconda Prompt` > hit `Enter`).
1. Navigate to the download directory where `environment.yml` is located (use [`cd`](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) to navigate, for example, to `cd C:/temp/`).
1. Enter `conda env create -f environment.yml` (this creates an environment called `flussenv`). <br> *... takes a while ...*
1. Activate *flussenv*: `conda activate flussenv`
1. Install *flusstools*: `pip install flusstools`

### Create and Install

To create a new *conda* environment, open *Anaconda Prompt* and type (replace `ENV-NAME` for example with `flussenv`):

```
conda create --name ENV-NAME python=3.8
```

An alternative (and recommended for the tutorials on this page) option is to install an environment that suites most of the needs for codes and analyses shown on these pages through an *environment* (*YML*) file:



```{tip}
The provided [environment.yml](https://github.com/hydro-informatics/materials-py-install/blob/master/environment.yml) file creates a carefree environment for using *Python* as described on this website. Still, you may want to create your own environment and use this section refresh your mind for installing any missing libraries.
```

### Activate Environment

The active environment corresponds to the environment that you are working in (e.g., for installing libraries or using *Jupyter*). To activate the above-created *flussenv* environment:

1. Open *Anaconda Prompt* (`Windows` key or click on the start menu of your operating system > type `Anaconda Prompt` > hit `Enter`).
1. Activate the *flussenv* environment with `conda activate flussenv`

(install-pckg)=
### Install Additional *Python* Packages

To install more {ref}`*Python* packages <sec-pypckg>`:

1. Activate the environment where you want to install, remove, or modify packages (e.g., `conda activate flussenv` - see above).
1. Install a package by typing `conda install PACKAGE_NAME` (if the package cannot be found, try `conda install -c conda-forge PACKAGE_NAME`).

Alternatively, press the `Windows` key (or click on the start menu of your operating system) > type `Anaconda Navigator` > got to the `Environments` tab > select the `flussenv` environment (or create another environment) > *install* > install packages.

### Remove (Delete) Environment
To remove a conda environment open *Anaconda Prompt* and type:

```
conda env remove --name ENVIRONMENT-TO-REMOVE
```

For example, to remove the `flussenv` environment type:

```
conda env remove --name flussenv
```

There are many more `conda` commands and the most important ones are summarized in the developer's [*conda* cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).

(python-ide-setup)=
## Setup Interfaces and IDEs

To follow the course content and run code cells, it is recommended to use {ref}`jupyter`, which can be installed locally or run it remotely by clicking on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter) - the batch is implementd at the top of all jupyter notebook-based sections. To create projects, develop programs, or simply to complete course assignments, it is recommended to use an Integrated Development Environment (*IDE*), such as {ref}`pycharm`.

### JupyterLab

The descriptions on the *Get started* for installing and launching [*JupyterLab*](../get-started/ide.html#jupyter), where *Jupyter* notebooks (*.ipynb* files), *Python* scripts (*.py* files), folders and more can be created from the *File* menu.

```{tip}
Start *JupyterLab* by typing `jupyter lab` in *Anaconda Prompt*.
```

 The *Kernel* menu runs the defined programming language (*Python 3* in the example below). The *Settings* menu provides options to configure styles (e.g., choose the *JupyterLab Dark* theme shown in the below figure).
*JupyterLab* runs on a local server (typically on `localhost:XXPORTXX/lab`), which is why it is just like an interactive website in your browser. At the beginning it takes some getting used to, but one gets quickly familiar with it and there are many advantages such as the inline use of online graphics.

```{figure} ../img/jupyter-illu.png
:alt: pyc-prj-setup

JupyterLab in Dark theme appearance with a Jupyter notebook (xml.ipynb) opened showing the combination of a markdown cell (Charts(plots) and a Python 3 cell.
```

*Jupyter* is a spin-off of [*IPython*](https://ipython.org/), which is "a rich architecture for interactive computing". Therefore, when we start a *Python* kernel in *JupyterLab*, an *IPython* kernel is started, which refers to the currently activated *conda* environment. So if you need to install a package for usage in *JupyterLab*, follow the [above instructions](##install-pckg) and make sure that the corresponding environment is activated.

*Python* cells in *Jupyter* notebooks often require certain packages, which must be reloaded for each cell after each kernel start (learn more about packages in the {ref}`sec-pypckg` section). So it can be useful to define default imports for *IPython* and this works as follows.

1. Look for the (hidden) `.ipython` folder on your computer
    * In *Windows*, this ist typically in your user folder (`C:\Users\your-name\.ipython\`) ([how to show hidden files in *Windows*](https://support.microsoft.com/en-us/help/14201/windows-show-hidden-files)
    * In *Linux* (or other *Unix*-based system such as *macOS*), files beginning with a `.` are hidden and *IPython* is typically located in `/usr/local/etc/ipython/` or `/usr/local/etc/.ipython/` (either use the terminal and type `ls -a` or simultaneously hit the `CTRL`+`H` keys)
1. In the `.ipython` or `ipython` folder, create a sub-directory called `/profile_default/startup/` (if not yet present).
1. If not yet present: Create the directory `.../ipython/profile_default/startup/`, with a *Python* file called `ipython_config.py`.
1. Open `ipython_config.py` (right-click > edit - do not run the file) and add default import packages.
1. For the Python (basics) course it is recommended to define the following default imports in `ipython_config.py` (add modifications, then save and close the file):

```python
import os
import sys
import numpy as np
import pandas as pd
import matplotlib as plt
import tkinter as tk
from tkinter import ttk
```

For the geospatial *Python* section, consider to add ([read `gdal` installation instructions](../geopy/geo-pckg.html#gdal) first):
```python
import gdal
from gdal import ogr
from gdal import osr
```

```{note}
The `default_profile` is part of the default *Jupyter* installation and it is normally not necessary to create it manually. The [*IPython* docs](https://ipython.org/ipython-doc/stable/config/intro.html) provide more detail about custom settings and modifying profiles on any platform.
```

(atom-setup)=
### Atom and Python

Window Users
: Preferably use the *flusstools* conda environment because its *gdal* dependency may cause errors when used with *pip*. To setup a *Python* *Anaconda* terminal in *Atom* the following **one-time steps** are required:

  * Make sure that the `platformio-ide-terminal` package is installed (see {ref}`atom-packages`).
  * Launch `platformio-ide-terminal` (in *Atom* go to **Packages** (top menu) > **platformio-ide-terminal** > **New Terminal**)
  * Typically, [PowerShell](https://aka.ms/pscore6) will open, where the following commands need to be entered:
    * `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
    * `conda init`
  * Close the current PowerShell.

  The following steps are necessary for **regular use** of the *flusstools* package in a *conda* environment in `platformio-ide-terminal`:

  * Launch `platformio-ide-terminal` (in *Atom* go to **Packages** (top menu) > **platformio-ide-terminal** > **New Terminal**)
  * In the terminal activate the *flussenv* environment: `conda activate flusstools`
  * In the activated environment launch python `python`
  * If the installation of *gdal* and *flusstool* was successful, the following imports should pass silently (otherwise, start over with installing *flussenv* and *flusstools*):
    * `import gdal`
    * `import flusstools as ft`

Linux Users
: When *flusstools* and its requirements were installed in the system's *Python* interpreter, it is sufficient to launch `platformio-ide-terminal` (in *Atom* go to **Packages** (top menu) > **platformio-ide-terminal** > **New Terminal**). Note that this action requires that the `platformio-ide-terminal` package is installed (see {ref}`atom-packages`).

  In the opening terminal start *Python* and try to import *flusstools*:

  ```
  user:~$ python
  Python 3.X.X (default, MMM DD YYYY, hh:mm:ss)
  [GCC 9.X.X on linux]
  >>> import flusstools as ft
  ```

  The import of *flusstools* should pass silently. Otherwise, re-install the requirements (`pip install -r requirements.txt`) and *flusstools* ( `pip install flusstools`).



(ide-setup)=
### PyCharm Python Projects

After the successful installation of [*PyCharm*](../get-started/ide.html#ide) within *Anaconda*, use the just created *conda* environment as interpreter. The following steps guide through the setup of *PyCharm* for using *conda* environments.

1. Launch *PyCharm* and create a new project.
   ```{figure} ../img/pyc-project.png
:alt: pyc-prj" max-width="500px

Create a new project in PyCharm.
```
1. Define The new `flussenv` environment as *Pure Python* project interpreter:
    * Select *New environment using `Conda`
    * In the *Location* box select the new `flussenv` environment
    * Click *Create* to create the new project.
   ```{figure} ../img/pyc-prj-setup.png
:alt: pyc-prj-setup

Setup the flussenv conda environment for the new project.
```
1. Verify that the project interpreter is correctly defined:
  * Click on *PyCharm*'s `File` menu and select `Settings...`
  * In the *Settings* window go to `Project: [NAME]` > `Project Interpreter`
  * Make sure that the above-created `flussenv` *conda* environment is defined as *Project Interpreter*.

 ```{figure} ../img/pyc-prj-interp.png
:alt: pyc-prj-interp

Verify the correct setup of the Project Interpreter.
```

```{tip}
**Are you struggling with setting up *PyCharm* correctly?** *PyCharm* and *Anaconda* are designed for working hand-in-hand and the developers provide an [up-to-date documentation](https://docs.anaconda.com/anaconda/user-guide/tasks/pycharm/) for setting up *PyCharm* to work with *conda* environments.
```
