(chpt-git)=
# Version Control : git

## The Concept

**git is a fast, scalable, distributed revision (version) control system**, originally developed by *Linus Torvalds*  ([read more about the git kernel](https://git.kernel.org/)). *git* enables to coordinate work among collaborators beyond programming, in any set of files. Its support of non-linear workflows, speed, and data integrity make git an indispensable tool in many industries and research. Before starting to read this *git* tutorial, have a look at the schematic functioning of repositories hosted with *git*.

```{figure} ../img/git-scheme.png
:alt: git-scheme

The concept of git and basic vocabulary. The REMOTE frame is online (i.e., someone else's computer) and the LOCAL frame is what happens on a personal computer, which is connected to the internet. Repositories can be newly created or forked remotely. Remote repositories can be cloned locally, modified locally, and local changes can be pushed to a remote repository. Collaborators want to make sure to regularly pull changes of a remote repository. Working with and on different branches becomes increasingly important with the number of developers and for the moment we just need to remember that we start working in the master branch (i.e., upstream origin / HEAD = main).
```

(dl)=
## Install git
The materials provided with this eBook are best downloaded and updated using *git*-able environments (avoid downloading materials as *zip* file).

````{tabbed} Linux
Although git is an integral feature of most Linux distributions, Debian users might still need to install it. For this purpse, open Terminal and tap:
```
sudo apt install git
```
````

````{tabbed} Windows
Download and install [Git Bash](https://git-scm.com/downloads) and use it for example [PyCharm's Community Edition](https://www.jetbrains.com/pycharm/) or [Atom](https://atom.io).
````

````{tabbed} macOS
macOS users may use [Homebrew](https://developer.apple.com/xcode/) for installing git, but there are other options, such as [Xcode](https://developer.apple.com/xcode/).

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

Ultimately, Homewbrew provides many more packages, which are essentially useful for developers, such as [ruby](https://formulae.brew.sh/formula/ruby) or [React](https://formulae.brew.sh/formula/react-native-cli) ([go to the full package list](https://formulae.brew.sh/formula/)).

Read more installation instructions and about options for git on macOS at [https://git-scm.com/download/mac](https://git-scm.com/download/mac).

````

The repositories for this course are mainly hosted on *GitHub*. There are many other *git* service providers out there, such as [GitLab](https://gitlab.com/pages), [plan.io](https://plan.io/knowledge-management/), or [BitBucket](https://bitbucket.org/).


## Create a Repository

To create a *git* repository, make sure to have access to a *git* provider. The most popular way to get access to a *git*-able server is to register with one on the long list of popular *git* providers.

```{admonition} Students of the University of Stuttgart
:class: note
Students of the University of Stuttgart may use *GitHub* using their institutional ID (e.g., `st9009133` ) through the [TIK's GitHub account and login page](https://github.tik.uni-stuttgart.de/login).
```

## Clone (Download) a Repository

*GitHub* provides detailed descriptions and standard procedures to work with their repositories ([read more](https://help.github.com/en/articles/cloning-a-repository)). The following "recipe" guides through the first time download of *git* materials

1. Open your favorite *git*-able command line:
    * *Windows* Options: *PowerShell*, *Git Bash*, or *Command Prompt*
    * *Linux*: *Terminal*
1. Clone the course repository (change materials according to the course attended):<br> `git clone https://github.com/hydro-informatics/materials`  (or whatever repository you want to clone)

Done.

(update)=
## Pull (Update/Re-Download) a Local Repository

*git* (within *Git Bash*, *PyCharm*, or *Terminal*) is the only option to update local copies of a remote repository consistently. To do so, open one of the above mention *git*-able command lines and do the following:

1. Go to the local directory of the repository with the [`cd`](https://en.wikipedia.org/wiki/Cd_(command)) command (e.g., `materials`):<br> `cd "D:/Python/materials/"` (or wherever `materials` was cloned).
1. `git status` - shows the modifications made.
1.  Merge errors may occur when changes were made in the local copy. To avoid merge errors, type: <br> `git pull --rebase` - if locally edited scripts were modified remotely since the last pull, this will prompt issues and highlight problematic sections with `>>>` ). Manually open concerned files and resolve the issues (delete invalid `>>>` highlights).
1. `git push`

Done.


(push)=
## Update a Remote Repository (Push Local Changes)

After editing files in a repository locally, *add* - *commit* - *push* (in that order) your edits to the remote copy of the repository with version control. To *add* - *commit* - *push* local changes to a remote repository, make sure to be the remote repository owner or a contributor. Then open a *git*-able terminal and type:
1. `git status` - this shows the modifications made.
1. If the status looks OK with the consciously made changes, type `git add .` <br>Optionally, if only single files were changed, use `git add filename.py` instead. Best solution: use a local [.gitignore file](https://help.github.com/en/github/using-git/ignoring-files).
1. Commit changes `git commit -m "Leave a message"` - leave a significant and precise short message.
1. `git pull --rebase` - if locally edited scripts were modified remotely since the last pull, this will prompt issues and highlight problematic sections with `>>>`). Manually open concerned files and resolve the issues (delete invalid `>>>` highlights).
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

```{admonition} Exercise
Practice *git* with the {ref}`markdown and git <git-exercise>` exercise.
```
