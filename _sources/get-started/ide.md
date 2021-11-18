(sec-ide)=
# Integrated Development Environments (IDEs)

The teaching contents of this eBook build on so-called *Application Programming Interface*s **API**s) and *Integrated Development Environment*s (**IDE**s).

An **API** represents a computing interface that enables interactions between multiple software intermediaries. Modular programming becomes easy with an API because it systematically hides complex information that is not necessarily needed to write code according to industry standards. For instance, an API can define the interface between an application (such as Python or *Word*) and an **Operating System** (**OS**) such as *Windows*, *Linux*, or *macOS* (also referred to as **platform**).

An **IDE** enables the definition of a project to use, for example, a specific Python environment, and it enables robust coding by pointing out issues directly in the code, even before it ran for the first time. Powerful IDEs go even further and assist in documenting code with markdown (*.md* files) and directly pipe into *git* (see the {ref}`chpt-git`).

```{admonition} Which IDE to choose?
:class: tip
The answer to this question depends on the platform you are using (e.g., *Windows* or *Linux*), your personal preferences, and your goals.

For writing Python software itself, the Author's preference is in general {ref}`Atom <install-atom>` (optionally and on Windows only: {ref}`PyCharm <pycharm>`). To test and run Python code (software) locally,  for ***Windows* users, the installation of {ref}`anaconda` is almost indispensable**. *Linux* users will be mostly fine with their system setup without the need to install *Anaconda* or *PyCharm*.

For code documentation, examples, and the best learning experience in the Python courses featured in this eBook, consider installing {ref}`jupyter` locally. *Windows* users find instructions in the {ref}`install-jupyter-windows` section. *Linux* users find instructions in the {ref}`install-jupyter-linux` section.

**Once you have an IDE installed, carefully read the {ref}`instructions for installing Python <install-python>`.**
```

(anaconda)=
# Anaconda

***Anaconda* is the favorite solution for** working with the Python tutorials in this eBook on **Windows**. *Linux* users may want to install the text and code editor {ref}`install-atom` and optionally {ref}`install-jupyter-linux`.

## Anaconda Navigator

```{admonition} Use Anaconda on Windows
Anaconda works well on Windows, but Linux (or also macOS) users will have a better experience with advanced text editors such as {ref}`Atom <install-atom>`.
```

