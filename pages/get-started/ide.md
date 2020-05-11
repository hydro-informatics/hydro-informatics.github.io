---
title: Anaconda and Integrated Development Environments (IDEs)
keywords: IDEs, conda, Anaconda
summary: "Let's start at the very beginning ..."
sidebar: mydoc_sidebar
permalink: hy_ide.html
folder: get-started
---

## Anaconda {#anaconda}

{% include note.html content="[Anaconda](https://www.anaconda.com/distribution/) represents the baseline for many applications presented on this web site. It enables the built-in installation of programming languages such as *Python* and *R*, as well as *IDE*s such as [*PyCharm*](https://www.jetbrains.com/pycharm/) or [*Spyder*](https://www.spyder-ide.org/), and [*Jupyter Notebook (Lab)*](https://jupyter.org/)." %}

The very first step to get started consist in downloading and installing [Anaconda](https://www.anaconda.com/distribution/). In Windows, *Anaconda* ([download](https://docs.anaconda.com/anaconda/install/windows/)) should be installed in a *LOCAL* user folder (e.g., *C:\users\<your-user-name>\AppData\Local*). Linux or macOS users find download and installation instructions directly at the developers web site ([Linux installation](https://docs.anaconda.com/anaconda/install/linux/) and [macOS installation](https://docs.anaconda.com/anaconda/install/mac-os/)).

After the successful installation of *Anaconda*, *IDE*s for *Python* programming or *markdown* editing can be directly installed by launching the **Anaconda navigator**. **`conda`** environments can be created later on following the [instructions in the *Python (fundamentals)* section](hypy_install.html#conda-env).

## Install and setup an Integrated Development Environment (IDE) {#ide}
An IDE enables the definition of a project to use for example a specific [*Conda Environment*](https://docs.conda.io/) and it enables robust coding by pointing out issues directly in the code, even before it was executed once. Powerful IDEs go even further and provide assistance in documenting code with markdown (*.md* files) and direct pipes into *git* ([see section on the usage of *git*](hy_git.html)). *Jetbrains*'s [*PyCharm (Community Edition)*](https://www.jetbrains.com/pycharm/) is one of the best open-access IDEs for non-commercial use and good alternatives are [*Spyder IDE*](https://www.spyder-ide.org/) (for *Python*) or [*RStudio*](https://rstudio.com/) (*R* and *Python*). However, before launching any project in an IDE, the installation of an interpreter (e.g., *Python* or *R*) is necessary. The cooking recipe for setting up an IDE is:
 
 and it can be set up as follows to use conda environments:
1. Install interpreter (e.g., *Python Anaconda* according to the instructions in the [Python section](hypy_install.html)).
1. [Download](https://www.jetbrains.com/pycharm/), install and open an IDE  *PyCharm*
1. Click on `+ Create New Project`
1. A window will open - enter:
    - *Location* - Select a local directory for the project (e.g., *C:/hydro/project*)
    - *Project Interpreter* - Check the `Existing interpreter` box and select the above-installed [conda environment `geo-python`](#conda-env) (e.g., `C:\users\<your-user-name>\AppData\Local\Continuum\anaonda3\envs\`)
    - Click on the `Create` button.

All set - you are ready to work with *Python*, markdown (documentation), and [git](hy_git.html) now.

{% include note.html content="To learn more about how to define and use *conda* environments, go to the [*Python (basics)* > *Install Python*](hypy_install.html#ide-setup) pages." %}

{% include note.html content="These pages are written with [*Jupyter Lab*](https://jupyter.org/), which is suitable to follow the course contents. However, *IDE*s such as *PyCharm* or *Spyder* are more suitable to setup projects." %}



