---
title: Introduction to git
keywords: git
summary: "This chapter explains the basics of git usage"
sidebar: mydoc_sidebar
permalink: hypy_git.html
folder: part1
---

# Requirements<a name="req"></a>
Codes are designed for being used with [Python Anaconda](https://www.anaconda.com/distribution/). Python Anaconda should be installed in a *LOCAL* user folder (e.g., *C:\users\<your-user-name>\AppData\Local*) to use batchfiles that launch conda environments outside of IDEs (currently only provided for Windows and Unix-based solutions will be available in the future).
 
Use the provided `environment.yml` file to create a conda environment:

1. Open Anaconda prompt
1. Navigate to the download directory of the course material (use [`cd`](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands))
1. Enter `conda env create -f environment.yml` (this creates the environment `geopython`)
1. [OPTIONAL] To install more packages, type (in Anaconda prompt):
    - `conda activate geo-python`
    - `conda install PACKAGE_NAME`


## Usage of git and download course materials<a name="dl"></a>
The materials provided on the github pages is best downloaded and updated using *git*-able environments (e.g., *PyCharm*'s Community Edition or [*Git Bash*](https://git-scm.com/downloads)). Updates are tricky when materials are downloaded as *zip* file.

### Pure download
*GitHub* provides detailed descriptions and standard procedures to work with their repositories ([read more](https://help.github.com/en/articles/cloning-a-repository)). The following "recipe" guides through the first time installation (cloning) of *Hy2Opt:

1. Open *Git Bash*
2. Type `cd "D:/Target/Directory/"` to change to the target installation directory (recommended: `cd "D:/Python/hy2opt/"`). If the directory does not exist, it can be created in the system explorer (right-click in empty space > `New >` > `Folder`).
3. Clone the repository: `git clone https://github.com/sschwindt/course-<sn>]` (replace `<sn>` with the course short name; e.g., `dm`)

Done. Close *Git Bash* and start working with the materials.

### Update (re- pull) with *git* <a name="update"></a>

*git* (within *Git Bash* or other git-able IDEs such as *PyCharm*) is the only option to update local copies of the course material consistently.

In a *git*-able terminal do the following:
1. Go to the local directory of the course material: `cd "D:/Python/course-<dm>"` (or wherever the material was cloned).
2. Check the current status: `git status`
3. Pull changes: `git pull`

Please note that merge errors may occur when changes were made in the local copy. In this case, *git* will guide through a manual merge process.

### Push to other repositories<a name="push"></a>
To update (add, commit and push) local changes to a remote repository, make sure to be the remote repository owner or a contributor. 

***