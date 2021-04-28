# Debugging Anaconda

Sometimes packages will not install as wanted (resulting in import errors, *Anaconda Navigator* is not behaving as expected or does not start up at all. This page summarizes remedies for such problems.

## *Anaconda Navigator* does not start up

The most common problems for *Anaconda* not starting up are listed in the [developer's docs](https://docs.anaconda.com/anaconda/navigator/troubleshooting/) and include:

* Delete a potentially corrupted `.condarc` file. To do that, open *Anaconda Prompt* (on *Windows*) or *Terminal* (on *Linux* or *macOS*) and enter:
	- `conda info` to learn where the `.condarc` file is located  (on *Windows* typically `C:\Users\Username`),
	- Open the indicated directory (e.g., in *Windows* explorer),
	- Delete the `.condarc` file.
* Try to launch *Anaconda Navigator*  from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*) by entering `anaconda-navigator`.
* Fix perfmission issues by deleting the `.continuum` directory:
	- *Windows*: Open *Anaconda Prompt* and run `rd /s .continuum`
	- *Linux* / *macOS*: Open *Terminal* and run `rm -rf ~/.continuum`
* Update *Anaconda Navigator* from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*) by entering `conda update anaconda-navigator`
* Re-install *Anaconda Navigator* from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*) by running:
	- `conda remove anaconda-navigator`
	- `conda install anaconda-navigator`
* Reset *Anaconda Navigator* configuration from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*) by running `anaconda-navigator --reset` (caution: this may be destructive).

Other, bug-fixes, not listed on the above-metioned developer's website are:
* Re-initialize *conda* from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*) by running `conda init`. Then, close and re-open *Anaconda Prompt* (or *Terminal*).
* Update *conda* and *Anaconda Navigator* from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*) as root:
	- `activate root`
	- `conda update -n root conda`
	- `conda update --all`
	- `conda update anaconda-navigator`
* Re-install *PyQt5* from *Anaconda Prompt* (or *Linux* / *macOS* *Terminal*):
	- `pip uninstall PyQt5`
	- `pip install PyQt5`
	- `pip install pyqtwebengine`


## Conda package installation fails
Several reason may cause that installing new packages fails in *Anaconda Prompt* or *Linux* / *macOS* *Terminal*.

* Make sure to close all *Python*-dependent applications (e.g., *Jupyter* or *PyCharm*) before installing.
* Conflict solving activates:
	- Wait until conflicts are parsed (and solved)
	- Enter `conda update conda`
	- Enter `conda update anaconda`
	- Restart *Terminal* or *Anaconda Prompt*
	- Try to re-install the package prompted.

## Large storage size of *Anaconda*

The *Anaconda* *base* environment comes with many pre-installed packages and can be very storage intensive in the order of many gigabytes. Every new environment that is produced can take the same size and multiple *conda* environments may jam your hard disk. Again, there are some solutions:

* Create light-weight environments with [*Miniconda*](https://docs.conda.io/en/latest/miniconda.html).
* Clean tarballs an unnecessary package installation files with *Anaconda Prompt* or *Linux* / *macOS* *Terminal*:
    + Aggressive cleanup: `conda clean --all` (read more in the [developer's docs](https://docs.conda.io/projects/conda/en/latest/commands/clean.html)).
    + Conservative cleanup: `conda clean -tipsy`


## Cannot find ... path

In *Anaconda Prompt* or *Linux* / *macOS* *Terminal* run `conda init` and restart the application.
