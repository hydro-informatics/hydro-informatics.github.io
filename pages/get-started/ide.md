---
title: Install, setup and use external software
keywords: python
summary: "This chapter guides through the installation of Python Anaconda and Conda environments."
sidebar: mydoc_sidebar
permalink: hy_ide.html
folder: get-started
---


Integrated Development Environments (**IDE**s) or batchfiles use conda environments and interpreters to run Python scripts.



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

The visualization of other 2- or 3-dimensional data is possible through [ParaView](https://www.paraview.org/), which can be downloaded on their [website](https://www.paraview.org/).

2-dimensional (2D) numerical simulations described on these pages use the freely available software *BASEMENT* 3.x, which is developed at the ETH Zurich in Switzerland. Visit their [website](https://basement.ethz.ch/) to download the program and documentation.



[libreoffice]: https://www.libreoffice.org/
