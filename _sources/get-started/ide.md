(sec-ide)=
# Integrated Development Environments (IDEs)

The teaching contents for programming in this eBook require so-called *Application Programming Interface*s **API**s) and *Integrated Development Environment*s (**IDE**s).

An **API** represents a computing interface that enables interactions between multiple software intermediaries. Modular programming becomes easy with an API because it systematically hides complex information that is not necessarily needed to write code according to industry standards. For instance, an API can define the interface between an application (such as Python or *Word*) and an **Operating System** (**OS**) such as *Windows*, *Linux*, or *macOS* (also referred to as **platform**).

An **IDE** enables the definition of a project to use, for example, a specific Python environment, and it enables robust coding by pointing out issues directly in the code, even before it runs for the first time. Powerful IDEs go even further and assist in documenting code with markdown (*.md* files) and directly pipe into *git* (see the {ref}`chpt-git`).

```{admonition} Which IDE to choose?
:class: tip
The answer to this question depends on the platform you are using (e.g., *Windows* or *Linux*), your personal preferences, and your goals.

For writing Python software itself, {ref}`PyCharm <pycharm>` is a powerful solution. In addition, {ref}`Jupyter <jupyter>` is a great tool for writing word-office-like documents with functional code examples. To test and run Python code (software) locally,  for ***Windows* users, the installation of {ref}`anaconda` is almost indispensable**. *Linux* users will be mostly fine with their system setup without the need to install *Anaconda*.

For code documentation, examples, and the best learning experience in the Python courses featured in this eBook, consider installing {ref}`jupyter` locally. *Windows* users find instructions in the {ref}`install-jupyter-windows` section. *Linux* users find instructions in the {ref}`install-jupyter-linux` section.

**Once you have an IDE installed, carefully read the {ref}`instructions for installing Python <install-python>`.**
```

(anaconda)=
# Anaconda

***Anaconda* is a powerful tool for managing Python environments on Windows. Linux users better use virtual environments** (read more in the chapter on {ref}`installing Python <install-python>`).

## Anaconda Navigator

