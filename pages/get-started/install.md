---
title: Install, setup and use external software
keywords: python
summary: "This chapter guides through the installation of Python Anaconda and Conda environments."
sidebar: mydoc_sidebar
permalink: hy_install.html
folder: get-started
---


Integrated Development Environments (**IDE**s) or batchfiles use conda environments and interpreters to run Python scripts.

## Anaconda<a name="conda"></a>
The very first step to get started consist in downloading and installing [Python Anaconda](https://www.anaconda.com/distribution/). On Windows platforms, Python Anaconda ([download](https://docs.anaconda.com/anaconda/install/windows/)) should be installed in a *LOCAL* user folder (e.g., *C:\users\<your-user-name>\AppData\Local*). Linux or macOS users find download and installation instructions directly at the developers ([Linux installation](https://docs.anaconda.com/anaconda/install/linux/) and [macOS installation](https://docs.anaconda.com/anaconda/install/mac-os/))

## Create and launch conda environments<a name="conda-env"></a>
Python's two-fold development (Python2 and Python3) and other parallel versions of Python (e.g., ESRI's ArcGIS or Nvidia's cuda Python versions) may cause that multiple versions of Python are installed on your computer. As a consequence packages might have been unintentionally or unknowingly installed for another Python than used for a project. However, the parallel existence of multiple Python interpreters that may access packages may be beneficial (e.g., when packages are installed that are not compatible with each other). So, how to deal with the challenge of having multiple Python interpreters installed? 

*Conda Environment*s are the solution to this challenge: A *Conda Environment* is a directory on your computer that represents a virtual environment with a particular Python interpreter (e.g., a Python2 or Python3 executable) and packages. The directory is typically named `env` (or `venv` for virtual environment) and Anaconda will control automatically where the environment directories (folders) are stored on your computer. On Windows, the typical directory is `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`. Note that *AppData* is a hidden folder ([view hidden folders on Windows](https://support.microsoft.com/en-us/help/4028316/windows-view-hidden-files-and-folders-in-windows-10)). Only change the default directory for Conda Environment directories, if you exactly know what you are doing.

To install an environment that suites most of the needs for codes and analyses shown on these pages, apply our provided `environment.yml`:

1. Download the environment file [here](https://github.com/hydro-informatics/materials/blob/master/python/environment.yml) (if needed: copy the file contents of `environment.yml` in a local text editor tool such as [Notedpad++](https://notepad-plus-plus.org/) and save the file for example in a directory called *C:/temp/*)
1. Open Anaconda prompt (`Windows` key > type `Anaconda prompt` > hit `Enter`)
1. Navigate to the download directory where `environment.yml` is located (use [`cd`](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) to navigate for example to *C:/temp/*)
1. Enter `conda env create -f environment.yml` (this creates the environment called `geo-python`)
1. [OPTIONAL] To install more packages, type (in Anaconda prompt):
    - `conda activate geo-python`
    - `conda install PACKAGE_NAME`

## Install and setup an Integrated Development Environment (IDE)
An IDE enables the definition of a project that uses a certain *Conda Environment* and it enables robust coding by pointing out issues directly in the code, even before it was executed once. Powerful IDEs go even further and provide assistance in documenting code with markdown (*.md* files) and direct pipes into *git* ([see section on the usage of *git*](hy_git.html)). *Jetbrains*'s *PyCharm (Community Edition)* is one of the best open-access IDEs for non-commercial use and it can be set up as follows to use conda environments:

1. After downloading and installing, open *PyCharm*
1. Click on `+ Create New Project`
1. A window will open - enter:
    - *Location* - Select a local directory for the project (e.g., *C:/hydro/project*)
    - *Project Interpreter* - Check the `Existing interpreter` box and select the above-installed [conda environment `geo-python`](#conda-env) (e.g., `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`)
    - Click on the `Create` button.

All set - you are ready to work with Python, markdown (documentation), and git now.


## Other software and dependencies {#other}

An office software such as [*LibreOffice*][libreoffice] or Microsoft's *Excel* is required for some of the analyses described on these pages.

For the visualization of geodata (`.shp` and `.tif` files) a GIS software is required and the analyses described on these pages refer to the usage of [*QGIS* ](https://www.qgis.org/en/site/forusers/download.html) (*Please note: There is much more GIS software out there.*).

The visualization of other 2- or 3-dimensional data is possible through [Paraview](https://www.paraview.org/), which can be downloaded on their [website](https://www.paraview.org/).

2-dimensional (2D) numerical simulations described on these pages use the freely available software BASEMENT v.3, which is developed at the ETH Zurich in Switzerland. Visit their [website](https://basement.ethz.ch/) to download the program and documentation.



[libreoffice]: https://www.libreoffice.org/
