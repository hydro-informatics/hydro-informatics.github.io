---
title: Install Python
tags: [python]
keywords: python
sidebar: mydoc_sidebar
permalink: hypy_install.html
folder: python-basics
---


*Python*'s two-fold development (*Python2* and *Python3*) and other parallel versions of *Python* (e.g., ESRI's ArcGIS or Nvidia's cuda *Python* versions) may cause that multiple versions of *Python* are installed on your computer. As a consequence packages might have been unintentionally or unknowingly installed for another *Python* than used for a project. However, the parallel existence of multiple *Python* interpreters that may access packages may be beneficial (e.g., when packages are installed that are not compatible with each other). So, **how to deal with the challenge of having multiple *Python* interpreters installed?**

***Conda* environments** are the solution to this challenge: A *Conda Environment* is a directory on your computer that represents a virtual environment with a particular *Python* interpreter (e.g., a Python2 or Python3 executable) and packages. The directory is typically named `env` (or `venv` for virtual environment) and Anaconda will control automatically where the environment directories (folders) are stored on your computer. On Windows, the typical directory is `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`. Note that *AppData* is a hidden folder ([view hidden folders on Windows](https://support.microsoft.com/en-us/help/4028316/windows-view-hidden-files-and-folders-in-windows-10)). Only change the default directory for Conda Environment directories, if you exactly know what you are doing.

{% include tip.html content="Before you continue, make sure that *Anaconda* is installed according to the [descriptions in the *Get Started*](hy_ide.html#anaconda) section." %}

## Create and install conda environments
To install an environment that suites most of the needs for codes and analyses shown on these pages, apply our provided `environment.yml`:

1. Download the environment file [here](https://github.com/hydro-informatics/materials/blob/master/python/environment.yml) (if needed: copy the file contents of `environment.yml` in a local text editor tool such as [Notedpad++](https://notepad-plus-plus.org/) ([alternatives](hy_others.html#npp)) and save the file for example in a directory called *C:/temp/*)
1. Open Anaconda prompt (`Windows` key > type `Anaconda prompt` > hit `Enter`)
1. Navigate to the download directory where `environment.yml` is located (use [`cd`](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) to navigate for example to *C:/temp/*)
1. Enter `conda env create -f environment.yml` (this creates the environment called `geo-python`)
1. [OPTIONAL] To install more packages, type (in Anaconda prompt):
    - `conda activate geo-python`
    - `conda install PACKAGE_NAME`

## Setup PyCharm IDE {#ide-setup}
After the successful installation of your favorite [*IDE*](hy_ide.html#ide) within *Anaconda*, use the just created *conda* environment as interpreter. The following steps guide through the setup of *PyCharm* for using *conda* environments.

1. Launch *PyCharm* and create a new project. 
    {% include image.html file="pyc-project.png" alt="pyc-prj" max-width="500px" caption="Create a new project in PyCharm." %}
1. Define The new `geo-python` environment as *Pure Python* project interpreter:
    * Select *New environment using `Conda`
    * In the *Location* box select the new `geo-python` environment
    * Click *Create* to create the new project.
    {% include image.html file="pyc-prj-setup.png" alt="pyc-prj-setup" caption="Setup the geo-python conda environment for the new project." %}
1. Verify that the project interpreter is correctly defined:
    * Click on *PyCharm*'s `File` menu and select `Settings...` 
    * In the *Settings* window go to `Project: [NAME]` > `Project Interpreter` 
    * Make sure that the above-created `gep-python` *conda* environment is defined as *Project Interpreter*.
    {% include image.html file="pyc-prj-interp.png" alt="pyc-prj-interp" caption="Verify the correct setup of the Project Interpreter." %}