*Anaconda* is a Python and *R* distribution that enables the usage of a couple of IDEs such as [*PyCharm*](https://www.jetbrains.com/pycharm/), [*Spyder*](https://www.spyder-ide.org/), or [*JupyterLab (Notebook)*](https://jupyter.org/).

The very first step to getting started with *Anaconda* consists in downloading and installing [*Anaconda*](https://www.anaconda.com/products/individual) where students may use the individual license for educational training purposes (note that a commercial license needs to be purchased for for-profit organizations). On Windows, *Anaconda* should be installed in the *LOCAL* user folder (e.g., *C:\users\<your-user-name>\AppData\Local*). *Linux* or *macOS* users find download and installation instructions directly at the developer's website, tailored for their specific distribution, even though they might be better of with {ref}`install-atom`.

After the successful installation of *Anaconda*, IDEs for Python programming or *markdown* editing can be directly installed by launching the **Anaconda navigator**. **`conda`** environments can be created later, following the instructions in the {ref}`conda-env` section.

## Miniconda

*Anaconda* may create large environments that require several gigabytes of storage. To install lightweight environments, use [Miniconda](https://docs.conda.io/en/latest/miniconda.html). *Miniconda* does not include *Anaconda Navigator* and to enable working with *Jupyter* notebooks (in *Windows*):

1. Click on *Start*.
1. Type `Anaconda Prompt` and hit enter (use *Miniconda3*). A *Terminal* window (black background) opens.
1. In *Anaconda prompt* type `conda install jupyter` and confirm with `y` when the *Terminal* asks `Proceed ([y]/n)?`.

To work with *Jupyter* notebooks (open, create, or modify), type `jupyter lab` (or `jupyter notebook`) in *Anaconda Prompt (Miniconda3)* and hit *Enter*. The *JupyterLab* application will open in the default web browser.

(pycharm)=
## PyCharm with Anaconda

*Jetbrains* [*PyCharm (Community Edition)*](https://www.jetbrains.com/pycharm/) is an open-access IDE for non-commercial use. Alternatives are [*Spyder IDE*](https://www.spyder-ide.org/) (for Python) or [*RStudio*](https://rstudio.com/) (*R* and Python). However, before launching any project in an IDE, the installation of an interpreter (e.g., Python or *R*) is necessary (we already installed an interpreter with *Anaconda*).

*PyCharm* is available as an *Anaconda Navigator* (i.e., *Anaconda*'s graphical user interface) module. To enable *PyCharm* in *Anaconda*, download *PyCharm* from the [developer's website](https://www.jetbrains.com/pycharm/promo/anaconda/) and install *PyCharm*. A reboot may be required after the installation.

After the installation of *PyCharm* for *Anaconda*, open *Anaconda Navigator*:

1. Open *Anaconda Navigator* and make sure to be in the *Home* tab.
1. If the installation of *PyCharm* was successful, click on the *Launch* button to open *PyCharm*.
1. In *PyCharm* click on `+ Create New Project`
1. Option 1 (preferred): Use the [developer's up-to-date documentation](https://docs.anaconda.com/anaconda/user-guide/tasks/pycharm/) for setting up *PyCharm* with *Anaconda*.
1. Option 2 (quick to read, but may fail): A window will open - enter:
  - *Location* - Select a local directory for the project (e.g., *C:/hydro/project*)
  - *Project Interpreter* - Check the `Existing interpreter` box and select an existing interpreter.
  - Click on the `Create` button.

All set - you are ready to edit Python (`.py`), markdown (`.md` for documentation), and other file types.

```{admonition} Finalize the Installation of Python
:class: tip
**Carefully read the {ref}`instructions for installing Python <install-python>` on your platform.**
```

(jupyter)=
# JupyterLab

*Jupyter* is a spin-off of [IPython](https://ipython.org/), which is "a rich architecture for interactive computing".

*JupyterLab* is a product of the nonprofit organization [*Project Jupyter*](https://jupyter.org/), which develops "open-source software, open-standards, and services for interactive computing across dozens of programming languages". A *Jupyter* notebook (*.ipynb* file) enables the combination of markdown text blocks with executable code blocks. Essentially, a *Jupyter* notebook is a *JavaScript Object Notation* ([*JSON*](https://www.json.org/json-en.html) file. The structure of *JSON* files enables the easy export of *.ipynb*  notebooks to many other open standard output formats such as *HTML*, [*LaTeX*](https://latex-project.org/), *markdown*, Python, *presentation slides*, or *PDF*.
The *Jupyter* kernels support the three core programming languages **Ju**lia, **Pyt**hon and **R**, and many more *Jupyter* kernels (currently 49) for other programming languages exist.


```{admonition} Working with Jupyter
:class: tip
Get familiar with *JupyterLab*, by creating files, adding new *Markdown* or Python cells, and running cells. The essentials of *markdown* are explained in the {ref}`Markdown <markdown>` section (short read). Learning Python is more than a short read and the {ref}`Python Basics chapter <about-python>` provides some insights (takes time).
```

(install-jupyter-windows)=
## Jupyter on Windows

*Anaconda Navigator* alternatively provides the application *Jupyter Notebook*. However, *JupyterLab* is the *Project Jupyter*'s next-generation user interface, which is more flexible and powerful. This is why this website refers to *JupyterLab* rather than the *Jupyter Notebook* app. The following sections explain how to install it on your Windows computer, either by using the graphical user interface of *Anaconda Navigator*, or the conda prompt command line (recommended).

### Via Anaconda Navigator

1. Open *Anaconda Navigator* and make sure to be in the *Home* tab.
1. Look for *JupyterLab* and click on the *Install* button (if already installed, there is only a *Launch* button visible).
1. After successful installation, open *JupyterLab*, by clicking on the *Launch* button.
1. *JupyterLab* opens in the default web browser, where *Jupyter* notebooks (*.ipynb*) or Python files can be created and edited.


### Via Anaconda Prompt (Recommended)

Open *Anaconda Prompt*, which represents a *Terminal* window with a black background and a blinking cursor.

If you are working with *Miniconda*, install the *Jupyter Notebook* app by typing `conda install jupyter` and confirm with `y` when *Anaconda Prompt* asks `Proceed ([y]/n)?`.

To **start** *JupyterLab* and open, create, or modify *Jupyter* notebooks, type:

```
jupyter lab
```

If the command fails, try either `jupyter-lab` or start Jupyter notebook by typing `jupyter notebook`. The *Jupyter Notebook* application will open in the default webbrowser.

### Extensions and Spellchecker

Many additional features for *JupyterLab* are available through [*nbextensions*](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html), which can be installed through *Anaconda Prompt*:

```
conda install -c conda-forge jupyter_contrib_nbextensions
```

When reading through the Python tutorials on this website, you will probably find one or another spelling mistake (please <a href="mailto:sebastian.schwindt[AT]iws.uni-stuttgart.de?subject=HYPY%20Spelling%20mistake">report mistakes!</a>). In particular, the Python sections may be affected because they were created with *Jupyter Lab*, where there is no spell checker pre-installed. To avoid at least the most unpleasant errors you can install a spellchecker in *jupyter*. One solution is to install [*@ijmbbarr*](https://github.com/ijmbarr/jupyterlab_spellchecker)s spellchecker, which requires installing *nodejs* (through *Anaconda Prompt* and in addition to *nbextensions*):

```
conda install -c conda-forge nodejs
jupyter labextension install @ijmbarr/jupyterlab_spellchecker
```

The spellchecker uses [Typo.js](https://github.com/cfinke/Typo.js) as a dictionary and only identifies misspelled words without proposing corrections. More details on spellchecking are available at the [developer's website](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/spellchecker/README.html).

In the case that several warning messages occur when starting *JupyterLab* (such as `[W 18:49:22.283 NotebookApp] Config option template_path not recognized by LenvsHTMLExporter. Did you mean one of: template_file, template_name, template_paths?`), downgrade *jupyter notebook* from version 6.x to 5.6.1 (there is currently an issue with the `temp_path` variable):

```
conda install "nbconvert=5.6.1"
```

(install-jupyter-linux)=
## Jupyter on Linux

To install *JupyterLab* on *Linux*, open *Terminal* and make sure that `pip`/`pip3` is installed:

```
sudo apt install python3 python3-pip python3-venv
```

Export the user-level `bin` to the `PATH` environment and install JupyterLab in the user space with the following commands:

```
export PATH="$HOME/.local/bin:$PATH"
pip install --user jupyterlab
```

```{note}
It might be necessary to replace `pip` with `pip3` (depending on the *Linux* distribution).
```

To start *JupyterLab* tap:

```
jupyter-lab
```

The command `jupyter-lab` starts a localhost server that runs *JupyterLab*, which will open up in a web browser like an interactive website.

```{warning}
Closing *Terminal* will also terminate the localhost that runs *JupyterLab*. Thus, do not close *Terminal* as long as you are working with *JupyterLab*, in particular, when there are unsaved books.
```

(install-atom)=
# Atom

*Atom* is a hackable text editor that is compatible with almost any programming language. While its bare installation has little functionality, the omni-compatibility can be enabled by installing desired packages (e.g., for Python, *Markdown*, or *LaTex*). Another big advantage of *Atom* is the availability of powerful spell checker packages.

## Installation

````{tabbed} Linux
**Linux** users find installers for various distributions at [atom.io](https://atom.io/). **Debian** (**Ubuntu**), **Red Hat** / **CentOS**, **Fedora**, and **SUSE** find easy installation guides at [https://flight-manual.atom.io](https://flight-manual.atom.io/getting-started/sections/installing-atom/).

The short version for **Debian** (**Ubuntu**) is:

* Add the *Atom* package repository to the system:

```
wget -qO - https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'
sudo apt update
```

* Then install *Atom*:

```
sudo apt install atom
```
````

````{tabbed} Windows
**Windows** users can download *Atom* from [atom.io](https://atom.io/) and install the executable.
````



(atom-packages)=
## Atom Packages

### Get Useful Atom Packages

To install packages:

* *Windows* users go to **File** > **Settings** > **+ Install**
* *Linux* users go to **Edit** > **Preferences** > **+ Install**

The following (additional) packages are useful for working with the contents of this eBook:

* `ide-python` provides language support for Python code
* `language-markdown` (optional) for writing documentations with [Markdown](https://daringfireball.net/projects/markdown/).
* `language-restructuredtext` (optional) for writing documentations with [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html).
* `language-tex` (optional) to write reports or presentations with [LaTex](https://www.latex-project.org/)
* `platformio-ide-terminal` (*platformio-ide*) adds a terminal window to *Atom*
* `python-docstring` facilitates inline documentation of Python code
* `python-requirements` enables to install required packages for running Python code
* `script` enables to run Python and many other code types ([read the docs](https://atom.io/packages/script)); after the installation, running a code (Python) file can be triggered by clicking on the **Packages** top menu > **Script**  > **Run Script**.

### Spell Checking

The default-installed **spell-check** package runs basic spellcheck for plain text, GitHub Markdown, AsciiDoc, and reStructuredText by using the system's default dictionaries.

If `spell-check` is not revising the current document, click on the document in question in *Atom* and open the *Command Palette* (*Windows*:  press `CTRL` + `Shift` + `P`). In the *Command Palette* type `Editor: Log Cursor Scope`. A pop-up window will show the current scope. To make sure that the current scope is checked by `spell-check`, open the *Atom* *Settings* (on *Windows*) or *Preferences* (on *Linux*) and find the `spell-check` package. Click on **Settings** and find the **Grammars** field. Click in the *Grammars* field and add the current scope here. Restart *Atom* to make sure that the changes are implemented.

*Debian Linux* users can install the *hunspell* package with support for many languages:

```
sudo apt install hunspell-en-gb
sudo apt install myspell-en-gb
```

Other packages enable spell checking for particular file formats:

* `linter` basic package for spell checkers
* `linter-spell` grammar and spell checking basis
* `linter-markdown` spell checks *Markdown* files
* `linter-spell-rst` spell checks *reStructuredText*

```{warning}
`linter *` packages might conflict with `spell-check`. If your files are not spell-checked anymore after installing `linter *` , roll back the installation of `linter` and reset `spell-check`.
```

Read more at [atom.io](https://atom.io/packages/spell-check) for more information on other distributions and dictionaries.

(atom-python)=
## Usage with Python

```{admonition} Requirements
To enable Python compatibility, first, visit the {ref}`install-python` section and install {{ ft_url }} for your system (i.e., either in a virtual or conda environment).
```

````{tabbed} Linux

Open Terminal and activate the environment where `flusstools` is installed. For instance, if `flusstools` is installed in a virtual environment called `vflussenv` that lives in the user home directory (`/home/USER/`) according to the Python installation instructions in this eBook (see {ref}`pip quick guide <pip-quick>`), activate the environment as follows:

```
cd ~
source vflussenv/bin/activate
```

````

````{tabbed} Windows
Open Anaconda Prompt and activate `flussenv` (given that {{ ft_url }} is installed according to the {ref}`conda quick guide <conda-quick>`):

```
conda activate flussenv
```
````

Then, start *Atom* in the (pip or conda) environment through Terminal (Linux) or Anaconda Prompt (Windows):

```
atom
```

*Atom* should open and provide the option to select a folder where a Python project will live or is already living. After selecting a folder, start editing your Python (`.py`) files. For running Python scripts, there are two options:


````{tabbed} Option 1: Use Script Package
 first set up the *Script* package:

* Make sure that the [script package](https://atom.io/packages/script) is installed.
* Configure the *Srcipt* packge in *Atom* by clicking on **Packages** > **Configure Script** (`Alt` + `Ctrl` + `Shift` + `O`):
  * In the **Command** field enter `python` (or `python3`).
  * Click on **Save as profile** and enter a prilfe name (e.g. `flussprofile`).

To run a Python script:

* Either go to **Packages** > **Script** > **Run with profile** and select **flussprofile**
* Or press `Alt` + `Ctrl` + `Shift` + `B`
````
````{tabbed} Option 2: Use atom-python-virtualenv Package
Make sure to install the `atom-python-virtualenv` package (see the section on {ref}`installing Atom packages <atom-packages>`) and select `vflussenv` from the status bar at the bottom of the window as indicated in the below figure.

```{image} ../img/python/atom-enable-env.png
```
````

## More Console Options

While the `script` package enables running a Python script, it may be desirable to have a built-in Python console window running in *Atom*. To this end, the `platformio-ide-terminal` package tweaks into the system's default terminal (*Terminal* on *Linux* or *PowerShell* on *Windows 10*), which can run an existing installation of Python (i.e., Python must be installed on the system in some form). Depending on your platform, follow the instructions in the {ref}`atom-setup` section.
