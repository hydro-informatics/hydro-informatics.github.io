---
title: Anaconda and Integrated Development Environments (IDEs)
keywords: IDEs, conda, Anaconda, jupyter, pycharm
summary: "Let's start at the very beginning ..."
sidebar: mydoc_sidebar
permalink: hy_ide.html
folder: get-started
---

## Anaconda {#anaconda}

{% include note.html content="[Anaconda](https://www.anaconda.com/distribution/) represents the baseline for many applications presented on this web site. It enables the built-in installation of programming languages such as *Python* and *R*, as well as *IDE*s such as [*PyCharm*](https://www.jetbrains.com/pycharm/), [*Spyder*](https://www.spyder-ide.org/), or [*Jupyter Notebook (Lab)*](https://jupyter.org/)." %}

The very first step to get started consist in downloading and installing [Anaconda](https://www.anaconda.com/distribution/). In Windows, *Anaconda* ([download](https://docs.anaconda.com/anaconda/install/windows/)) should be installed in a *LOCAL* user folder (e.g., *C:\users\<your-user-name>\AppData\Local*). Linux or macOS users find download and installation instructions directly at the developers web site ([Linux installation](https://docs.anaconda.com/anaconda/install/linux/) and [macOS installation](https://docs.anaconda.com/anaconda/install/mac-os/)).

After the successful installation of *Anaconda*, *IDE*s for *Python* programming or *markdown* editing can be directly installed by launching the **Anaconda navigator**. **`conda`** environments can be created later on following the [instructions in the *Python (fundamentals)* section](hypy_install.html#conda-env).

## Install and setup Interfaces {#ide}

An interfaces to an *Integrated Development Environment* (*IDE*) enables the definition of a project to use for example a specific [*Conda Environment*](https://docs.conda.io/) and it enables robust coding by pointing out issues directly in the code, even before it was executed once. Powerful IDEs go even further and provide assistance in documenting code with markdown (*.md* files) and direct pipes into *git* ([see section on the usage of *git*](hy_git.html)). *Jetbrains*'s [*PyCharm (Community Edition)*](https://www.jetbrains.com/pycharm/) is one of the best open-access IDEs for non-commercial use and good alternatives are [*Spyder IDE*](https://www.spyder-ide.org/) (for *Python*) or [*RStudio*](https://rstudio.com/) (*R* and *Python*). However, before launching any project in an IDE, the installation of an interpreter (e.g., *Python* or *R*) is necessary.

{% include note.html content="These pages are written with [*JupyterLab*](https://jupyter.org/), which is suitable to follow the course contents. *IDE*s such as *PyCharm* or *Spyder* are more suitable to setup projects (e.g., for course assignments)." %}


### Install *PyCharm* *IDE* (Anaconda Navigator) {#pycharm}
To set up *PyCharm* through *Anaconda* navigator:

1. Open *Anaconda Navigator* (i.e., *Anaconda*'s graphical user interface) and make sure to be in the *Home* tab.
1. Look for *PyCharm* and click on the *Install* button (if already installed, there is only a *Launch* button).
1. After successful installation, open *PyCharm*, by clicking on the *Launch* button.
1. In *PyCharm* click on `+ Create New Project`
1. A window will open - enter:
    - *Location* - Select a local directory for the project (e.g., *C:/hydro/project*)
    - *Project Interpreter* - Check the `Existing interpreter` box and select the above-installed [conda environment `geo-python`](#conda-env) (e.g., `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`)
    - Click on the `Create` button.

All set - you are ready to work with *Python*, markdown (documentation), and [git](hy_git.html) now.

{% include note.html content="*PyCharm* can also be installed without *Anaconda*, directly from the [developer's website](https://www.anaconda.com/distribution/)." %}

{% include important.html content="***Python* users** read more about setting up *conda* environments on the [*Python (basics)*](hypy_install.html#ide-setup) page." %}

### Install *JupyterLab* (Anaconda Navigator) {#jupyter}

*JupyterLab* is a product of the nonprofit organization [*Project Jupyter*](https://jupyter.org/), which develops "open-source software, open-standards, and services for interactive computing across dozens of programming languages". A *Jupyter* notebook (*.ipynb* file) enables the combination of markdown text blocks with executable code blocks. Essentially, a *Jupyter* notebook is a JavaScript Object Notation ([JSON](https://www.json.org/json-en.html)) file. The version schema of *JSON* files enables the easy export of *.ipynb*  notebooks to many open standard output format such as *HTML*, [*LaTeX*](https://latex-project.org/), *markdown*, *Python*, *presentation slides*, or *PDF*. 
The *Jupyter* kernels support the three core programming languages ***Ju**lia*, ***Pyt**hon* and ***R***, and many more (currently 49)  *Jupyter* kernels for other programming languages exist. 

1. Open *Anaconda Navigator* and make sure to be in the *Home* tab.
1. Look for *JupyterLab* (also) and click on the *Install* button (if already installed, there is only a *Launch* button).
1. After successful installation, open *JupyterLab*, by clicking on the *Launch* button.
1. *JupyterLab* opens in the default web browser, where *Jupyter* notebooks (*.ipynb*) or *Python* files can be created and edited.

{% include tip.html content="Get familiar with *JupyterLab*, by creating files, adding new *Markdown* or *Python* cells and `Run`ning cells. The essentials of *markdown* are explained on the [Markdown and Documentation](hy_documentation.html#markdown) page (short read). Learning *Python* is more than a short read and the [*Python* (basics)](python.html) walks you through the course contents to learn *Python* (takes time)." %}

{% include note.html content="*Anaconda Navigator* alternatively provides to install and launch the application *Jupyter Notebook*. However, *JupyterLab* is *Project Jupyter*'s next-generation user interface, which is more flexible and powerful. This is why this website builds on *JupyterLab* rather than the *Jupyter Notebook* app." %}




