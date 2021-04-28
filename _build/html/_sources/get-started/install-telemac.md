# open TELEMAC (Installation)

```{admonition} Requirements
This tutorial guides through the installation of [*open TELEMAC-MASCARET*](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/).
```

## Preface

This page only guides through the **installation** of *TELEMAC*. A **tutorial pages for running hydro(-morpho)dynamic models with *TELEMAC* are under construction**.

### Good to Know

* Installing *TELEMAC* on a [Virtual Machine (VM)](../get-started/vm) is useful for getting started with *TELEMAC* and its sample cases, but not recommended for running a real-world numerical model.
* Make sure to be able to use the [GNOME *Terminal*](../get-started/vm.html#terminal).
* This tutorial refers to the software package *open TELEMAC-MASCARET* as *TELEMAC* because *MASCARET* is a one-dimensional (1D) model and the numerical simulation schemes on this website focus on two-dimensional (2D) and three-dimensional (3D) modelling.

### Two Installation Options

This page describes two ways for installing *TELEMAC*:

* Option 1: Stand-alone installation of *TELEMAC*
    * Every software and packages needed to run a *TELEMAC* model is installed manually
    * **Advantages**:
        - Full control over modules to be installed (high flexibility)
        - Latest version of *TELEMAC* is installed and can be regularly updated
        - Up-to-date compilers and all libraries are exactly matching the system.
    * **Disadvantages**:
        - The variety of install options may cause errors when incompatible packages are combined
        - Challenging installation of optional modules such as AED2, HPC and parallelism
* Option 2: Installation of *TELEMAC* within the *SALOME-HYDRO* software suite.
    * All pre-processing tasks are managed with *SALOME-HYDRO*
    * *TELEMAC* is launched through the *HYDRO-SOLVER* module
    * Post-processing is performed with *ParaView*
    * **Advantages**:
        - All-in-one solution for pre-processing
        - Integrated HPC installation of *TELEMAC* *v8p2*
        - Efficient for MED-file handling
    * **Disadvantages**:
        - Common input geometry file formats such as *SLF* (serafin) require additional software
        - Only works without errors on old *Debian 9 (stretch)*
        - The pre-compiled version of TELEMAC and other modules were built with outdated gfortran compilers that cannot run on up-to-date systems.
        - Often problems with the GUI and high risk of simulation crashes because of invalid library links.

So what option to choose? To leverage the full capacities of *TELEMAC*, use both: [*SALOME-HYDRO*](#salome-hydro) is a powerful pre-processor for preparing simulations and the [stand-alone installation of *TELEMAC*](#modular-install) enables maximum flexibility, system integrity, and computational stability.

## Stand-alone Installation of TELEMAC {#modular-install}

### Install mandatory Prerequisites (Part 1)

Working with *TELEMAC* requires some software for downloading source files, compiling, and running the program. The mandatory software prerequisites for installing *TELEMAC* on [Debian Linux](https://www.debian.org/) are:

* *Python* (use *Python3* in the latest releases)
* *Subversion (svn)*
* GNU Fortran 95 compiler (*gfortran*)

```{tip}
Superuser (`sudo`) rights are required for many actions described in this workflow. Read more about how to set up and grant `sudo` rights for a user account on *Debian Linux* in the [tutorial for setting up *Debian* on a VM](../get-started/vm.html#users).
```

### Python3

***Estimated duration: 5-8 minutes.***

The high-level programing language *Python3* is pre-installed on Debian Linux 10.x and needed to launch the compiler script for *TELEMAC*. To launch *Python3*, open *Terminal* and type `python3`. To exit *Python*, type `exit()`.

*TELEMAC* requires the following additional *Python* libraries:

* [*NumPy*](https://numpy.org/)
* [*SciPy*](https://scipy.org/)
* [*matplotlib*](https://matplotlib.org/)

To install the three libraries, open *Terminal* and type (hit `Enter` after every line):

```
sudo apt install python3-numpy python3-scipy python3-matplotlib python3-distutils python3-dev python3-pip
```

```{tip}
If an error occurs during the installation, install the extended dependencies (includes Qt) with the following command: `sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6`. Then re-try to install the libraries.
```

To test if the installation was successful, type `python3` in *Terminal* and import the three libraries:

```
Python 3.7.7 (default, Jul  25 2030, 13:03:44) [GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> import scipy
>>> import matplotlib
>>> a = numpy.array((1, 1)
>>> print(a)
[1 1]
>>> exit()
```

None of the three library imports should return an `ImportError` message. To learn more about *Python* read the [*Python*<sup>basics</sup>](../python-basics/python) chapter.

<!--
Debian Linux' standard installation comes with `python` for *Python2* and `python3` for *Python3*. To avoid confusion in the installation of *TELEMAC*, make sure that whatever `python*` environment variable is used, *Python3* is called. To do so, open *Terminal* (as superuser/root `su`) and find out what versions of *Python* are installed:

```
ls /usr/bin/python*
```

```
        $ /usr/bin/python  /usr/bin/python2  /usr/bin/python2.7  /usr/bin/python3  /usr/bin/python3.7  /usr/bin/python3.7m  /usr/bin/python3m
```

Now set the `python` environment variable so that it points at *Python3*:

```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
alias python=python3
```

Depending on the installed subversion of *Python3*, the folder name `python3.7` needs to be adapted (e.g., to `python3.8`). Finally, verify that the user environment correctly points at *Python3*:

```
/usr/bin/env python --version
```
    $ Python 3.7.3
-->

### Subversion (svn)

***Estimated duration: Less than 5 minutes.***

We will need the version control system [*Subversion*](https://wiki.debian.org/SVNTutorial) for downloading (and keeping up-to-date) the *TELEMAC* source files. *Subversion* is installed through the Debian *Terminal* with (read more in the [Debian Wiki](https://wiki.debian.org/Subversion):

```
sudo apt install subversion
```

After the successful installation, test if the installation went well by typing `svn --help` (should prompt an overview of `svn` commands). The Debian Wiki provides a [tutorial](https://wiki.debian.org/SVNTutorial) for working with *Subversion*.

### GNU Fortran 95 Compiler (gfortran)

***Estimated duration: 3-10 minutes.***

The Fortran 95 compiler is needed to compile *TELEMAC* through a *Python3* script, which requires that `gfortran` is installed. The Debian Linux retrieves `gfortran` from the standard package repositories. Thus, to install the Fortran 95 compiler, open *Terminal* and type:

```
sudo apt install gfortran
```

***

***IF THE `gfortran` INSTALLATION FAILS***, add the [buster repository](https://packages.debian.org/buster/gfortran) for *amd64* to the Linux sources file (`/etc/apt/sources.list`). To open the file, go to *Activities* > *Files* (file container symbol)> *Other Locations* > *etc* > *apt* and right-click in the free space to open *Terminal* (you need to be root). In *Terminal* type:

```
sudo editor sources.list
```

If not defined otherwise, the [GNU nano](https://www.nano-editor.org/) text editor will open. Add the follow following line at the bottom of the file:

```
deb http://ftp.de.debian.org/debian buster main
```

```{note}
This tutorial was written in Stuttgart, Germany, where `http://ftp.de.debian.org/debian` is the closest mirror. Replace this mirror, depending on where you are at the time of installing the Fortran 95 compiler. A full list of repositories can be found [here](https://packages.debian.org/buster/amd64/gfortran-multilib/download).
```

Then, save the edits with `CTRL` + `O` keys and exit *Nano* with `CTRL` + `X` keys. Next, update the repository information by typing (in *Terminal*):

```
sudo apt update
sudo apt install gfortran
```

***

### Compilers and Other Essentials

To enable parallelism, a *C* compiler is required for recognition of the command `cmake` in *Terminal*. Moreover, we will need `build-essential` for building packages and create a comfortable environment for `dialog`ues. [VIM](https://www.vim.org/) is a text editor that we will use for bash file editing. Therefore, open *Terminal* (as root/superuser, i.e., type `su`) and type:

```
sudo apt install -y cmake build-essential dialog vim
```


## Download *TELEMAC*

We will need more packages to enable parallelism and compiling, but before installing them, download the latest version of *TELEMAC* through subversion (`svn`). The developers (irregularly) inform about the newest public release on [their website](http://www.opentelemac.org/index.php/latest-news-development-and-distribution) and the latest absolute latest release can be read from the [*svn-tags* website](http://svn.opentelemac.org/svn/opentelemac/tags/) (use with passwords in the below command line block). To download* *TELEMAC*, open *Terminal* in the *Home* directory (either use `cd` or use the *Files* browser to navigate to the *Home* directory and right-click in the empty space to open *Terminal*) and type (enter `no` when asked for password encryption):

```
svn co http://svn.opentelemac.org/svn/opentelemac/tags/v8p2r0  ~/telemac/v8p2 --username ot-svn-public --password telemac1*
```

This will have downloaded *TELEMAC* *v8p2r0* to the directory `/home/USER-NAME/telemac/v8p2`.



## Install Recommended Prerequisites (Part 2: Parallelism and Compilers)

This section guides through the installation of additional packages required for parallelism. Make sure that *Terminal* recognizes `gcc`, which should be included in the *Debian* base installation (verify with `gcc --help`). This section includes installation for:

* Install packages for parallelism to enable a substantial acceleration of simulations:
    + MPI distribution
    + Metis 5.1.x
* Output MED Format:
    + Hdf5
    + MEDFichier

```{tip}
The newest versions of Hdf5, MEDFichier, Metis, AED2, and many more are included and compiled in the [*SALOME-HYDRO* installer](#salome-hydro). Thus, consider installing *SALOME-HYDRO* before installing TELEMAC and just copy relevant, compiled libraries from the directory `~/SALOME-HYDRO/Salome-V2_2-s9/prerequisites/` to `~/telemac/v8p2/optionals/`. In this case, it is sufficient to install *open MPI* as below described and then go directly to the [compiling section](#compile), where the optionals-folder names need to be adapted.
```

(mpi)=
### Parallelism: Install MPI

***Estimated duration: 5 minutes.***

MPI stands for *Message Passing Interface*, which is a portable message-passing standard. MPI is implemented in many open-source C, C++, and Fortran applications ([read more](https://en.wikipedia.org/wiki/Message_Passing_Interface)). *TELEMAC* developers recommend installing either *MPICH* or *Open MPI*. Here, we opt for *Open MPI*, which can be installed through the *Terminal*:

```
sudo apt install libopenmpi-dev openmpi-bin
```

To test if the installation was successful type:

```
mpif90 --help
```

The *Terminal* should prompt option flags for processing a *gfortran* file. The installation of MPI on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).

```{attention}
In this tutorial, we will use the configuration file `systel.cis-debian.cfg`, which includes parallelism compiling options that build on *Open MPI*. Other configuration files (e.g., `systel.cis-ubuntu.cfg`) use *MPICH* in lieu of *Open MPI*. To use those configuration files, install *MPICH* with `sudo apt install mpich`.
```

(metis)=
### Parallelism: Install Metis

***Estimated duration: 10-15 minutes.***

Metis is a software package for partitioning unstructured graphs, partitioning meshes, and computing fill-reducing orderings of sparse matrices by George Karypis. *TELEMAC* uses *Metis* as a part of *Partel* to split the mesh into multiple parts for parallel runs. Learn more about *Metis* and potentially newer versions than `5.1.0` (used in the following) on the [Karypis Lab website](http://glaros.dtc.umn.edu/gkhome/metis/metis/download) or reading the [PDF manual](http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/manual.pdf).

***IF TELEMAC/OPTIONALS/METIS DOES NOT EXIST:*** Download the *Metis* archive and unpack it in a temporary (`temp`) directory. The following code block changes to the `optionals` directory (`cd`) of *TELEMAC*, creates the `temp` folder with `mkdir`, downloads, and unzips the *Metis* archive (run in *Terminal* as ***normal user*** - ***not as root***):

```
cd ~/telemac/v8p2/optionals
mkdir metis-5.1.0
mkdir temp
cd temp
wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
gunzip metis-5.1.0.tar.gz
tar -xvf metis-5.1.0.tar
cd metis-5.1.0
```

Open *Metis*' `Makefile` in the *VIM* text editor (installed earlier through `sudo apt install vim`):

```
sudo vim Makefile
```

*VIM* opens in the *Terminal* window and the program may be a little bit confusing to use for someone who is used to *Windows* or *mac OS*. If *VIM*/*Terminal* asks if you want to continue *E*diting, confirm with the `E` key. Then click in the file and enable editing through pressing the `i` key. Now, `-- INSERT --` should be prompted on the bottom of the window. Look for the `prefix  = not-set` and the `cc = not-set` definitions. Click in the corresponding lines and press the `i` key to enable editing (recall: `-- INSERT --` will appear at the bottom of the window). Then change both variables to:

```
prefix = ~/telemac/v8p2/optionals/metis-5.1.0/build/
cc = gcc
```

Press `Esc` to leave the *INSERT* mode and then type `:wq` (the letters are visible on the bottom of the window) to save (write-quit) the file. Hit `Enter` to return to the *Terminal*.

```{tip}
Some hints to troubleshooting typical *VIM* problems:<br>***VIM freezes***: Did you hit the `CTRL` + `S` keys, which is intuitive for *Windows* users to save a file, but in *Linux*, it has a different effect? So, you freezed the window. To unfreeze, simply hit `CTRL` + `Q`<br>***IS `:wq` not working?*** Maybe you enabled the *easy mode*. Disable *easy mode* by hitting the `CTRL` + `O` keys.<br> ***Are you on a virtual machine or remote desktop?*** Check if another keyboard layout is installed on the VM guest / remote machine the host machine /your computer uses.
```

Back in *Terminal*, copy the folder contents and remove the `temp` folder with the following command sequence (if you want to keep the `temp` folder for installing `hdf5` and `med` file libraries, do not `rm` the `temp` folder):

```
sudo cp -a . ~/telemac/v8p2/optionals/metis-5.1.0/
cd ~/telemac/v8p2/optionals/
rm -rf temp
```

Change to the final directory where *Metis* will live and compile *Metis*:

```
cd ~/telemac/v8p2/optionals/metis-5.1.0
make config
make
make install
```

***IF TELEMAC/OPTIONALS/METIS DOES NOT EXIST:*** Install *Metis* from *Terminal* directly in the *TELEMAC* directory tree downloaded with `svn`. Before compiling *Metis*, clean up the *Metis* folder (there is an existing *Makefile*, which we do not want to use):

```
cd ~/telemac/v8p2/optionals/metis-5.1.0
make clean
rm -r build
rm Makefile
```

Then build *Metis* (use for example `~/telemac/v8p2/optionals/metis-5.1.0/build` as `<install_path>`):

```
cmake -D CMAKE_INSTALL_PREFIX=~/telemac/v8p2/optionals/metis-5.1.0/build .
make
make install
```

To verify the successful installation, make sure that the file `~/telemac/v8p2/optionals/metis-5.1.0/build/lib/libmetis.a` exists (i.e., `<install_path>/lib/libmetis.a`). The installation of *Metis* on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_metis).

(med-hdf)=
### Hdf5 and MED Format Handlers

***Estimated duration: 15-25 minutes (building libraries takes time).***

***HDF5*** is a portable file format that incorporates metadata and communicates efficiently with *C/C++* and *Fortan* on small laptops as well as massively parallel systems. The *hdf5* file library is provided by the [HDFgroup.org](https://portal.hdfgroup.org/).

We will install here version `1.8.21`. Do not try to use any other *hdf5* version because those will not work with the *med file* library (next step). The following code block creates a `temp` folder with `mkdir`, downloads, and unzips the *hdf-5-1.8.21* archive (run in *Terminal* as normal user - not as root):

```
cd ~/telemac/v8p2/optionals
mkdir temp
cd temp
wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.21/src/hdf5-1.8.21.tar.gz
gunzip hdf5-1.8.21.tar.gz
tar -xvf hdf5-1.8.21.tar
cd hdf5-1.8.21
```

Configure and compile *hdf5* (enter every command one-by-one):

```
./configure --prefix=/home/USER-NAME/telemac/v8p2/optionals/hdf5 --enable-parallel
make
make install
```

The flag `--prefix=/home/USER-NAME/telemac/v8p2/optionals/hdf5` determines the installation directory for the *hdf5* library, which we will need in the next step for installing the *med file* library. The absolute path `/home/USER-NAME/` is required because `--prefix` does not accept a relative path.
The installation of *hdf5* on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_hdf5).

***MED FILE LIBRARY:*** The *med file* library is provided by [salome-platform.org](https://salome-platform.org/) and we need to use the file ([med-3.2.0.tar.gz](http://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz) to ensure compatibility with *hdf5*. So do not try to use any other *med file* library version because those will not work properly with the *hdf5* file library. Moreover, the *med file* library requires that *zlib* is installed. To install *zlib* open *Terminal* and type:

```
sudo apt-cache search zlib | grep -i zlib
sudo apt install zlib1g zlib1g-dbg zlib1g-dev
```

The following command block, switches to the above-created`temp` folder, downloads, and unzips the *med-3.2.0* archive (run in *Terminal* as ***normal user*** - ***not as root***):

```
cd ~/telemac/v8p2/optionals
mkdir temp
cd temp
wget http://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz
gunzip med-3.2.0.tar.gz
tar -xvf med-3.2.0.tar
cd med-3.2.0
```

To compile the *med file* library type:

```
./configure --prefix=/home/USER-NAME/telemac/v8p2/optionals/med-3.2.0 --with-hdf5=/home/USER-NAME/telemac/v8p2/optionals/hdf5 --disable-python
make
make install
```

The flag `--prefix` sets the installation directory and `--width-hdf5` tells the med library where it can find the *hdf5* library. Thus, adapt `/home/USER-NAME/telemac/v8p2/optionals/hdf5` to your local `<install_path>` of the *hdf5* library. Both flags to not accept relative paths (`~/telemac/...`), and therefore, we need to use the absolute paths (`home/USER-NAME/telemac/...`) here.

```{note}
:class: dropdown
We need to disable *Python* for the *med file* library because this feature would require *SWIG* version 2.0 and it is not compatible with the current versions of *SWIG* (4.x). Because *SWIG* has no full backward compatibility, the only option we have is to disable *Python* integrity for the *med file* library. Otherwise, *Python* integrity could be implemented by installing *Python* developer kits (`sudo apt install python3-dev` and `sudo apt install python3.7-dev`) and using the configuration `./configure --with-hdf5=/home/USER-NAME/Telemac/hdf5 PYTHON_LDFLAGS='-lpython3.7m' --with-swig=yes`. To find out what version of *Python* is installed, type `python -V`.
```


The installation of the *med file* library on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_med).

```{admonition} Permission denied?
:class: tip, dropdown
If you consistently get ***permission denied*** messages, unlock all read and write rights for the `telemac` directory with the following command: `sudo -R 777  /home/USER-NAME/telemac` (replace `USER-NAME` with the user for whom `telemac` is installed).
```

Finally, **remove the `temp` folder** to avoid storing garbage:

```
cd ~/telemac/v8p2/optionals
sudo rm -r temp
```

### AED2

***Estimated duration: < 5 minutes.***

To use *TELEMAC*'s water quality (***waqtel***) module, the *AED2* is (partially) required. In some verswions of *TELEMAC*, the make files for installing *AED2* are provided with the `svn` repository in the *optionals* folder. Otherwise, download and unpack the *aed2* folder from the manual installation sources on [opentelemac.org](http://www.opentelemac.org/index.php/component/jdownloads/summary/39-manual-installation-sources/2126-aed2?Itemid=54). Then, to install *AED2*, `cd` to the *aed2* folder and run `make`:

```
cd ~/telemac/v8p2/optionals/aed2
make
```

```{note}
*AED2* is not needed for the tutorials on this website and the installation of this module can be skipped.
```


## Compile *TELEMAC* <a name="compile"></a>

### Adapt and Verify Configuration File (systel.*.cfg)

***Estimated duration: 15-20 minutes.***

```{tip}
To facilitate setting up the `systel` file, use our template (no * by default AED2*): <br>Right-click on [this download](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/debian/systel.cis-debian.cfg) > *Save Link As...* > `~/telemac/v8p2/configs/systel.cis-debian.cfg` > *Replace Existing*.<br>Make sure to verify the  directories described in this section and replace the `USER-NAME` with your user name in the downloaded `systel.cis-debian.cfg` file.<br>To use *AED2*, [download systel.cis-debian-aed2.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/debian/systel.cis-debian-aed2.cfg).<br>For **dynamic** compiling, [download systel.cis-debian-dyn.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/debian/systel.cis-debian-dyn.cfg).
```

The configuration file will tell the compiler how flags are defined and where optional software lives. Here, we use the configuration file `systel.cis-debian.cfg`, which lives in `~/telemac/v8p2/configs/`. In particular, we are interested in the following section of the file:

```fortran
# _____                          ___________________________________
# ____/ Debian gfortran openMPI /__________________________________/
[debgfopenmpi]
#
par_cmdexec:   <config>/partel < partel.par >> <partel.log>
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
libs_all:    /usr/lib64/openmpi/lib/libmpi.so.0.0.2 /home/telemac/metis-5.1.0/build/lib/libmetis.a
```

The configuration file contains other configurations such as a *scalar* or a *debug* configuration for compiling *TELEMAC*. Here, we only use the *Debian gfortran open MPI* section that has the configuration name `[debgfopenmpi]`. To verify if this section if correctly defined, check where the following libraries live on your system (use *Terminal* and `cd` + `ls` commands or Debian's *File* browser):

* *Metis* is typically located in `~/telemac/v8p2/optionals/metis-5.1.0/build` (if you used this directory for `<install_path>`), where `libmetis.a` typically lives in `~/telemac/v8p2/optionals/metis-5.1.0/build/lib/libmetis.a`
* *Open MPI*'s *include* folder is typically located in `/usr/lib/x86_64-linux-gnu/openmpi/include`
* *Open MPI* library typically lives in `/usr/lib/x86_64-linux-gnu/openmpi/libmpi.so.40.10.3`<br>The number **40.10.3** may be different depending on the latest version. Make sure to adapt the number after **libmpi.so.**.
* *mpiexec* is typically installed in `/usr/bin/mpiexec`
* *mpif90* is typically installed in `/usr/bin/mpif90`
* If installed, *AED2* typically lives in `~/telemac/v8p2/optionals/aed2/`, which should contain the file `libaed2.a` (among others) and the folders *include*, *obj*, and *src*.

Then open the configuration file in *VIM* (or any other text editor) to verify and adapt the *Debian gfortran open MPI* section:

```
cd ~/telemac/v8p2/configs
vim systel.cis-debian.cfg
```

Make the following adaptations in *Debian gfortran open MPI* section to enable parallelism:<a name="parcmd"></a>

* Remove `par_cmdexec` from the configuration file; that means delete the line (otherwise, parallel processing will crash with a message that says *cannot find PARTEL.PAR*):<br>`par_cmdexec:   <config>/partel < PARTEL.PAR >> <partel.log>`
* Find `libs_all` to add and adapt:
    + *metis* (all *metis*-related directories to `/home/USER-NAME/telemac/v8p2/optionals/metis-5.1.0/build/lib/libmetis.a`).
    + *openmpi* (correct the library file to `/usr/lib/x86_64-linux-gnu/openmpi/libmpi.so.40.10.3` or wherever `libmpi.so.xx.xx.x` lives on your machine).
    + *med* including *hdf5* (`~/telemac/v8p2/optionals/`).
    + *aed2* (`~/telemac/v8p2/optionals/aed2/libaed2.a`).

```
libs_all:    /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so.40.10.3 /home/USER-NAME/telemac/v8p2/optionals/metis-5.1.0/build/lib/libmetis.a /home/USER-NAME/telemac/v8p2/optionals/aed2/libaed2.a /home/USER-NAME/telemac/v8p2/optionals/med-3.2.0/lib/libmed.so /home/USER-NAME/telemac/v8p2/optionals/hdf5/lib/libhdf5.so
```

* Add the `incs_all` variable to point include *openmpi*, *med*, and *aed2*:

```
incs_all: -I /usr/lib/x86_64-linux-gnu/openmpi/include -I /home/USER-NAME/telemac/v8p2/optionals/aed2 -I /home/USER-NAME/telemac/v8p2/optionals/aed2/include  -I /home/USER-NAME/telemac/v8p2/optionals/med-3.2.0/include
```

* Search for *openmpi* in `libs_all` and
* Search for `cmd_obj:` definitions, add `-cpp` in front of the `-c` flags, `-DHAVE_AED2`, and `-DHAVE_MED`. For example:

```
cmd_obj:    /usr/bin/mpif90 -cpp -c -O3 -DHAVE_AED2 -DHAVE_MPI -DHAVE_MED -fconvert=big-endian -frecord-marker=4 <mods> <incs> <f95name>
```

An additional keyword in the configurations is `options:` that accepts multiple keywords including `mpi`, `api` (*TelApy* - *TELEMAC's Python API*), `hpc`, and `dyn` or `static`.  The provided `cfg` file primarily uses the `mpi` keyword. To use other installation options (e.g., HPC or dynamic), read the instructions for HPC installation on [opentelemac.org](http://wiki.opentelemac.org/doku.php?id=installation_on_linux) and have a look at the most advanced default config file from EDF (`~/telemac/v8p2/configs/systel.edf.cfg`).


### Setup *Python* Source File

***Estimated duration: 15-20 minutes.***

```{tip}
To facilitate setting up the `pysource` file use our template:<br>Right-click on [this download](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/debian/pysource.openmpi.sh) > *Save Link As...* > `~ /telemac/v8p2/configs/pysource.openmpi.sh` (without *AED2*). <br>Make sure to verify all directories defined in the provided `pysource.openmpi.sh` file as described in this section, and replace the `USER-NAME`.<br>To use *AED2*, [download systel.pysource.openmpi-aed2.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/debian/pysource.openmpi-aed2.sh).<br>For **dynamic compiling**, [download systel.pysource.openmpi-dyn.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/debian/pysource.openmpi-dyn.sh).
```

The *Python* source file lives in `~/telemac/v8p2/configs`, where there is also a template available called `pysource.template.sh`. Here, we will use the template to create our own *Python* source file called `pysource.openmpi.sh` tailored for compiling the parallel version of *TELEMAC* on Debian Linux with the *Open MPI* library. The *Python* source file starts with the definition of the following variables:

* `HOMETEL`: The path to the `telemac/VERSION` folder (`<root>`).
* `SYSTELCFG`: The path to the above-modified configuration file  (`systel.cis-debian.cfg`) relative to `HOMETEL`.
* `USETELCFG`: The name of the configuration to be used (`debgfopenmpi`). Configurations enabled are defined in the `systel.*.cfg` file, in the brackets (`[debgfopenmpi]`) directly below the header of every configuration section.
* `SOURCEFILE`: The path to this file and its name relative to `HOMETEL`.

More definitions are required to define TELEMAC's *Application Programming Interface* (*API*), (parallel) compilers to build *TELEMAC* with *Open MPI*, and external libraries located in the `optionals` folder. The following code block shows how the *Python* source file `pysource.openmpi.sh` should look like. Make sure to **verify every directory on your local file system**, use your *USER-NAME*, and take your time to get all directories right, without typos (critical task).

```
### *TELEMAC* settings -----------------------------------------------
###
# Path to Telemac s root dir
export HOMETEL=/home/USER-NAME/telemac/v8p2
# Add Python scripts to PATH
export PATH=$HOMETEL/scripts/python3:.:$PATH
# Configuration file
export SYSTELCFG=$HOMETEL/configs/systel.cis-debian.cfg
# Name of the configuration to use
export USETELCFG=debgfopenmpi
# Path to this Python source file
export SOURCEFILE=$HOMETEL/configs/pysource.openmpi.sh
# Force python to flush its output
export PYTHONUNBUFFERED='true'
### API
export PYTHONPATH=$HOMETEL/scripts/python3:$PYTHONPATH
export LD_LIBRARY_PATH=$HOMETEL/builds/$USETELCFG/wrap_api/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$HOMETEL/builds/$USETELCFG/wrap_api/lib:$PYTHONPATH
###
### COMPILERS -----------------------------------------------------
export SYSTEL=$HOMETEL/optionals
### MPI -----------------------------------------------------------
export MPIHOME=/usr/bin/mpifort.mpich
export PATH=lib/x86_64-linux-gnu/openmpi:$PATH
export LD_LIBRARY_PATH=$PATH/lib:$LD_LIBRARY_PATH
###
### EXTERNAL LIBRARIES ---------------------------------------------
### HDF5 -----------------------------------------------------------
export HDF5HOME=$SYSTEL/hdf5
export LD_LIBRARY_PATH=$HDF5HOME/lib:$LD_LIBRARY_PATH
export LD_RUN_PATH=$HDF5HOME/lib:$MEDHOME/lib:$LD_RUN_PATH
### MED  -----------------------------------------------------------
export MEDHOME=$SYSTEL/med-3.2.0
export LD_LIBRARY_PATH=$MEDHOME/lib:$LD_LIBRARY_PATH
export PATH=$MEDHOME/bin:$PATH
### METIS ----------------------------------------------------------
export METISHOME=$SYSTEL/metis-5.1.0/build/
export LD_LIBRARY_PATH=$METISHOME/lib:$LD_LIBRARY_PATH
### AED ------------------------------------------------------------
export AEDHOME=$SYSTEL/aed2
export LD_LIBRARY_PATH=$AEDHOME/obj:$LD_LIBRARY_PATH
```

### Compile

***Estimated duration: 20-30 minutes (compiling takes time).***

The compiler is called through *Python* and the above-created bash script (`pysource.openmpi.sh`). Thus, the *Python* source file `pysource.openmpi.sh` knows where helper programs and libraries are located, and it knows the configuration to be used. With the *Python* source file, compiling *TELEMAC* becomes an easy task in *Terminal*. First, load the *Python* source file `pysource.openmpi.sh` as source in *Terminal*, and then, test if it is correctly configured by running `config.py`:

```
cd ~/telemac/v8p2/configs
source pysource.openmpi.sh
config.py
```

Running `config.py` should produce a character-based image in *Terminal* and end with `My work is done`. If that is not the case and error messages occur, *attentively read the error messages* to identify the issue (e.g., there might be a typo in a directory or file name, or a misplaced character somewhere in `pysource.openmpi.sh` or `systel.cis-debian.cfg`).
When `config.py` ran successfully, start compiling *TELEMAC* with the `--clean` flag to avoid any interference with earlier installations:

```
compile_telemac.py --clean
```

The compilation should run for a while (can take more than 30 minutes) and successfully end with the phrase `My work is done`.

```{tip}
If an error occurred in the compiling process, traceback error messages and identify the component that did not work. Revise setting up the concerned component in this workflow very thoroughly. Do not try to re-invent the wheel - the most likely problem is a tiny little detail in the files that you created on your own. Troubleshooting may be a tough task, in particular, because you need to put into question your own work.
```

(testrun)=
### Test *TELEMAC*

***Estimated duration: 5-10 minutes.***

Once *Terminal* was closed or any clean system start-up requires to load the *TELEMAC* source environment in *Terminal* before running *TELEMAC*:

```
cd ~/telemac/v8p2/configs
source pysource.openmpi.sh
config.py
```


To run and test if *TELEMAC* works, use a pre-defined case from the provided `examples` folder:

```
cd ~/telemac/v8p2/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
```

To test if parallelism works, install *htop* to visualize *CPU* usage:

```
sudo apt update
sudo apt install htop
```

Start *htop*'s *CPU* monitor with:

```
htop
```

In a new *Terminal* tab run the above *TELEMAC* example with the flag `--ncsize=N`, where `N` is the number of *CPU*s tu use for parallel computation (make sure that `N` *CPU*s are also available on your machine):

```
cd ~/telemac/v8p2/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas --ncsize=4
```

```{admonition} Cannot find <<PARTEL.PAR>>?
:class: note, dropdown
If there is an error message such as **`Cannot find << PARTEL.PAR >>`** ... **`TypeError: can only concatenate str (not ...) to str`**, make sure that `par_cmdexec` is removed from the configuration file ([see above](#parcmd)).
```

When the computation is running, observe the *CPU* charge. If the *CPU*s are all working with different percentages, the parallel version is working well.

*TELEMAC* should startup, run the example case, and again end with the phrase `My work is done`. To assess the efficiency of the number of *CPU*s used, vary `ncsize`. For instance, the *donau* example (`cd ~/telemac/v8p2/examples/telemac2d/donau`) ran with `telemac2d.py t2d_donau.cas --ncsize=4` may take approximately 1.5 minutes, while `telemac2d.py t2d_donau.cas --ncsize=2` (i.e., half the number of *CPU*s) takes approximately 2.5 minutes. The computing time may differ depending on your hardware, but note that doubling the number of *CPU*s does not cut the calculation time by a factor of two. So to optimize system resources, it can be reasonable to start several simulation cases on fewer cores than one simulation on multiple cores.

```{tip}
If you interrupted the *Terminal* session and get an error message such as *No such file or directory*, you may need to re-define (re-load) the *Python* source file: In *Terminal* go (`cd`) to `~/telemac/v8p2/configs`, type `source pysource.openmpi.sh` > `config.py`, and then go back to the `examples` folder to re-run the example.
```

### Generate Sample Cases (Examples)

*TELEMAC* comes with many application examples in the sub-directory `~/telemac/v8p2/examples/`. To generate the documentation and verify the *TELEMAC* installation, load the *TELEMAC* environment and validate it:

```
cd ~/telemac/v8p2/configs/
source pysource.openmpi.sh
cd ..
config.py
validate_telemac.py
```

```{note}
The `validate_telemac.py` script may fail to run when not all modules are installed (e.g., *Hermes* is missing).
```


## Utilities (Pre- & Post-processing)

(bluekenue)=
### Blue Kenue<sup>TM</sup> (Windows or Linux+Wine)

***Estimated duration: 10 minutes.***

[*Blue Kenue<sup>TM</sup>*](https://nrc.canada.ca/en/research-development/products-services/software-applications/blue-kenuetm-software-tool-hydraulic-modellers) is a pre- and post-processing software provided by the [National Research Council Canada](https://nrc.canada.ca/en), which is compatible with *TELEMAC*. It provides similar functions as the [*Fudaa*](http://www.opentelemac.org/index.php/latest-news-development-and-distribution/240-fudaa-mascaret-3-6) software featured by the *TELEMAC* developers and additionally comes with a powerful mesh generator. It is in particular for the mesh generator that you want to install *Blue Kenue<sup>TM</sup>*. The only drawback is that *Blue Kenue<sup>TM</sup>* is designed for *Windows*. So there are two options for installing *Blue Kenue<sup>TM</sup>*:

1. *TELEMAC* is running on a Debian Linux VM and your host system is *Windows*:<br>[Download](http://www.opentelemac.org/index.php/assistance/forum5/blue-kenue) and install *Blue Kenue<sup>TM</sup>* on your host system and use the [shared folder](../get-started/vm.html#share) of the VM to transfer mesh files.
1. Use [*Wine*](https://wiki.debian.org/Wine) (compatibility layer in *Linux* that enables running *Windows* applications) to install *Blue Kenue<sup>TM</sup>* on *Linux*.

Here are the steps for installing *Blue Kenue<sup>TM</sup>* on Debian Linux with *Wine* ([read more about installing *Windows* applications with *Wine*](../get-started/vm.html#wine):

* Make sure to install *Wine* according to the descriptions on the [Virtual Machines page](../get-started/vm.html#wine).
* Download the *Blue Kenue<sup>TM</sup>* *msi* installer (**32-bit**) from the [developer's website](https://nrc.canada.ca/en/research-development/products-services/software-applications/blue-kenuetm-software-tool-hydraulic-modellers) (follow the instructions on the website - [direct download](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.3.4_32bit.msi)). In detail:
    + Go to [https://chyms.nrc.gc.ca](https://chyms.nrc.gc.ca) and log in with
    + User name: `Public.User`
    + Password: `anonymous`

```{note}
The latest 64-bit version (or any 64-bit version) will not install with *wine*. **Make sure to use the 32-bit installer.**
```

* Install *Blue Kenue<sup>TM</sup>* by using the *Wine*: In *Terminal* type `wine control`.
* After running `wine control` in *Terminal*, a windows-like window opens.
* Click on the *Add/Remove...* button in the window, which opens up another window (*Add/Remove Programs*).
* Click on the *Install...* button and select the downloaded *msi* installer for *Blue Kenue<sup>TM</sup>*.
* Follow the instructions to install *Blue Kenue<sup>TM</sup>* for *Everyone* (all users) and create a *Desktop Icon*.

After the successful installation, launch *Blue Kenue<sup>TM</sup>* with *Wine* ([read more about starting *Windows* applications through *Wine*](../get-started/vm.html#wine):

* In *Terminal* type `wine explorer`
* In the *Wine Explorer* window, navigate to *Desktop* and find the *BlueKenue* shortcut.
* Start *BlueKenue* by double-clicking on the shortcut.
* Alternatively, identify the installation path and the *Blue Kenue<sup>TM</sup>* executable.
    + The 32-bit version is typically installed in `"C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"`.
    + The 64-bit version is typically installed in `"C:\\Program Files\\CHC\\BlueKenue\\BlueKenue.exe"`.
    + Start *Blue Kenue<sup>TM</sup>* with `wine "C:\\Program Files\\CHC\\BlueKenue\\BlueKenue.exe"`.

The Canadian Hydrological Model Stewardship (CHyMS) provides more guidance for installing *Blue Kenue<sup>TM</sup>* on other platforms than *Windows* on their [FAQ](https://chyms.nrc.gc.ca/docs/FAQ.html) page in the troubleshooting section ([direct link to *how to run blue Kenue on another operating system*](https://chyms.nrc.gc.ca/docs/FAQ.html#troubleshooting-how-run-on-another-os)).

(fudaa)=
### Fudaa-PrePro (Linux and Windows)

***Estimated duration: 5-15 minutes (upper time limit if java needs to be installed).***

Get ready with the pre- and post-processing software Fudaa-PrePro:

* Install *java*:
    + On Linux: `sudo apt install default-jdk`
    + On Windows: Get java from [java.com](https://java.com/)
* Download the latest version from the [Fudaa-PrePro repository](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/237993985/Fudaa-Prepro+Downloads)
* Un-zip the downloaded file an proceed depending on what platform you are working with (see below)
* `cd` to the directory where you un-zipped the Fudaa-PrePro program files
* Start Fudaa-PrePro from *Terminal* or *Prompt*
    + On *Linux*: tap `sh supervisor.sh`
    + On *Windows*: tap `supervisor.bat`

There might be an error message such as:
```
Error: Could not find or load main class org.fudaa.fudaa.tr.TrSupervisor
```
In this case, open *supervisor.sh* in a text editor and correct `$PWD Fudaa` to `$(pwd)/Fudaa`. In addition, you can edit the default random-access memory (RAM) allocation in the *supervisor.sh* (or*bat*) file. Fudaa-PrePro starts with a default RAM allocation of 6 GB, which might be too small for grid files with more than 3·10<sup>6</sup> nodes, or too large if your system's RAM is small. To adapt the RAM allocation and7or fix the above error message, right-click on *supervisor.sh* (or on *Windows*: *supervisor.bat*), and find the tag `-Xmx6144m`, where `6144` defines the RAM allocation. Modify this values an even-number multiple of 512. For example, set it to 4·512=2048 and correct `$PWD Fudaa` to `$(pwd)/Fudaa`:

```
#!/bin/bash
cd `dirname $0`
java -Xmx2048m -Xms512m -cp "$(pwd)/Fudaa-Prepro-1.4.2-SNAPSHOT.jar"
org.fudaa.fudaa.tr.TrSupervisor $1 $2 $3 $4 $5 $6 $7 $8 $9
```

(salome-hydro)=
## SALOME-HYDRO (Linux Pre-&Post-processor)

SALOME-HYDRO is a specific version of SALOME ([see description in the modular installation](#salome) with full capacities to create and run a numerical model with *TELEMAC*. The program is distributed on [salome-platform.org](https://www.salome-platform.org/contributions/edf_products/downloads/) as specific EDF contribution.

```{admonition} Linux
SALOME-HYDRO also works on *Windows* platforms, but most applications and support is provided for *Debian Linux*.
```

```{note}
On any system that is not Debian 9 (stretch), SALOME-HYDRO can only be used as a pre-processor (Geometry & Mesh modules) and as a post-processor (ParaVis module) for med-file handling. The *HydroSolver* module that potentially enables running TELEMAC does not work properly with Debian 10 or any system that is not Debian 9.
```

### Prerequisites

* Download the installer from the [developer's website](https://www.salome-platform.org/contributions/edf_products/downloads/) or use the newer version provided through the [TELEMAC user Forum](http://www.opentelemac.org/index.php/kunena/other/12263-hydrosalome-z-interpolation#34100) (registration required)
<!-- [Salome-Hydro V2_2](https://drive.google.com/file/d/1Bimoy9d9dqgQDbMW_kJxilw5JEoMvZ0Q/view) -->
* Install required packages (verify the latest version of `libssl` and if necessary, correct version)

```
sudo apt install openmpi-common gfortran mpi-default-dev zlib1g-dev libnuma-dev xterm net-tools
```

<!-- sudo apt install libssl1.1 libssl-dev  -->

* Install earlier versions of `libssl`:

    * Open the list of sources <br> `sudo editor /etc/apt/sources.list`
    * **Ubuntu users**: In *sources.list*, add *Ubuntu's Bionic* security as source with<br> `deb http://security.ubuntu.com/ubuntu bionic-security main` <br> Using *Nano* as text editor, copy the above line into *sources.list*, then press `CTRL`+`O`, confirm writing with `Enter`, then press `CTRL`+`X` to exit *Nano*.
    * **Debian users**: In *sources.list*, add *Debian Stretch* source with<br> `deb http://deb.debian.org/debian/ stretch main contrib non-free` <br> `deb-src http://deb.debian.org/debian stretch main contrib non-free`<br> Using *Nano* as text editor, copy the above lines into *source.list*, then press `CTRL`+`O`, confirm writing with `Enter`, then press `CTRL`+`X` to exit *Nano*.
    * Back in *Terminal* tap <br> `sudo apt update && apt-cache policy libssl1.0-dev` <br> `sudo apt install libssl1.0-dev libopenblas-dev libgeos-dev unixodbc-dev libnetcdf-dev libhdf4-0-alt libpq-dev qt5ct libgfortran3`

* **Debian 9 users** will need to add and install *nvidia* drivers as described on the virtual machine / *Debian Linux* installation page ([go there](../get-started/vm.html#opengl)).

### Debian 10 (buster) users

*SALOME-HYDRO* is using some out-dated libraries, which require that newer versions (e.g., of the *openmpi* library) must be copied and the copies must be renamed to match the out-dated library names. Therefore, open *Terminal* and tap:

```
sudo cp /usr/lib/x86_64-linux-gnu/libmpi.so.40 /usr/lib/x86_64-linux-gnu/libmpi.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libicui18n.so.63 /usr/lib/x86_64-linux-gnu/libicui18n.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicuuc.so.63 /usr/lib/x86_64-linux-gnu/libicuuc.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicudata.so.63 /usr/lib/x86_64-linux-gnu/libicudata.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libnetcdf.so.13 /usr/lib/x86_64-linux-gnu/libnetcdf.so.11
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_java.so.40 /usr/lib/x86_64-linux-gnu/libmpi_java.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.40 /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.20
```

In addition, the *Qt* library of the *SALOME-HYDRO* installer is targeting out-dated libraries on *Debian 10*. To troubleshoot this issue, open the file explorer and:

* Go to the directory `/usr/lib/x86_64-linux-gnu/`
* Find, highlight, and copy all **lib** files that contain the string **libQt5** (or even just **Qt5**).
* Paste the copied **Qt5** library files into `/SALOME-HYDRO/Salome-V2_2/prerequisites/Qt-591/lib/` (confirm **replace existing files**).

Both procedures for copying library files are anything but a coherent solution. However, it is currently the only way to get *SALOME-HYDRO* working on *Debian 10*.

### Install SALOME-HYDRO

Open the *Terminal*, `cd` into the directory where you downloaded **Salome-V1_1_univ_3.run** (or **Salome-HYDRO-V2_2-s9.run**),  and tap:

```
chmod 775 Salome-HYDRO-V2_2-S9.run
./Salome-HYDRO-V2_2-S9.run
```

During the installation process, define a convenient installation directory such as **/home/salome-hydro/**. The installer guides through the installation and prompts how to launch the program at the end.

```{attention}
If you get error messages such as `./create_appli_V1_1_univ.sh/xml: line [...]: No such file or directory.`, there is probably an issue with the version of *Python*. In this case, run `update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1` and re-try.
```

Try to launch SALOME-HYDRO:

```
cd /home/salome-hydro/appli_V2_2/
./salome
```

If there are issues such as  `Kernel/Session` in the `Naming Service` (`[Errno 3] No such process` ... `RuntimeError: Process NUMBER for Kernel/Session not found`), go to the [troubleshooting page](../troubleshoot/dbg-telemac.html#salome-dbg).

If the program is not showing up properly (e.g., empty menu items), read more about [Qt GUI support on the troubleshooting page](../troubleshoot/dbg-telemac.html#qt-dbg)

<!--
```{tip}
**Set a keyboard shortcut to start SALOME-HYDRO on Debian Linux**: Go to *Activities*, tap *keyboard*, and select *Keyboard* from the list (do not click on *Tweaks*). In the *Keyboard* window, scroll to the bottom and click on the `+` sign to define a new shortcut. In the popup window use, for example, *Salome-Hydro* as *Name*, in the *Command* box tap `/home/salome-hydro/appli_V1_1_univ/salome` (or where ever *SALOME-HYDRO* is installed), and define a *Shortcut*, such as `CTRL` + `Alt` + `S`.
```

```{figure} ../img/sah-keyboard-shortcut.png
:alt: salome-hydro shortcut

Define a keyboard shortcut to start SALOME-HYDRO.
```
-->

(paravis-salome)=
### ParaView (ParaVis) through SALOME-HYDRO

[*ParaView*](https://www.paraview.org) serves for the visualization of model results in the SALOME-HYDRO modelling chain. The built-in module *ParaViS* essentially corresponds to *ParaView*, but the separate usage of *ParaView* enables a better experience for post-processing of results. The installation of *SALOME-HYDRO* already involves an older version of *ParaView* that is able to manipulate *MED* files. To start *ParaView* through *SALOME-HYDRO*, open *Terminal*, `cd` to the directory where *SALOME-HYDRO* is installed, launch the environment, and then launch *ParaView*:

```
cd /home/slome-hydro/appli_V2_2/
. env.d/envProducts.sh
./runRemote.sh paraview
```

```{tip}
If the *ParaVis* module continuously crashes in *SALOME-HYDRO*, consider to install the latest version of [*SALOME*](../get-started/install-openfoam.html#salome) (e.g., as described with the installation of *OpenFOAM*).
```

Alternatively, *ParaView* is freely available on the [developer's website](https://www.paraview.org/download/) and the latest stable release can be installed on *Debian Linux*, through the *Terminal*:

```
sudo apt install paraview
```

In this case, to run *ParaView* tap `paraview` in *Terminal*. If you are using a virtual machine, start *ParaView* with the `--mesa-llvm` flag (i.e., `paraview --mesa-llvm`).
To enable *MED* file handling, *MED* coupling is necessary, which requires to follow the installation instructions on [docs.salome-platform.org](https://docs.salome-platform.org/7/dev/MEDCoupling/install.html).

### Start SALOME-HYDRO

To start *SALOME-HYDRO*, open *Terminal* and tap:

```
/home/salome-hydro/appli_V1_1_univ/salome
```

(qgis-telemac)=
### QGIS (Linux and Windows)

***Estimated duration: 5-10 minutes (depends on connection speed).***

*QGIS* is a powerful tool for viewing, creating, and editing geospatial data that can be useful in Pre- and post-processing. Detailed installation guidelines are provided on the [Geospatial (GIS) page on this website](../get-started/geo). The short path to install *QGIS* on Debian Linux is via *Terminal*:

```
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt update && sudo apt install -y qgis python-qgis qgis-plugin
```

For working with *TELEMAC*, consider installing the following *QGIS Plugins* (*Plugins* > *Manage and Install Plugins...*):

*  *PostTelemac* visualizes *slf* (and others such as *res*) geometry files at different time steps.
* *DEMto3D* enables to export *STL* geometry files for working with *SALOME* and creating 3D meshes.

Note that *DEMto3D* will be available in the *Raster* menu: *DEMto3D* > *DEM 3D printing*.
