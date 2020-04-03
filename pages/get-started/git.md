---
title: Introduction to git
keywords: git
summary: "This chapter explains the basics of git usage"
sidebar: mydoc_sidebar
permalink: hy_git.html
folder: get-started
---


## Usage of git<a name="dl"></a>
The materials provided on these pages is best downloaded and updated using *git*-able environments (e.g., *PyCharm*'s Community Edition or [*Git Bash*](https://git-scm.com/downloads) - see the [installation](install) instructions). Updates are tricky when materials are downloaded as *zip* file.

### Download
*GitHub* provides detailed descriptions and standard procedures to work with their repositories ([read more](https://help.github.com/en/articles/cloning-a-repository)). The following "recipe" guides through the first time download of *git* materials

1. Open *PyCharm* (go to the `Terminal` tab, which is usually at the bottom of the window) or *Git Bash*
2. Go to the local target directory with the command `cd "D:/Target/Directory/"` to change to the target installation directory. If the directory does not exist, it can be created in the system explorer (right-click in empty space > `New` > `Folder`).
3. Clone the repository: `git clone https://github.com/hydro-informatics/materials]` (or whatever repository you want to clone)

Done.

### Update downloaded repository (re-pull local copy with *git*) <a name="update"></a>

*git* (within *Git Bash* or *PyCharm*) is the only option to update local copies of a remote repository consistently.  In a *git*-able terminal do the following:

1. Go to the local directory of the repository (e.g., `materiald`): `cd "D:/Python/materials/"` (or wherever `materials` was cloned).
1. `git status` - shows the modifications made.
1.  Merge errors may occur when changes were made in the local copy. To avoid merge errors, type: </br> `git pull --rebase` - if locally edited scripts were modified remotely since the last pull, this will prompt issues and highlight problematic section with `>>>`. Manually open concerned files and resolve the issues (delete invalid `>>>` highlights).
1. `git push`

Done.


### Update remote repositories (push local changes)<a name="push"></a>

After editing files in a repository locally, *add* - *commit* - *push* (in that order) your edits to the remote copy of the repository with version control. To *add* - *commit* - *push* local changes to a remote repository, make sure to be the remote repository owner or a contributor. Then open a *git*-able terminal and type:
1. `git status` - this shows the modifications made.
1. If the status seems OK with the consciously made changes, type `git add .`; if only single files were changed, use `git add filename.py` instead. Best solution: use a local [.gitignore file](https://help.github.com/en/github/using-git/ignoring-files).
1. Commit changes `git commit -m "Leave a message"` - leave a significant and precise short message.
1. `git pull --rebase` - if locally edited scripts were modified remotely since the last pull, this will prompt issues and highlight problematic section with `>>>`. Manually open concerned files and resolve the issues (delete invalid `>>>` highlights).
1. `git push`

Done.

