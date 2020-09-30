---
title: open TELEMAC-MASCARET (Installation)
tags: [telemac, linux, numerical, modelling, install, vm]
keywords: Virtual, machine, TELEMAC-MASCARET
summary: "Install the numerical modelling tool TELEMAC-MASCARET on Debian Linux."
sidebar: mydoc_sidebar
permalink: install-telemac.html
folder: get-started
---

{% include requirements.html content="This tutorial guides through the installation of [*open TELEMAC-MASCARET*](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/). Because TELEMAC-MASCARET has some very specific dependencies and running numerical models may occupy all available system capacities, it is highly recommended to install the program on a Virtual Machine (VM). Read more on the [Virtual Machines (VMs)](vm.html) page for installing Debian Linux on a Virtual Machine. Make sure to be able to use the [GNOME *Terminal*](vm.html#terminal)." %}

{% include note.html content="This page only guides through the installation of TELEMAC-MASCARET. A tutorial page for running a hydro-morphodynamic model with TELEMAC-MASCARET is under construction." %}

## Install mandatory Prerequisites (Part 1)

Open TELEMAC-MASCARET requires some software for downloading source files, compiling and running the program.

Mandatory prerequisites are:
* *Python* (use *Python3* in the latest releases)
* *Subversion (svn)*
* GNU Fortran 95 compiler (*gfortran*)

{% include tip.html content="Superuser (`sudo`) rights are required for many actions described in this workflow. Read more about how to set up and grant `sudo` rights for your user account on Debian Linux in the [tutorial for setting up Debian on a VM](vm.html#setupd-debian)." %}

### Python3

***Estimated duration: 5-8 minutes.***

The high-level programing language *Python3* is pre-installed on Debian Linux 10.x and needed to launch the compiler script for TELEMAC-MASCARET. To launch *Python3*, open *Terminal* and type `python3`. To exit *Python*, type `exit()`.

TELEMAC-MASCARET requires the following additional *Python* libraries:

