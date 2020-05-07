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
An IDE enables the definition of a project to use for example a specific [*Conda Environment*](https://docs.conda.io/) and it enables robust coding by pointing out issues directly in the code, even before it was executed once. Powerful IDEs go even further and provide assistance in documenting code with markdown (*.md* files) and direct pipes into *git* ([see section on the usage of *git*](hy_git.html)). *Jetbrains*'s [*PyCharm (Community Edition)*](https://www.jetbrains.com/pycharm/) is one of the best open-access IDEs for non-commercial use and good alternatives are [*Spyder IDE*](https://www.spyder-ide.org/) (for *Python*) or [*RStudio*](https://rstudio.com/) (*R* and *Python*). However, before launching any project in an IDE, the installation of an interpreter (e.g., *Python* or *R*) is necessary. The cooking recipe for setting up an IDE is:
 
 and it can be set up as follows to use conda environments:
1. Install interpreter (e.g., *Python Anaconda* according to the instructions in the [Python section](hypy_install.html)).
1. [Download](https://www.jetbrains.com/pycharm/), install and open an IDE  *PyCharm*
1. Click on `+ Create New Project`
1. A window will open - enter:
    - *Location* - Select a local directory for the project (e.g., *C:/hydro/project*)
    - *Project Interpreter* - Check the `Existing interpreter` box and select the above-installed [conda environment `geo-python`](#conda-env) (e.g., `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`)
    - Click on the `Create` button.

All set - you are ready to work with Python, markdown (documentation), and [git](hy_git.html) now.


## Other software and dependencies {#other}

An office software such as [*LibreOffice*][libreoffice] or Microsoft's *Excel* is required for some of the analyses described on these pages.

[libreoffice]: https://www.libreoffice.org/
