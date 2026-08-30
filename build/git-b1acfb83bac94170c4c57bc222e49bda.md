---
description: Comprehensive git version control tutorial covering installation, repositories, branching, committing, pushing, and collaborative workflows for engineers and scientists.
---

(chpt-git)=
# Version Control : git

## The Concept

**git is a fast, scalable, distributed revision (version) control system**, originally developed by *Linus Torvalds* ([read more about the git kernel](https://git.kernel.org/)). *git* enables coordinating work among collaborators beyond programming, in any set of files. Its support of non-linear workflows, speed, and data integrity makes git an indispensable tool in many industries and research. Before starting to read this *git* tutorial, have a look at the schematic functioning of repositories hosted with *git*.

```{figure} ../img/git-scheme.png
:alt: git-scheme

The concept of git and basic vocabulary. The REMOTE frame is online (i.e., someone else's computer) and the LOCAL frame is what happens on a personal computer, which is connected to the internet. Repositories can be newly created or forked remotely. Remote repositories can be cloned locally, modified locally, and local changes can be pushed to a remote repository. Collaborators want to make sure to regularly pull changes of a remote repository. Working with and on different branches becomes increasingly important with the number of developers (see the section on collaboration and branches below) and for the moment we just need to remember that we start working in the main branch (i.e., upstream origin / HEAD = main).
```

(dl)=
## Install git
The materials provided with this eBook are best downloaded and updated using *git*-able environments (avoid downloading materials as *zip* file).

`````{tab-set}
````{tab-item} Linux
Although git is an integral feature of most Linux distributions, Debian users might still need to install it. For this purpose, open Terminal and tap:
```
sudo apt install git
```
````

````{tab-item} Windows
Download and install [Git Bash](https://git-scm.com/downloads) and use it together with an IDE such as [PyCharm's Community Edition](https://www.jetbrains.com/pycharm/) or [VS Code](https://code.visualstudio.com/).
````

````{tab-item} macOS
macOS users may use [Homebrew](https://brew.sh/) for installing git, but there are other options, such as [Xcode](https://developer.apple.com/xcode/).

To use Homebrew for installing git, start with installing Homebrew through the [macOS Terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac):

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The installation of Homebrew may take a while. After the installation, make sure to export the required PATH variable (copy line-by-line):

```
echo 'eval $(/opt/homebrew/bin/brew shellenv)' >> /Users/$USER/.zprofile
eval $(/opt/homebrew/bin/brew shellenv)
```

It might be possible that the paths in the above commands need to be adapted to the directories that the Homebrew installer prompts at the end of its installation.

Finally, install git with Homebrew:

```
brew install git
```

Ultimately, Homebrew provides many more packages, which are essentially useful for developers, such as [ruby](https://formulae.brew.sh/formula/ruby) or [React](https://formulae.brew.sh/formula/react-native-cli) ([go to the full package list](https://formulae.brew.sh/formula/)).

Read more installation instructions and about options for git on macOS at [https://git-scm.com/download/mac](https://git-scm.com/download/mac).

````
`````

The repositories for this course are mainly hosted on *GitHub*. There are many other *git* service providers out there, such as [GitLab](https://gitlab.com/), [plan.io](https://plan.io/knowledge-management/), or [BitBucket](https://bitbucket.org/).


## Create a Repository

To create a *git* repository, make sure to have access to a *git* provider. The most popular way to get access to a *git*-able server is to register with one on the long list of popular *git* providers.

```{admonition} Students of the University of Stuttgart
:class: note
Students of the University of Stuttgart may use *GitHub* using their institutional ID (e.g., `st9009133` ) through the [TIK's GitHub account and login page](https://github.tik.uni-stuttgart.de/login).
```

## Clone (Download) a Repository

*GitHub* provides detailed descriptions and standard procedures to work with their repositories ([read more](https://help.github.com/en/articles/cloning-a-repository)). The following "recipe" guides through the first-time download of *git* materials:

1. Open your favorite *git*-able command line:
    * *Windows* Options: *PowerShell*, *Git Bash*, or *Command Prompt*
    * *Linux*: *Terminal*
1. Clone the course repository (change materials according to the course attended):<br> `git clone https://github.com/hydro-informatics/materials`  (or whatever repository you want to clone)

Done.

(update)=
## Pull (Update/Re-Download) a Local Repository

*git* (within *Git Bash*, *PyCharm*, or *Terminal*) is the only option to update local copies of a remote repository consistently. To do so, open one of the above-mentioned *git*-able command lines and do the following:

1. Go to the local directory of the repository with the [`cd`](https://en.wikipedia.org/wiki/Cd_(command)) command (e.g., `materials`):<br> `cd "D:/Python/materials/"` (or wherever `materials` was cloned).
1. `git status` - shows the modifications made.
1. Merge conflicts may occur when changes were made in the local copy. To keep the local history linear, type: <br> `git pull --rebase` - if locally edited files were modified remotely since the last pull, *git* will highlight problematic (conflicting) sections with `<<<<<<<`, `=======`, and `>>>>>>>` markers. Manually open the concerned files, resolve the conflicts, and delete the invalid conflict markers. Then mark the files as resolved with `git add FILENAME` and finalize with `git rebase --continue`.

Done.


(push)=
## Update a Remote Repository (Push Local Changes)

After editing files in a repository locally, *add* - *commit* - *push* (in that order) your edits to the remote copy of the repository with version control. To *add* - *commit* - *push* local changes to a remote repository, make sure to be the remote repository owner or a contributor. Then open a *git*-able terminal and type:
1. `git status` - this shows the modifications made.
1. If the status only lists consciously made changes, type `git add .` <br>Alternatively, if only single files were changed, use `git add filename.py` instead. Best practice: exclude files that should never be tracked (e.g., temporary or large binary files) with a local [.gitignore file](https://help.github.com/en/github/using-git/ignoring-files).
1. Commit the changes with `git commit -m "Leave a message"` - leave a significant and precise short message (e.g., `"fix typos in flow calculator"`).
1. `git pull --rebase` - if locally edited files were modified remotely since the last pull, *git* will highlight problematic (conflicting) sections with `<<<<<<<`, `=======`, and `>>>>>>>` markers. Manually open the concerned files, resolve the conflicts, delete the invalid conflict markers, then run `git add FILENAME` and `git rebase --continue`.
1. `git push`

````{admonition} Summary for updating a repository
:class: tip
Tap the following in Terminal or GitBash to upload all modifications in a local repository to the remote repository (make sure to know in which folder your repository is located on your computer - this defines what you need to enter for `/change-directory-to/repository/`):

```
cd /change-directory-to/repository/
git status
git add .
git commit -m "Leave a commit message"
git pull --rebase
git push
```
````

If any error occurs, carefully read why the error occurred and follow the instructions for troubleshooting (e.g., for setting up your user configuration with [git config --global user.email "email@example.com"](https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/managing-email-preferences/setting-your-commit-email-address#setting-your-commit-email-address-in-git)). You may ignore warning messages regarding line-end formats (*WARNING ... LF endings ...*) for most applications presented in this eBook.

(collaboration)=
## Collaboration & Branches

As soon as more than one person works on a repository (or one person works on more than one feature), committing everything directly to the `main` branch becomes error-prone. Best practice is to keep `main` always in a working state and to develop new features, fixes, or experiments on dedicated **branches**. A branch is an independent line of development that starts as a copy of another branch (typically `main`) and can later be merged back.

### Create a Branch

To create a new branch and switch to it, open a *git*-able terminal in the local repository and type:

1. `git switch main` - make sure to start from the `main` branch (older *git* versions require `git checkout main`).
1. `git pull` - update the local `main` branch to avoid branching off an outdated state.
1. `git switch -c fix-hydraulics-chapter` - create and directly switch to a new branch (here called `fix-hydraulics-chapter`; older *git* versions require `git checkout -b fix-hydraulics-chapter`). Use short, descriptive branch names, such as `fix-typos-git-chapter` or `feature-sediment-transport`.

`git branch` lists all local branches and marks the currently active branch with a `*`. Switch between existing branches with `git switch BRANCH-NAME`.

### Modify (Work on) a Branch

Working on a branch is exactly the same *add* - *commit* - *push* workflow as described in the {ref}`push` section, with one difference: the first push must tell the remote repository about the new branch. Thus:

1. Edit files, then `git status` and `git add .` (or `git add filename.py`).
1. `git commit -m "Leave a message"` - commit small, coherent units of work rather than one giant commit at the end.
1. `git push -u origin fix-hydraulics-chapter` - the `-u` (upstream) flag links the local branch to the remote branch, so that all later updates only require a plain `git push`.

To keep a long-living branch up to date with ongoing developments in `main`, regularly type (with the feature branch active):

```
git fetch origin
git merge origin/main
```

Resolve possible conflicts as described in the {ref}`update` section (here, conclude with `git commit` rather than `git rebase --continue`).

### Comment and Review (Pull Requests)

Directly merging an own branch without any review works for solo projects, but in a team, best practice is to open a **pull request** (called *merge request* on *GitLab*). A pull request is a proposal to merge one branch into another and constitutes the central place for commenting on code:

1. Push the branch to the remote repository (see above).
1. On *GitHub*, the repository page will suggest **Compare & pull request** for recently pushed branches. Alternatively, go to the *Pull requests* tab and click on **New pull request**, then select `main` as *base* and the feature branch (e.g., `fix-hydraulics-chapter`) as *compare*.
1. Give the pull request a precise title and describe **what** was changed and **why**. Request a review from one or more collaborators (right menu on *GitHub*).
1. Reviewers can comment on the pull request as a whole (*Conversation* tab) or on individual lines of code (*Files changed* tab, hover over a line and click the `+` symbol). Line comments may also be bundled into a formal review with the verdicts *Comment*, *Approve*, or *Request changes*.
1. To address review comments, simply commit and push new changes to the same branch. The pull request updates automatically, and resolved discussions can be marked as such with the **Resolve conversation** button.

### Merge a Development Branch into main

Once the pull request is approved (and automated checks pass, if configured), apply the new developments to `main` by clicking the **Merge pull request** button on *GitHub*. In addition, *GitHub* offers *Squash and merge* (combines all branch commits into a single commit, which keeps the history of `main` tidy) and *Rebase and merge*. After merging, delete the branch remotely (*GitHub* suggests a **Delete branch** button) and locally:

```
git switch main
git pull
git branch -d fix-hydraulics-chapter
```

Without a *git* provider interface (e.g., for a purely local repository), a branch can also be merged manually:

1. `git switch main` - switch to the target branch.
1. `git pull` - make sure the local `main` branch is up to date (skip for purely local repositories).
1. `git merge fix-hydraulics-chapter` - merge the development branch into `main`. Resolve possible conflicts (see the {ref}`update` section), then `git add` the resolved files and `git commit`.
1. `git push` - publish the updated `main` branch.
1. `git branch -d fix-hydraulics-chapter` - delete the merged branch (*git* refuses to `-d`-delete branches with unmerged changes, which is a useful safety net).

Done.

````{admonition} Summary of a branch lifecycle
:class: tip
```
git switch main
git pull
git switch -c feature-name
# edit files, then repeatedly:
git add .
git commit -m "Describe the change"
git push -u origin feature-name
# open a pull request on GitHub, discuss, revise, and merge; finally:
git switch main
git pull
git branch -d feature-name
```
````

```{admonition} Exercise
Practice *git* with the {ref}`markdown and git <git-exercise>` exercise.
```