* [*NumPy*](https://numpy.org/)
* [*SciPy*](https://scipy.org/)
* [*matplotlib*](https://matplotlib.org/)
 
To install the three libraries, open *Terminal* and type (hit `Enter` after every line):

```
sudo apt-get install python3-numpy python3-scipy python3-matplotlib python3-distutils python3-dev 
```

{% include tip.html content="If an error occurred during the installation, install the extended dependencies (includes Qt) with the following command (after `su`): `apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6`. Then re-try to install the libraries." %}

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

None of the three library imports should return an `ImportError` message. To learn more about *Python* read the [*Python*<sup>basics</sup>](python.html) on this website.

Debian Linux' standard installation comes with `python` for *Python2* and `python3` for *Python3*. To avoid confusion in the installation of TELEMAC-MASCARET, make sure that whatever `python*` environment variable is used, *Python3* is called. To do so, open *Terminal* (as superuser/root `su`) and find out what versions of *Python* are installed:

```
ls /usr/bin/python*

    /usr/bin/python  /usr/bin/python2  /usr/bin/python2.7  /usr/bin/python3  /usr/bin/python3.7  /usr/bin/python3.7m  /usr/bin/python3m
```

Now set the `python` environment variable so that it points at *Python3*:

```
update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
```

Depending on the installed subversion of *Python3*, the folder name `python3.7` needs to be adapted (e.g. to `python3.8`).


### Subversion (svn)

***Estimated duration: Less than 5 minutes.***

We will need the version control system [*Subversion*](https://wiki.debian.org/SVNTutorial) for downloading (and keeping up-to-date) the TELEMAC-MASCARET source files. *Subversion* is installed through the Debian *Terminal* with (read more in the [Debian Wiki](https://wiki.debian.org/Subversion)):

```
su
  ...password:

apt-get install subversion
```

After the successful installation, test if the installation went well by typing `svn --help` (should prompt an overview of `svn` commands). The Debian Wiki provides a [tutorial](https://wiki.debian.org/SVNTutorial) for working with *Subversion*.

### GNU Fortran 95 compiler (gfortran)

***Estimated duration: 3-10 minutes.***

The Fortran 95 compiler is needed to compile TELEMAC-MASCARET through a *Python3* script, which requires that `gfortran` is installed. The Debian Linux retrieves `gfortran` from the standard package repositories. Thus, to install the Fortran 95 compiler open *Terminal* and type:

```
sudo apt-get install gfortran
```

***

***If the installation fails***, add the [buster repository](https://packages.debian.org/buster/gfortran) for *amd64* to the Debian's sources file (`/etc/apt/sources.list`). To open the file, go to *Activities* > *Files* (file container symbol)> *Other Locations* > *etc* > *apt* and right-click in the free space to open *Terminal* (you need to be root). In *Terminal* type:

```
sudo editor sources.list
```

If not defined otherwise, the [GNU nano](https://www.nano-editor.org/) text editor will open. Add the follow following line at the bottom of the file:

```
deb http://ftp.de.debian.org/debian buster main 
``` 

{% include note.html content="This tutorial was written in Stuttgart, Germany, where `http://ftp.de.debian.org/debian` is the closest mirror. Replace this mirror depending on where you are sitting at the time of installing the Fortran 95 compiler. A full list of repositories can be found [here](https://packages.debian.org/buster/amd64/gfortran-multilib/download)." %}

Then, save the edits with `CTRL` + `O` keys and exit *Nano* with `CTRL` + `X` keys. Next, update the repository information by typing (in *Terminal*):

```
apt-get update
apt-get install gfortran
```

***

### Compilers and other essentials

To enable parallelism, a *C* compiler is required for recognition of the command `cmake` in *Terminal*. Moreover, we will need `build-essential` for building packages and create a comfortable environment for `dialog`ues. [VIM](https://www.vim.org/) is a text editor that we will use for bash file editing. Therefore, open *Terminal* (as root/superuser, i.e., type `su`) and type:

```
apt-get install -y cmake build-essential dialog vim
```


## Download TELEMAC-MASCARET

We will need more packages to enable parallelism and compiling, but before installing them, download the latest version of TELEMAC-MASCARET through subversion (`svn`). The developers (irregularly) inform about the newest version on [their website](http://www.opentelemac.org/index.php/latest-news-development-and-distribution). To download TELEMAC-MASCARET open *Terminal* in the *Home* directory (either use `cd` or use the *Files* browser to navigate to the *Home* directory and right-click in the empty space to open *Terminal*) and type (enter `no` when asked for password encryption):

```
svn co http://svn.opentelemac.org/svn/opentelemac/tags/v8p1r0  ~/telemac/v8p1 --username ot-svn-public --password telemac1*
```

This will have downloaded TELEMAC-MASCARET *v8p1r0* to the directory `/home/USER-NAME/telemac/v8p1`.



## Install recommended Prerequisites (Part 2: Parallelism and Compilers)

This section guides through the installation of additional packages required for parallelism. Make sure that *Terminal* recognizes `gcc`, which should be already included in Debian Linux (verify with `gcc --help`). The proceed through this section to:

* Set up environmental variables for the installation of TELEMAC-MASCARET
* Install packages for parallelism to enable a substantial acceleration of simulations:
    + MPI distribution
    + Metis 5.1.x
* Output MED Format:
    + Hdf5
    + MEDFichier 

### Setup environmental variables

Environmental variables will help in the following to compile TELEMAC-MASCARET and helper programs. In this section, we will create a `PATH` variable for pointing at the *Python3* scripts and a `SYSTELCFG` variable to define the configuration file to use for compiling TELEMAC-MASCARET. First, verify that the *Python3* scripts are correctly downloaded in  `~/telemac/v8p1/scripts/python3/` and verify that a *systel* config file called `~/telemac/v8p1/configs/systel.cis-debian.cfg` exists.

Create a new bash file with *Vim* text editor by typing in *Terminal* (as superuser/root `su`)

```
vim ~/.bashrc
```

*Vim* opens in the *Terminal* window and they program may be a little bit confusing in its manipulation. When *Terminal* asks if you want to continue *E*diting, confirm with the `E` key. Then click on the end of the file and enable editing through pressing the `i` key. Now, `-- INSERT --` should be prompted on the bottom of the window. Copy the following lines (`CTRL` + `C` here) and insert the lines by clicking on *Edit* > *Paste*:

```
export PATH=~/telemac/v8p1/scripts/python3/:$PATH
export SYSTELCFG=~/telemac/v8p1/configs/systel.cis-debian.cfg
```

Press `Esc` to leave the *INSERT* mode and then type `:wq` (the letters are visible on the bottom of the window) to save (write-quit) the file. Hit `Enter` to return to the *Terminal*.

{% include tip.html content="Here some hints to troubleshoot typical *VIM* problems:<br>***VIM freezes***: Maybe you hit `CTRL` + `S` keys, which is intuitive for *Windows* users to save a file. In Linux, it has a different meaning... to unfreeze the window, simply hit `CTRL` + `Q`<br>***:wq not working***: Maybe you enabled the *easy mode*. Disable *easy mode* by hitting the `CTRL` + `O` keys.<br> Other typical errors may occur if you installed another keyboard layout for a VM guest machine than the host machine uses." %}

Back in the *Terminal* type the following to apply the new environmental variables (pointers):

```
source ~/.bashrc
```

{% include note.html content="Alternatively you may want to use `systel.cis-ubuntu.cfg` in lieu of `systel.cis-debian.cfg`. In this case, you will need to install `mpich` (`sudo apt-get install mpich`) in lieu of *openMPI* as shown in the following sections to enable parallelism." %}

### Parallelism: Install MPI

***Estimated duration: 5 minutes.***

MPI stands for *Message Passing Interface*, which is a portable message-passing standard. MPI is implemented in many open-source C, C++, and Fortran applications ([read more](https://en.wikipedia.org/wiki/Message_Passing_Interface)). TELEMAC developers recommend to install either *MPICH* or *Open MPI*. Here, we opt for *Open MPI*, which can be installed through the *Terminal*:

```
sudo apt-get install libopenmpi-dev openmpi-bin
```

Test if the installation was successful type:

```
mpif90 --help
```

The *Terminal* should prompt option flags for processing a *gfortran* file. The installation of MPI on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).

{% include important.html content="Recall that we will use the config file `systel.cis-debian.cfg`, which includes parallelism compiling options that build on *Open MPI*. Other configuration files (e.g., `systel.cis-ubuntu.cfg`)   use *MPICH* in lieu of *Open MPI*. To use those configuration files, install *MPICH* with `sudo apt-get install mpich`." %}

### Parallelism: Install Metis

***Estimated duration: 10-15 minutes.***

Metis is a software package for partitioning unstructured graphs, partitioning meshes, and computing fill-reducing orderings of sparse matrices by George Karypis. TELEMAC-MASCARET uses *Metis* as a part of *Partel* to split the mesh in multiple parts for parallel runs. Learn more about *Metis* and potentially newer versions than `5.1.0` (used in the following) on the [Karypis Lab website](http://glaros.dtc.umn.edu/gkhome/metis/metis/download) or reading the [PDF manual](http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/manual.pdf).

Here, we will install *Metis* from *Terminal* directly in the TELEMAC-MASCARET directory. Download the *Metis* archive and unpack it in a temporary (`temp`) directory. The following code block changes to the `optionals` directory (`cd`) of TELEMAC-MASCARET, creates the `temp` folder with `mkdir`, downloads, and unzips the *Metis* archive (run in *Terminal* as ***normal user*** - ***not as root***): 

```
cd ~/telemac/v8p1/optionals
mkdir temp
cd temp
wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
gunzip metis-5.1.0.tar.gz
tar -xvf metis-5.1.0.tar
cd metis-5.1.0
```

Open *Metis*' `Makefile` in the *VIM* text editor (the same )
```
vim Makefile
```

In *VIM*, look for the `prefix  = not-set` and the `cc = not-set` definitions. Click in the according lines and press the `i` key to enable editing (recall: `-- INSERT --` will appear at the bottom of the window). Then change both variables to:

```
prefix = ~/telemac/v8p1/optionals/metis-5.1.0/build/
cc = gcc
```

Press `Esc` to leave the *INSERT* mode and then type `:wq` (the letters are visible on the bottom of the window) to save (write-quit) the file. Hit `Enter` to return to the *Terminal*.

Back in *Terminal*, copy the `Makefile` and remove the `temp` folder with the following command sequence (note: you may want to keep the `temp` folder for installing `hdf5` and `med` file libraries):

```
sudo cp Makefile ~/telemac/v8p1/optionals/metis-5.1.0
cd ~/telemac/v8p1/optionals/
rm -rf temp
```

Change to the final directory where *Metis* will live and compile *Metis*:

```
cd ~/telemac/v8p1/optionals/metis-5.1.0
sudo make config
sudo make
sudo make install
```

Verify the successful installation by running:

```
mpmetis --help
```

The installation of Metis on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_metis).


### Hdf5 and MED format handlers

***Estimated duration: 15-25 minutes (building libraries takes time).***

***HDF5*** is a portable file format that incorporates metadata and communicates efficiently with *C/C++* and *Fortan* on small laptops as well as massively parallel systems. The *hdf5* file library is provided by the [HDFgroup.org](https://portal.hdfgroup.org/).

We will install here version `1.8.21`. Do not try to use any other *hdf5* version because those will not work with the *med file* library (next step). The following code block, creates a `temp` folder with `mkdir` (can be omitted if the folder still exists from the *Metis* installation), downloads, and unzips the *hdf-5-1.8.21* archive (run in *Terminal* as ***normal user*** - ***not as root***): 

```
cd ~/telemac/v8p1/optionals
mkdir temp
cd temp
sudo wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.21/src/hdf5-1.8.21.tar.gz
sudo gunzip hdf5-1.8.21.tar.gz
sudo tar -xvf hdf5-1.8.21.tar
cd hdf5-1.8.21
```

Configure and compile *hdf5*:

```
sudo ./configure --prefix=/home/USER-NAME/telemac/v8p1/optionals/hdf5 --enable-parallel
sudo make
sudo make install 
```

The flag `--prefix=/home/USER-NAME/telemac/v8p1/optionals/hdf5` determines the installation directory for the *hdf5* library, which we will need in the next step for installing the *med file* library. The absolute directory `/home/USER-NAME/` is required because `--prefix` does not accept a relative path. 
The installation of *hdf5* on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_hdf5).

***MED FILE LIBRARY:*** The *med file* library is provided by [salome-platform.org](https://salome-platform.org/) and we need to use the file ([med-3.2.0.tar.gz](http://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz) to ensure compatibility with *hdf5*. So do not try to use any other *med file* library version because those will not work properly with any other *hdf5* file library. The *med file* library requires that *zlib* is installed. To install *zlib* open *Terminal* and type:

```
sudo apt-cache search zlib | grep -i zlib
sudo apt-get install zlib1g zlib1g-dbg zlib1g-dev
```

The following command block, switches to the above-created`temp` folder, downloads, and unzips the *med-3.2.0* archive (run in *Terminal* as ***normal user*** - ***not as root***): 

```
cd ~/telemac/v8p1/optionals
mkdir temp
cd temp
wget http://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz
gunzip med-3.2.0.tar.gz
tar -xvf med-3.2.0.tar
cd med-3.2.0.tar
```

To compile the *med file* library type:

```
./configure --prefix=/home/USER-NAME/telemac/v8p1/optionals/med-3.2.0 --with-hdf5=/home/USER-NAME/telemac/v8p1/optionals/hdf5 --disable-python
sudo make
sudo make install 
```

The flag `--prefix` sets the installation directory and `--width-hdf5` tells the med library where it can find the *hdf5* library. Thus, adapt `/home/USER-NAME/telemac/v8p1/optionals/hdf5` to your local `<install_path>` of the *hdf5* library. Both flags to not accept relative paths (`~/telemac/...`), and therefore, we need to use the absolute paths (`home/USER-NAME/telemac/...`)

{% include note.html content="We need to disable *Python* for the *med file* library because this feature would require *SWIG* version 2.0 and it is not compatible with the current versions of *SWIG* (4.x). Because *SWIG* has no full backward compatibility, the only option we have is to disable *Python* integrity for the *med file* library. Otherwise, *Python* integrity could be implemented by installing *Python* developer kits (`sudo apt-get install python3-dev` and `sudo apt-get install python3.7-dev`) and using the configuration `./configure --with-hdf5=/home/USER-NAME/Telemac/hdf5 PYTHON_LDFLAGS='-lpython3.7m' --with-swig=yes`. To find out what version of *Python* is installed, type `python -V`." %} 


The installation of the *med file* library on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_med).

{% include tip.html content="If you consistently get ***permission denied*** messages, unlock all read and write rights for the `telemac` directory with the following command: `sudo -R 777  /home/USER-NAME/telemac` (replace `USER-NAME` with the user for whom `telemac` is installed)." %}

## Compile TELEMAC-MASCARET

### Adapt and Verify Configuration File (systel.*.cfg)

The configuration file will tell the compiler how flags are defined and where optional software lives. Here, we use the configuration file `systel.cis-debian.cfg`, which lives in `~/telemac/v8p1/configs/`. In particular, we are interested in the following section of the file:

```
# _____                          ___________________________________
# ____/ Debian gfortran openMPI /__________________________________/
[debgfopenmpi]
#
par_cmdexec:   <config>/partel < PARTEL.PAR >> <partel.log>
#
mpi_cmdexec:   /usr/bin/mpiexec -wdir <wdir> -n <ncsize> <exename>
mpi_hosts:
#
cmd_obj:    /usr/bin/mpif90 -c -O3 -DHAVE_MPI -fconvert=big-endian -frecord-marker=4 <mods> <incs> <f95name>
cmd_lib:    ar cru <libname> <objs>
cmd_exe:    /usr/bin/mpif90 -fconvert=big-endian -frecord-marker=4 -lpthread -v -lm -o <exename> <objs> <libs>
#
mods_all:   -I <config>
#
libs_all:    /usr/lib64/openmpi/lib/libmpi.so.0.0.2 /home/telemac/metis-5.1.0/build/Linux-x86_64/libmetis/libmetis.a
```

Verify where the following libraries live on your system (use *Terminal* and `cd` + `ls` commands or Debian's *File* browser):
* *Metis* (something like `~/telemac/v8p1/optionals/metis-5.1.0/build/Linux-x86_64/libmetis/libmetis.a`)
* *Open MPI* (something like `/usr/lib/x86_64-linux-gnu/openmpi/libmpi.so.40.10.3`)
* *mpiexec* (`/usr/bin/mpiexec`)
* *mpif90* (`/usr/bin/mpif90`)
* `~/telemac/metis-5.1.0/build/Linux-x86_64/libmetis/libmetis.a`

Open the configuration file in *VIM*:

```
cd ~/telemac/configs
vim systel.cis-debian.cfg
```

Make the following adaptations in `systel.cis-debian.cfg` as a function of where you found the *Metis* and *Open MPI* libraries:

* Search for *metis* in `libs_all` and adapt all *metis*-related directories to `/home/USER-NAME/telemac/v8p1/optionals/metis-5.1.0/build/Linux-x86_64/libmetis/libmetis.a` (i.e., adapt the absolute directory and the *Metis* version to `5.1.0`). 
* Search for *openmpi* in `libs_all` and correct the library file to `/usr/lib/x86_64-linux-gnu/openmpi/libmpi.so.40.10.3`
* Search for `cmd_obj:` definitions and add `-cpp` in front of the `-c` flags. For example:
```
cmd_obj:    /usr/bin/mpif90 -cpp -c -O3 -DHAVE_MPI -fconvert=big-endian -frecord-marker=4 <mods> <incs> <f95name>
```

{% include tip.html content="To facilitate setting up the `systel` file, we provide a template on our group repository ([download](https://raw.githubusercontent.com/Ecohydraulics/telemac-install-helpers/master/debian/systel.cis-debian.cfg)). Make sure to verify the above-described directories and replace the user name `ssc-deb` with your local user name in the provided `systel.cis-debian.cfg` file." %}

### Setup *Python* source file
The *Python* source file lives in `~/telemac/v8p1/configs` and there is a template available called `pysource.openmpi.sh`.

{% include tip.html content="To facilitate setting up the `pysource` file, we provide a template on our group repository ([download](https://raw.githubusercontent.com/Ecohydraulics/telemac-install-helpers/master/debian/pysource.openmpi.sh)). Make sure to verify all directories set in the provided `pysource.openmpi.sh` file and replace the user name `ssc-deb` with your local user name." %}

### Compile

```
source pysource.openmpi.sh
config.py
```

If `config.py` runs successfully, launch the compilers with the `--clean` flag to avoid any interference with earlier installations:

```
compile_telemac.py --clean
```

## Test TELEMAC MASCARET


## Software for Pre- and Post-processing

### QGIS

*QGIS* is a powerful tool for viewing, creating and editing geospatial data that can be useful in Pre- and post-processing. Detailed installation guidelines are provided on the [Geospatial (GIS) page on this website](geo_software.html). The short path to install *QGIS* on Debian Linux is via *Terminal*:

```
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update && sudo apt-get install -y qgis python-qgis qgis-plugin
```

### Blue Kenue


