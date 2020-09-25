---
title: open TELEMAC-MASCARET (Installation)
tags: [telemac, numerical, modelling, install, vm]
keywords: Virtual, machine, TELEMAC-MASCARET
summary: "Install the numerical modelling tool TELEMAC-MASCARET on Debian Linux."
sidebar: mydoc_sidebar
permalink: install-telemac.html
folder: get-started
---

{% include requirements.html content="This tutorial guides through the installation of [*open TELEMAC-MASCARET*](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/). Because TELEMAC-MASCARET has some very specific dependencies and running numerical models may occupy all available system capacities, it is highly recommended to install the program on a Virtual Machine (VM). Read more on the [Virtual Machines (VMs)](vm.html) page for installing Debian Linux on a Virtual Machine. Make sure to be able to use the [GNOME *Terminal*](vm.html#terminal)." %}

{% include note.html content="This page only guides through the installation of TELEMAC-MASCARET. A tutorial page for running a hydro-morphodynamic model with TELEMAC-MASCARET is under construction." %}

## Install Mandatory Prerequisites (Dependencies)

Open TELEMAC-MASCARET requires some software for downloading source files, compiling and running the program.

Mandatory prerequisites are:
* *Python* (use *Python3* in the latest releases)
* *Subversion (svn)*
* GNU Fortran 95 compiler (*gfortran*)


### Python3

> Estimated duration: 5-8 minutes.

The high-level programing language *Python3* is pre-installed on Debian Linux 10.x and needed to launch the compiler script for TELEMAC-MASCARET. To launch *Python3*, open *Terminal* and type `python3`. To exit *Python*, type `exit()`.

TELEMAC-MASCARET requires the following additional *Python* libraries:

* [*NumPy*](https://numpy.org/)
* [*SciPy*](https://scipy.org/)
* [*matplotlib*](https://matplotlib.org/)
 
To install the three libraries, open *Terminal* and type (hit `Enter` after every line):

```
su
  ...password:
apt-get install python3-numpy
  [...]
apt-get install python3-scipy
  [...] Y [...]
apt-get install python3-matplotlib
  [...] Y [...]
```

> If an error occurred during the installation, install the extended dependencies (includes Qt) with the following command (after `su`): `apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6`. Then re-try to install the libraries.

To test if the installation was successful, type `python3` in *Terminal* and import the three libraries:

```
Python 3.7.7 (default, Jul  25 2020, 13:03:44) [GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> import scipy
>>> import matplotlib
>>> a = numpy.array((1, 1))
>>> print(a)
[1 1]
>>> exit()
```

None of the three library imports should return an `ImportError` message. To learn more about *Python* visit [hydro-informatics.github.io/python](https://hydro-informatics.github.io/python.html).

### Subversion (svn)

> Estimated duration: Less than 5 minutes.

We will need the version control system [*Subversion*](https://wiki.debian.org/SVNTutorial) for downloading (and keeping up-to-date) the TELEMAC-MASCARET source files. *Subversion* is installed through the Debian *Terminal* with (read more in the [Debian Wiki](https://wiki.debian.org/Subversion)):

```
su
  ...password:

apt-get install subversion
```

After the successful installation, test if the installation went well by typing `svn --help` (should prompt an overview of `svn` commands). The Debian Wiki provides a [tutorial](https://wiki.debian.org/SVNTutorial) for working with *Subversion*.

### GNU Fortran 95 compiler (gfortran)

> Estimated duration: 3-10 minutes.

The Fortran 95 compiler is needed to compile TELEMAC-MASCARET through a *Python3* script, which requires that `gfortran` is installed. The Debian Linux retrieves `gfortran` from the standard package repositories. Thus, to install the Fortran 95 compiler open *Terminal* and type:

```
su 
  password:...

apt-get install gfortran
```

***

***If the installation fails***, add the [buster repository](https://packages.debian.org/buster/gfortran) for *amd64* to the Debian's sources file (`/etc/apt/sources.list`). To open the file, go to *Activities* > *Files* (file container symbol)> *Other Locations* > *etc* > *apt* and right-click in the free space to open *Terminal* (you need to be root). In *Terminal* type:

```
su 
  password:...

editor sources.list
```

If not defined otherwise, the [GNU nano](https://www.nano-editor.org/) text editor will open. Add the follow following line at the bottom of the file:

```
deb http://ftp.de.debian.org/debian buster main 
``` 

> Note: This tutorial was written in Stuttgart, Germany, where `http://ftp.de.debian.org/debian` is the closest mirror. Replace this mirror depending on where you are sitting at the time of installing the Fortran 95 compiler. A full list of repositories can be found [here](https://packages.debian.org/buster/amd64/gfortran-multilib/download).

Then, save the edits with `CTRL` + `O` keys and exit *Nano* with `CTRL` + `X` keys. Next, update the repository information by typing (in *Terminal*):

```
apt-get update
apt-get install gfortran
```

***

## Optional (highly-recommended) Prerequisites

Optional prerequisites are:

* For parallelism (substantial acceleration of simulations):
    + MPI distribution
    + Metis 5.1.x
    + *MUMPS (a new parallel solver) - not shown here*
* Output MED Format:
    + Hdf5
    + MEDFichier 

### Parallelism: MPI

MPI stands for *Message Passing Interface*, which is a portable message-passing standard. MPI is implemented in many open-source C, C++, and Fortran applications ([read more](https://en.wikipedia.org/wiki/Message_Passing_Interface)). TELEMAC developers recommend to install either *MPICH* or *Open MPI*. Here, we opt for *Open MPI*, which can be installed through the *Terminal*.

```
su 
  password:...

apt-get install libopenmpi-dev openmpi-bin
```

To test if the installation was successful type:

```
mpif90 --help
```

The *Terminal* should prompt option flags for processing a *gfortran* file. The installation of MPI on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).

### Parallelism: Metis

Metis is a software package for partitioning unstructured graphs, partitioning meshes, and computing fill-reducing orderings of sparse matrices by George Karypis. Learn more about metis on the [Karypis Lab website](http://glaros.dtc.umn.edu/gkhome/metis/metis/download) or reading the [PDF manual](http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/manual.pdf)

To compile Metis, a *C* compiler is required to enable the command `cmake` in *Terminal*. To install *Cmake*, open *Terminal* and type:

```
su 
  password:...

apt-get install -y cmake
```

Then [download Metis 5.1.x](http://glaros.dtc.umn.edu/gkhome/metis/metis/download) from the Karypis Lab's website (University of Minnesota, USA).  Extract the metis source files from the `.tar.gz` archive into a directory of your choice, which corresponds to the `<install_path>`. For example, create a new folder in your Linux *Home* directory and call it `metis`.

{% include note.html content="Alternatively, you can [download the automatic installer](http://opentelemac.org/index.php/download) of the latest version of open TELEMAC-MASCARET (login required), which contains Metis in the sub-folder `/optionals/metis-5.1.0/`. Copy the contents of the latter folder to your `<install_path>` instead of extracting the `.tar.gz` archive from the Karypis Lab website." %}


In the following we use a new directory called `/home/deb-user/Telemac/metis/` as `<install_path>`, where the `.tar.gz` archive from the Karypis Lab was extracted using Debian's *Archive Manager* (in *Firefox* download [metis-5.1.0.tar.gz](http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz) > *Open With* > *Archive Manager* > select all files > right-click > *Extract* and navigate to `/home/deb-user/Telemac/metis/`). Open the directory `/home/deb-user/Telemac/metis/` in *Terminal* and type:

```
su 
  password:...


```



The installation of Metis on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_metis).

## Download and Compile TELEMAC-MASCARET


## Test TELEMAC MASCARET