*Anaconda* is a Python and *R* distribution that enables the usage of a couple of IDEs such as [PyCharm](https://www.jetbrains.com/pycharm/), [Spyder](https://www.spyder-ide.org/), or [JupyterLab (Notebook)](https://jupyter.org/).

The very first step to getting started with Anaconda consists in downloading and installing [Anaconda](https://www.anaconda.com/download) where students may use the individual license for educational training purposes (note that a commercial license needs to be purchased for for-profit organizations). On Windows, Anaconda should be installed in the *LOCAL* user folder (e.g., *C:\users\<your-user-name>\AppData\Local*). *Linux* or *macOS* users find download and installation instructions directly at the developer's website, tailored for their specific distribution, even though they might be better of with {ref}`virtual environments <pip-env>`.

After the successful installation of *Anaconda*, IDEs for Python programming or *markdown* editing can be directly installed by launching the **Anaconda navigator**. **`conda`** environments can be created later. Learn more about installing Anaconda (with Python) and this eBook's support package called {{ ft_url }} in the {ref}`Python conda quick guide <conda-quick>` section and in the video below.

```{admonition} Python Anaconda Installation Video on YouTube
:class: tip, dropdown
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/cbIPRGOUAVA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

## Miniconda

*Anaconda* may cause large environments that require several gigabytes of storage. To install lightweight environments, use [Miniconda](https://docs.conda.io/en/latest/miniconda.html). *Miniconda* does not include *Anaconda Navigator* and to enable working with *Jupyter* notebooks (in *Windows*):

1. Click on *Start*.
1. Type `Anaconda Prompt` and hit enter (use *Miniconda3*). A *Terminal* window (black background) opens.
1. In *Anaconda prompt* type `conda install jupyter` and confirm with `y` when the *Terminal* asks `Proceed ([y]/n)?`.

To work with *Jupyter* notebooks (open, create, or modify), type `jupyter lab` (or `jupyter notebook`) in *Anaconda Prompt (Miniconda3)* and hit *Enter*. The *JupyterLab* application will open in the default web browser.

(pycharm)=
## PyCharm

*Jetbrains* [*PyCharm*](https://www.jetbrains.com/pycharm/) is a powerful but proprietary IDE. Its usage is still free for non-commercial use in education. Alternatives are [*Spyder IDE*](https://www.spyder-ide.org/) (for Python) or [*RStudio*](https://rstudio.com/) (*R* and Python). However, before launching any project in an IDE, the installation of an interpreter (e.g., Python or *R*) is necessary (see chapter on {ref}`Python installation <install-python>`).

Get PyCharm from the [developer's website](https://www.jetbrains.com/pycharm/download/) or use it through Anaconda. For the educative training purposes provided in this eBook, you may be eligible to use the free education license. To use PyCharm with Anaconda, visit [https://docs.anaconda.com](https://docs.anaconda.com/free/anaconda/ide-tutorials/pycharm/).

(jupyter)=
# JupyterLab

*Jupyter* is a spin-off of [IPython](https://ipython.org/), which is "a rich architecture for interactive computing". *JupyterLab* is a product of the nonprofit organization [*Project Jupyter*](https://jupyter.org/), which develops "open-source software, open-standards, and services for interactive computing across dozens of programming languages". A *Jupyter* notebook (*.ipynb* file) enables the combination of markdown text blocks with executable code blocks. Essentially, a Jupyter Notebook is a *JavaScript Object Notation* ([JSON](https://www.json.org/json-en.html) file. The structure of JSON files enables the easy export of *.ipynb*  notebooks to many other open standard output formats such as HTML, [LaTeX](https://latex-project.org/), *Markdown*, Python, presentation slides, or *PDF*. The **Jupyter** kernels support the three core programming languages **Ju**lia, **Pyt**hon and **R**, and many more *Jupyter* kernels (currently 49) for other programming languages exist.


```{admonition} Working with Jupyter
:class: tip
Get familiar with *JupyterLab*, by creating files, adding new *Markdown* or Python cells, and running cells. The essentials of *markdown* are explained in the {ref}`Markdown <markdown>` section (short read). Learning Python is more than a short read and the {ref}`Python Basics chapter <about-python>` provides some insights (takes time).
```

(install-jupyter-windows)=
## Jupyter on Windows

Anaconda Navigator alternatively provides the application Jupyter Notebook. However, *JupyterLab* is the *Project Jupyter*'s next-generation user interface, which is more flexible and powerful. This is why this website refers to JupyterLab rather than the Jupyter Notebook app. The following sections explain how to install it on your Windows computer, either by using the graphical user interface of Anaconda Navigator, or the conda prompt command line (recommended).

### Via Anaconda Navigator

1. Open Anaconda Navigator and make sure to be in the *Home* tab.
1. Look for JupyterLab and click on the *Install* button (if already installed, there is only a *Launch* button visible).
1. After successful installation, open JupyterLab, by clicking on the *Launch* button.
1. JupyterLab opens in the default web browser, where Jupyter notebooks (*.ipynb*) or Python files can be created and edited.


### Via Anaconda Prompt (Recommended)

Open Anaconda Prompt, which represents a Terminal window with a black background and a blinking cursor.

If you are working with *Miniconda*, install the Jupyter Notebook app by typing `conda install jupyter` and confirm with `y` when Anaconda Prompt asks `Proceed ([y]/n)?`.

To **start** JupyterLab and open, create, or modify Jupyter notebooks, type:

```
jupyter lab
```

If the command fails, try either `jupyter-lab` or start Jupyter notebook by typing `jupyter notebook`. The *Jupyter Notebook* application will open in the default webbrowser.

### Extensions and Spellchecker

Many additional features for JupyterLab are available through [*nbextensions*](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html), which can be installed through Anaconda Prompt:

```
conda install -c conda-forge jupyter_contrib_nbextensions
```

When reading through the Python tutorials on this website, you will probably find one or another spelling mistake (please <a href="mailto:sebastian.schwindt[AT]iws.uni-stuttgart.de?subject=hydroinformatics%20spelling%20mistake">report mistakes!</a>). In particular, the Python sections may be affected because they were created with JupyterLab, where there is no spell checker pre-installed. To avoid at least the most unpleasant errors you can install a spellchecker in Jupyter. One solution is to install [@ijmbbarr](https://github.com/ijmbarr/jupyterlab_spellchecker)s spellchecker, which requires installing *nodejs* (through Anaconda Prompt and in addition to *nbextensions*):

```
conda install -c conda-forge nodejs
jupyter labextension install @ijmbarr/jupyterlab_spellchecker
```

The spellchecker uses [Typo.js](https://github.com/cfinke/Typo.js) as a dictionary and only identifies misspelled words without proposing corrections. More details on spellchecking are available at the [developer's website](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/spellchecker/README.html).

In the case that several warning messages occur when starting JupyterLab (such as `[W 18:49:22.283 NotebookApp] Config option template_path not recognized by LenvsHTMLExporter. Did you mean one of: template_file, template_name, template_paths?`), downgrade Jupyter Notebook from version 6.x to 5.6.1 (there is currently an issue with the `temp_path` variable):

```
conda install "nbconvert=5.6.1"
```

(install-jupyter-linux)=
## Jupyter on Linux

To install JupyterLab on Linux, open Terminal and make sure that `pip`/`pip3` is installed:

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

To start JupyterLab tap:

```
jupyter-lab
```

The command `jupyter-lab` starts a localhost server that runs JupyterLab, which will open up in a web browser like an interactive website.

```{warning}
Closing *Terminal* will also terminate the localhost that runs JupyterLab. Thus, do not close Terminal as long as you are working with JupyterLab, in particular, when there are unsaved books.
```

## A Debugger for Jupyter

To better understand and troubleshoot code crashes, a debugger represents a great relief. Unfortunately, debugging in Jupyter can cause some headache in the absence of an inherent debugging tool. To get a debugger working with Jupyter, check out [this blog entry from Jupyter Project](https://blog.jupyter.org/a-visual-debugger-for-jupyter-914e61716559).


(install-sublime)=
# Sublime

Sublime is one of the most popular editors for multiple (computer) languages. However, it is commercial software that is only free to use during an evaluation period without time limit. Read more about it at [sublimetext.com](https://www.sublimetext.com).

To install it on Debian Linux platforms, open Terminal and tap (source: https://www.sublimetext.com/docs):

```
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/sublimehq-archive.gpg
```

Then select the stable channel (the dev channel has more features but also more bugs):

```
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
```

Finally, update `apt` and install Sublime:

```
sudo apt update
sudo apt install sublime-text
```

If an error message occurs, make sure `apt` works with `https` sources:

```
sudo apt install apt-transport-https
```

When working with sublime, consider using an advanced spell check package, such as [LanguageTool](https://packagecontrol.io/packages/LanguageTool). More useful packages for sublime can be found at [packagecontrol.io](https://packagecontrol.io). Packages can also be found by hitting the `CTRL` + `Shift` + `P` keys (in Sublime) to open *Package Control*. Then, type `install` and enter the name of the package you are looking for in the box.

To enable modification of user settings, go to **Preferences** (top menu bar) > **Settings** and save the opening settings file either as `~./config/sublime-text/Packages/Default/Preferences.sublime-settings` (recommended for first-time saving) or  `~./config/sublime-text/Packages/User/Preferences.sublime-settings`. Then, edit the desired settings: for instance, look for `spell_check` and set it to `true` to default-enable spell checking. Save the `.sublime-settings` file to apply changes.

