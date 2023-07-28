(telemac-install)=
# TELEMAC (Installation)


## Preface


This tutorial guides through the installation of [open TELEMAC-MASCARET](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/) based platforms (i.e., also works with Ubuntu and its derivatives, such as Mint or Lubuntu). **Account for approximately 1-2 hours for installing TELEMAC and make sure to have a stable internet connection (>1.4 GB file download).**


***

This section only guides through the **installation** of TELEMAC. A tutorial for running hydro(-morpho)dynamic models with TELEMAC is currently under construction for this eBook.

***

Before you start, note:

* Installing TELEMAC on a {ref}`Virtual Machine (VM) <chpt-vm-linux>` is useful for getting started with TELEMAC and its sample cases, but not recommended for running a real-world numerical model (limited performance of VMs).
* Familiarize with the {ref}`Linux Terminal <linux-terminal>` to understand the underpinnings for compiling TELEMAC.
* This tutorial refers to the software package *open TELEMAC-MASCARET* as TELEMAC because *MASCARET* is a one-dimensional (1d) model and the numerical simulation schemes in this eBook focus on two-dimensional (2d) and three-dimensional (3d) modeling.
* A couple of installation options are available:

`````{tab-set}
````{tab-item} Custom Installation (Recommended)
Continue to read and walk through the following sections.

````

````{tab-item} Mint Hyfo VM

If you are working with the {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`, skip the tutorials on this website because TELEMAC v8p3 is already preinstalled and you are good to go for completing the {ref}`TELEMAC tutorials <chpt-telemac>`.

Load the TELEMAC environment and check if it works with:

```
cd ~/telemac/v8p3/configs
source pysource.hyfo.sh
config.py
```
````
````{tab-item} SALOME-HYDRO
TELEMAC is also available through the SALOME-HYDRO software suite, which is a spinoff of SALOME. However, the principal functionalities of SALOME-HYDRO may migrate to a new QGIS plugin. Therefore, this eBook recommends installing TELEMAC independently from any pre- or post-processing software.
````

````{tab-item} Docker Image

The Austrian engineering office *Flussplan* provides a Docker container of TELEMAC v8 on their [docker-telemac GitHub repository](https://github.com/flussplan/docker-telemac). Note that a Docker container represents an easy-to-install virtual environment that leverages cross-platform compatibility, but affects computational performance. If you have the proprietary Docker software installed and computational performance is not the primary concern for your models, Flussplan's Docker container might be a good choice. For instance, purely hydrodynamic models with small numbers of grid nodes and without additional TELEMAC module implications will efficiently run in the Docker container.

````
`````

(modular-install)=
## Basic Requirements

```{admonition} Old SVN has been replaced by GIT (since v8p3)
:class: note, dropdown

The newest release of TELEMAC (v8p4) is provided on [gitlab](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/tree/main) with the version control system {ref}`git <chpt-git>` rather than the previously used `svn` version control.
```
```{admonition} Admin (sudo) rights required
:class: attention, dropdown
Superuser (`sudo` for **su**per **do**ers list) rights are required for many actions described in this workflow. Read more about how to set up and grant `sudo` rights for a user account on *Debian Linux* in the tutorial for setting up {ref}`Debian Linux <user-rights>`.
```

Working with TELEMAC requires some software for downloading source files, compiling, and running the program. The mandatory software prerequisites for installing TELEMAC on [Debian Linux](https://www.debian.org/) are:

* Python 3.7 (and more recent) with {ref}`NumPy >=1.15 <numpy>`
* GNU Fortran 95 compiler (*gfortran*)


### Python3

***Estimated duration: 5-8 minutes.***

The high-level programing language *Python3* is pre-installed on Debian Linux 10.x and needed to launch the compiler script for TELEMAC. To launch *Python3*, open Terminal and type `python3`. To exit Python, type `exit()`.

TELEMAC requires the [NumPy](https://numpy.org/) Python library that comes along with [SciPy](https://scipy.org/) and [matplotlib](https://matplotlib.org/).

To install NumPy libraries, open Terminal and type (hit `Enter` after every line):

```
sudo apt install python3-numpy python3-scipy python3-matplotlib python3-distutils python3-dev python3-pip
```

````{admonition} Got Qt Errors?
:class: warning, dropdown
If an error occurs during the installation, install the extended dependencies (includes Qt) with the following command:

```
sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
```

Then re-try to install the libraries.
````

To test if the installation was successful, type `python3` in Terminal and import the three libraries:

```
Python 3.9.1 (default, Jul  25 2030, 13:03:44) [GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> a = numpy.array((1, 1))
>>> print(a)
[1 1]
>>> exit()
```

None of the three library imports should return an `ImportError` message. To learn more about Python read the section on {ref}`sec-pypckg`.

(tm-git-requirements)=
### GIT

***Estimated duration: Less than 5 minutes.***

The installation of the git version control system and its usage is extensively described in the {ref}`git section of this eBook <dl>`. In addition to the git functionalities described in the git section, the following are needed to manage large files that come along with TELEMAC:

```
sudo apt install git-all git-lfs
```

### GNU Fortran 95 Compiler (gfortran)

***Estimated duration: 3-10 minutes.***

The Fortran 95 compiler is needed to compile TELEMAC through a Python3 script, which requires that `gfortran` is installed. The Debian Linux retrieves `gfortran` from the standard package repositories. Thus, to install the Fortran 95 compiler, open Terminal and type:

```
sudo apt install gfortran
```

````{admonition} If the gfortran installation fails...
:class: attention, dropdown
Add the [buster repository](https://packages.debian.org/buster/gfortran) for *amd64* to the Linux sources file (`/etc/apt/sources.list`). To open the file, go to *Activities* > *Files* (file container symbol)> *Other Locations* > *etc* > *apt* and right-click in the free space to open Terminal (you need to be root). In Terminal type:

```
sudo editor sources.list
```

If not defined otherwise, the [GNU nano](https://www.nano-editor.org/) text editor will open. Add the follow following line at the bottom of the file:

```
deb http://ftp.de.debian.org/debian buster main
```

*Note:* This tutorial was written in Stuttgart (Germany) where `http://ftp.de.debian.org/debian` is one of the closest mirrors. Depending on where you are at the time of installing the Fortran 95 compiler replace the mirror address. A full list of repositories can be found at [https://packages.debian.org](https://packages.debian.org/buster/amd64/gfortran-multilib/download).

Then, save the edits with `CTRL` + `O` keys and exit *Nano* with `CTRL` + `X` keys. Next, update the repository information by typing (in Terminal):

```
sudo apt update
sudo apt install gfortran
```
````

### More Compilers and Essentials

***Estimated duration: 2-5 minutes.***
To enable parallelism, a *C* compiler is required for recognition of the command `cmake` in Terminal. Moreover, we will need `build-essential` for building packages and create a comfortable environment for `dialog`ues. [VIM](https://www.vim.org/) is a text editor that we will use for bash file editing. Alternatively to VIM, consider [gedit](https://wiki.gnome.org/Apps/Gedit) or [Nano](https://www.nano-editor.org/) (remove not-wanted editors from the below list). Therefore, open Terminal (as root/superuser, i.e., type `su`) and type:

```
sudo apt install -y cmake build-essential dialog vim gedit gedit-plugins
```


### Get the TELEMAC Repo

***Estimated duration: 25-40 minutes (large downloads).***

Before getting more packages to enable parallelism and compiling, download the latest version of TELEMAC with git in which additional packages will be embedded. To download (i.e., `git clone`) TELEMAC, open Terminal, which will by default start in your home directory (`/home/USERNAME/`). The following instructions assume you want to install TELEMAC directly in your home directory. However, it might make sense to create a new sub-folder (e.g., called `/modeling`) to better organize your file system (`mkdir ~/modeling/` > `cd ~/modeling`). To download TELEMAC into the home (or a new) directory, type (enter `no` when asked for password encryption):

```
git clone https://gitlab.pam-retd.fr/otm/telemac-mascaret.git
```

This will have downloaded TELEMAC to a sub-directory called `/telemac-mascaret`.

````{admonition} There are many (experimental) branches of TELEMAC available
:class: tip, dropdown

The TELEMAC git repository provides many other TELEMAC versions in the form of development or old-version branches. For instance, the following clones the `upwind_gaia` branch to a local sub-folder called `telemac/gaia-upwind`. After cloning this single branch, compiling TELEMAC can be done as described in the following.

```
git clone -b upwind_gaia --single-branch https://gitlab.pam-retd.fr/otm/telemac-mascaret.git telemac/gaia-upwind
```

Read more about cloning single TELEMAC branches in the [TELEMAC wiki](http://wiki.opentelemac.org/doku.php?id=telemac-mascaret_git_repository).
````

After downloading (cloning) the TELEMAC repository, switch to (check out) the latest version:

```
cd telemac-mascaret
git checkout tags/v8p4r0
```


## Optional Requirements (Parallelism and Others)

This section guides through the installation of additional packages required for parallelism. Make sure that Terminal recognizes `gcc`, which should be included in the *Debian* base installation (verify with `gcc --help`). This section includes installation for:

* Install packages for parallelism to enable a substantial acceleration of simulations:
    + MPI distribution
    + Metis 5.1.0
* For the MED file format (input mesh and computation results):
    + Hdf5
    + MEDFichier 3.2.0


(mpi)=
### Parallelism: Install MPI

***Estimated duration: 5 minutes.***

TELEMAC's parallelism modules require that the *Message Passing Interface* ({term}`MPI`) standard is installed either through the *MPICH* or the *Open MPI* library. Here, we opt for *Open MPI*, which can be installed via Terminal:

```
sudo apt install libopenmpi-dev openmpi-bin
```

To test if the installation was successful type:

```
mpif90 --help
```

The Terminal should prompt option flags for processing a *gfortran* file. The installation of MPI on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).

```{admonition}  How to use MPICH in lieu of Open MPI
:class: note
This tutorial uses the configuration file `systel.edfHy.cfg`, which includes parallelism compiling options that build on *Open MPI*. Other configuration files (e.g., `systel.cis-ubuntu.cfg`) use *MPICH* instead of *Open MPI*. To use those configuration files, install *MPICH* with `sudo apt install mpich`.
```

(metis)=
### Parallelism: Install Metis

***Estimated duration: 10-15 minutes.***

Metis is a software package for partitioning unstructured graphs, partitioning meshes, and computing fill-reducing orderings of sparse matrices by George Karypis. TELEMAC uses *Metis* as a part of *Partel* to split the mesh into multiple parts for parallel runs. *Metis* is developed by the Karypis Lab at the [University of Minnesota](https://umn.edu/).


Download the *Metis* archive and unpack it in a temporary (`temp`) directory. The following code block changes to the `optionals` directory (`cd`) of TELEMAC, creates the `temp` folder with `mkdir`, downloads, and unzips the *Metis* archive (run in Terminal as ***normal user*** - ***not as root***):

```{margin}
The [Telemac installation wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_metis) points to a software repository containing Metis-v5.1.0 that is hosted on the website of the [Karypis Lab](http://glaros.dtc.umn.edu/gkhome/metis/metis/download), which, however, was not available anymore upon our last update. This is why this eBook provides a Metis v5.1.1 fork from the Karypis Lab's [METIS Github repository](https://github.com/KarypisLab/GKlib.git) at [hydro-informatics/metis](https://github.com/hydro-informatics/metis).
```

To install Metis, use the [hydro-informatics/metis](https://github.com/hydro-informatics/metis) v5.1.1 fork from the Karypis Lab's [METIS Github repository](https://github.com/KarypisLab/METIS), which is tweaked for the Telemac installation:


```
cd ~/telemac/optionals
mkdir metis
git clone https://github.com/hydro-informatics/metis.git
cd metis
```

This repository also embraces a fork from the Karypis Labs' [GKlib](https://github.com/KarypisLab/GKlib), which still needs to be compiled (starting from the `~/telemac/optionals/metis` folder):

```
cd GKlib
make config cc=gcc prefix=~/telemac/optionals/metis/GKlib openmp=set
make
make install
cd ..
```

Next, adapt the Metis' `Makefile` either with any text editor or the *VIM* text editor (installed earlier through `sudo apt install vim`):

`````{tab-set}
````{tab-item} Any text editor
Open the metis `Makefile` (i.e., `~/telemac/optionals/metis/Makefile`) by navigating through your system browser (also known as *Explorer* on Windows) and double-clicking on the *Makefile* (opens, for example, [gedit](https://wiki.gnome.org/Apps/Gedit)). At the top of the Makefile, find `prefix  = not-set` and `cc = not-set` to replace them with:

```
prefix = ~/telemac/optionals/metis/build/
cc = gcc
```

Save and close the Makefile.

````

````{tab-item} VIM

```
vim Makefile
```

*VIM* opens in the Terminal window and the program may be a little bit confusing to use for someone who is used to *Windows* or *mac OS*. If *VIM*/Terminal asks if you want to continue {**E**}diting, confirm with the `E` key. Then click in the file and enable editing through pressing the `i` key. Now, `-- INSERT --` should be prompted on the bottom of the window. Look for the `prefix  = not-set` and the `cc = not-set` definitions. Click in the corresponding lines and press the `i` key to enable editing (recall: `-- INSERT --` will appear at the bottom of the window). Change both variables to:

```
prefix = ~/telemac/optionals/metis/build/
cc = gcc
```

Press `Esc` to leave the *INSERT* mode and then type `:wq` (the letters are visible on the bottom of the window) to save (write-quit) the file. Hit `Enter` to return to the Terminal.

```{admonition} Troubleshoot typical VIM issues
:class: dropdown

* **VIM freezes**: Did you hit the `CTRL` + `S` keys, which is intuitive for *Windows* users to save a file, but in *Linux*, it has a different effect? So, you have freezed the window. To unfreeze, simply hit `CTRL` + `Q`
* **IS `:wq` not working?** Maybe you enabled the *easy mode*. Disable *easy mode* by hitting the `CTRL` + `O` keys.
* **Are you on a virtual machine or remote desktop?** Check if another keyboard layout is installed on the VM guest / remote machine the host machine /your computer uses.
```

````
`````

Back in Terminal, install Metis (make sure to be in the right directory, that is, `~/telemac/optionals/metis/`):

```
make config
make
make install
```

To verify the successful installation, make sure that the file `~/telemac/optionals/metis/build/lib/libmetis.a` exists (i.e., `<install_path>/lib/libmetis.a` ).

````{admonition} Debian alternative: apt-install libmetis-dev
:class: tip, dropdown

Alternatively, on Debian-based systems, install `libmetis-dev` with: 

```
sudo apt install libmetis-dev
```

This package currently provides Metis v5.1.0, but verify the version on [https://packages.debian.org](https://packages.debian.org/sid/libmetis-dev) to be sure having a workable version of Metis available. However, we did not test the integration of Metis in the Telemac installation.
````


(med-hdf)=
### Hdf5 and MED Format Handlers

***Estimated duration: 15-25 minutes (building libraries takes time).***

**HDF5** is a portable file format that incorporates metadata and communicates efficiently with *C/C++* and *Fortran* on small laptops as well as massively parallel systems. The *hdf5* file library is provided by the [HDFgroup.org](https://portal.hdfgroup.org/).

```{margin}
The [Telemac installation wiki](http://wiki.opentelemac.org/doku.php?id=installation_on_linux) suggests using version `1.10.7`, which, however, will cause an error when compiling the medfile library.
```

We will install here version `1.10.3`. Do not try to use any other *hdf5* version because those will not work with the *med file* library (next step). The following code block downloads and unzips the *hdf-5-1.10.3* archive in the above-created (metis) `temp/` folder (run in Terminal as normal user - not as root):

```
cd ~/telemac/optionals/temp
wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.3/src/hdf5-1.10.3.tar.gz
gunzip hdf5-1.10.3.tar.gz
tar -xvf hdf5-1.10.3.tar
cd hdf5-1.10.3
```

Configure and compile *hdf5* (enter every command one-by-one):

```
./configure --prefix=/home/USERNAME/telemac/optionals/hdf5 --enable-parallel
make
make install
```

The flag `--prefix=/home/USERNAME/telemac/optionals/hdf5` determines the installation directory for the *hdf5* library, which we will need in the next step for installing the *med file* library. The absolute path `/home/USERNAME/` is required because `--prefix` does not accept a relative path.
The installation of *hdf5* on Linux is also documented in the [Telemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_hdf5).

***MED FILE LIBRARY:*** The *med file* library is provided by [salome-platform.org](https://salome-platform.org/) and we need to use the file ([med-4.0.0.tar.gz](http://files.salome-platform.org/Salome/other/med-4.0.0.tar.gz) to ensure compatibility with *hdf5*. So do not try to use any other *med file* library version because those will not work properly with the *hdf5* file library. Moreover, the *med file* library requires that *zlib* is installed. To install *zlib* open Terminal and type:

```
sudo apt-cache search zlib | grep -i zlib
sudo apt install zlib1g zlib1g-dev
```

The following command block, switches to the above-created `temp` folder, downloads, and unzips the *med-4.0.0* archive (run in Terminal as ***normal user*** - ***not as root***):


```
cd ~/telemac/optionals/temp
wget http://files.salome-platform.org/Salome/other/med-4.0.0.tar.gz
gunzip med-4.0.0.tar.gz
tar -xvf med-4.0.0.tar
cd med-4.0.0
```

To compile the *med file* library type:

```
./configure --prefix=/home/USERNAME/telemac/optionals/med-4.0.0 --with-hdf5=/home/USERNAME/telemac/optionals/hdf5 --disable-python
make
make install
```

The flag `--prefix` sets the installation directory and `--width-hdf5` tells the med library where it can find the *hdf5* library. Thus, adapt `/home/USERNAME/telemac/optionals/hdf5` to your local `<install_path>` of the *hdf5* library. Both flags do not accept relative paths (`~/telemac/...`), and therefore, we need to use the absolute paths (`home/USERNAME/telemac/...`) here.

```{admonition} Why *--disable-python*?
:class: note, dropdown
We need to disable Python for the *med file* library because this feature would require *SWIG* version 2.0 and it is not compatible with the current versions of *SWIG* (4.x). Because *SWIG* has no full backward compatibility, the only option is to disable Python integrity for the *med file* library. Otherwise, Python integrity could be implemented by installing Python developer kits ( `sudo apt install python3-dev`  and  `sudo apt install python3.7-dev` ) and using the configuration `./configure --with-hdf5=/home/USERNAME/Telemac/hdf5 PYTHON_LDFLAGS='-lpython3.7m' --with-swig=yes`. To find out what version of Python is installed, type `python -V`.
```


The installation of the *med file* library on Linux is also documented in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_med).

```{admonition} Permission denied?
:class: attention, dropdown
If you consistently get ***permission denied*** messages, you are probably installing Telemac in a directory where you should not install it. If your are sure about the ownership of the installation directory, you may unlock all read and write rights for the `telemac` directory with the following command: `sudo -R 777  /home/USERNAME/telemac` (replace `USERNAME` with the user for whom TELEMAC is installed).
```

Finally, **remove the `temp` folder** to avoid storing garbage:

```
cd ~/telemac/optionals
sudo rm -r temp
```

### AED2

***Estimated duration: < 5 minutes.***

To use TELEMAC's water quality (***waqtel***) module, the *AED2* is (partially) required. In some versions of TELEMAC, the make files for installing *AED2* are provided with the `git` repository in the *optionals* folder. Otherwise, download and unpack the *aed2* folder from the manual installation sources on [opentelemac.org](http://www.opentelemac.org/index.php/component/jdownloads/summary/39-manual-installation-sources/2126-aed2?Itemid=54). Then, to install *AED2*, *cd* to the *aed2* folder and run `make`:

```
cd ~/telemac/optionals/aed2
make
```

```{note}
*AED2* is not needed for the tutorials on this website and the installation of this module can be skipped.
```

(compile-tm)=
## Compile TELEMAC

### Adapt and Verify Configuration File (systel.x.cfg)

***Estimated duration: 2-20 minutes.***


Two options are described in this section for setting up a configuration file: (i) a modification (reduced module availability) of the default-available `~/telemac/configs/systel.edf.cgf` configuration file, and (ii) extended descriptions for setting up a custom configuration file. Option (i) provides a powerful HPC environment, but does not include the installation of the excludes [AED2 (waqtel)](http://wiki.opentelemac.org/doku.php?id=installation_linux_aed), [MUMPS](http://mumps.enseeiht.fr/), and [GOTM (general ocean)](http://wiki.opentelemac.org/doku.php?id=installation_linux_gotm) modules.

`````{tab-set}
````{tab-item} EDF Template

To facilitate setting up the `systel` file, use our edf-based template: right-click on [this download of systel.edfHy.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/edf/systel.edfHy.cfg) > *Save Link As...* > `~/telemac/configs/systel.edfHy.cfg`, which was tested on Debian 10, Debian 11, and Linux Mint 21.3.

The `systel.edfHy.cfg` is designed to be used with the `S10.gfortran.dyn` configuration, for which we removed all dependencies of AED2, MUMPS, and GOTM. That is, none of the flags `[flags_mumps] [flags_aed] [flags_gotm]` is enabled and they were removed from the `S10.gfortran.dyn` configuration, which is fully sufficient for running the {ref}`Telemac tutorials <chpt-telemac>` in this eBook.

```{admonition} How to add AED2, MUMPS, and GOTM
:class: warning

To add AED2, MUMPS, and GOTM functionality install the corresponding modules in the `optionals/` directory and use the default `systel.edf.cfg` configuration file. The installation of AED2, MUMPS, and GOTM is described in the [Telemac installation wiki](http://wiki.opentelemac.org/doku.php?id=installation_on_linux), though not straight forward because multiple links and additional dependencies are outdated.
```
````

````{tab-item} Custom Setup

```{admonition} Python API Not Set Up
:class: warning

The following descriptions for setting up a custom `systel.X.cfg` configuration file do not enable Telemac's Python API. For enabling the Python API, follow the template-based installation instructions, or use `systel.edf.cfg`.
```

The configuration file will tell the compiler how flags are defined and where optional software lives. Here, we use the configuration file `systel.cis-debian.cfg`, which lives in `~/telemac/configs/`. In particular, we are interested in the following section of the file:

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
libs_all:   /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so /home/telemac/metis/build/lib/libmetis.a
```


The configuration file contains other configurations such as a *scalar* or a *debug* configuration for compiling TELEMAC. Here, we only use the *Debian gfortran open MPI* section that has the configuration name `[debgfopenmpi]`. To verify if this section if correctly defined, check where the following libraries live on your system (use Terminal and `cd` + `ls` commands or Debian's *File* browser):

* *Metis* is typically located in `~/telemac/optionals/metis/build` (if you used this directory for `<install_path>`), where `libmetis.a` typically lives in `~/telemac/optionals/metis/build/lib/libmetis.a`
* *Open MPI*'s *include* folder is typically located in `/usr/lib/x86_64-linux-gnu/openmpi/include`
* *Open MPI* library typically lives in `/usr/lib/x86_64-linux-gnu/openmpi/libmpi.so`<br>The number **40.20.3** may need to be added after **libmpi.so** when your system is based on Debian 10.
* *mpiexec* is typically installed in `/usr/bin/mpiexec`
* *mpif90* is typically installed in `/usr/bin/mpif90`
* If installed, *AED2* typically lives in `~/telemac/optionals/aed2/`, which should contain the file `libaed2.a` (among others) and the folders *include*, *obj*, and *src*.

Then open the configuration file in *VIM* (or any other text editor) to verify and adapt the *Debian gfortran open MPI* section:

```
cd ~/telemac/configs
vim systel.edfHy.cfg
```

```{admonition} Enable Parallelism
:name: parcmd
Make the following adaptations in *Debian gfortran open MPI* section to enable parallelism:

* Remove `par_cmdexec` from the configuration file; that means delete the line (otherwise, parallel processing will crash with a message that says *cannot find PARTEL.PAR*):<br>`par_cmdexec:   <config>/partel < PARTEL.PAR >> <partel.log>`
* Find `libs_all` to add and adapt the following items:
    + *metis* (all *metis*-related directories to `/home/USERNAME/telemac/optionals/metis/build/lib/libmetis.a`).
    + *openmpi* (correct the library file to `/usr/lib/x86_64-linux-gnu/openmpi/libmpi.so` or wherever `libmpi.so.xx.xx.x` lives on your machine).
    + *med* including *hdf5* (`~/telemac/optionals/`).
    + *aed2* (`~/telemac/optionals/aed2/libaed2.a`).

`libs_all:    /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so /home/USERNAME/telemac/optionals/metis/build/lib/libmetis.a /home/USERNAME/telemac/optionals/aed2/libaed2.a /home/USERNAME/telemac/optionals/med-4.0.0/lib/libmed.so /home/USERNAME/telemac/optionals/hdf5/lib/libhdf5.so`

* Add the `incs_all` variable to point include *openmpi*, *med*, and *aed2*:

`incs_all: -I /usr/lib/x86_64-linux-gnu/openmpi/include -I /home/USERNAME/telemac/optionals/aed2 -I /home/USERNAME/telemac/optionals/aed2/include  -I /home/USERNAME/telemac/optionals/med-4.0.0/include`

* Search for *openmpi* in `libs_all` and
* Search for `cmd_obj:` definitions, add `-cpp` in front of the `-c` flags, `-DHAVE_AED2`, and `-DHAVE_MED`. For example:

`cmd_obj:    /usr/bin/mpif90 -cpp -c -O3 -DHAVE_AED2 -DHAVE_MPI -DHAVE_MED -fconvert=big-endian -frecord-marker=4 <mods> <incs> <f95name>`

An additional keyword in the configurations is `options:` that accepts multiple keywords including `mpi`, `api` (*TelApy* - *TELEMAC's Python API*), `hpc`, and `dyn` or `static`. The provided `cfg` file primarily uses the `mpi` keyword. To use other installation options (e.g., HPC or dynamic), read the instructions for HPC installation on [opentelemac.org](http://wiki.opentelemac.org/doku.php?id=installation_on_linux) and have a look at the most advanced default config file from EDF (`~/telemac/configs/systel.edf.cfg`).
```
````
`````


### Setup Python Source File

***Estimated duration: 4-20 minutes.***

A Python source file lives in `~/telemac/configs`, where also a template called `pysource.template.sh` is available. This section guides through either using our `pysource.gfortranHPC.sh` (without AED2 and MUMPS), or a custom source file.

`````{tab-set}
````{tab-item} Template Usage

To facilitate setting up the `pysource.gfortranHPC.sh` file, our template is designed for use with the above-described `systel.edfHy.cfg` configuration file, and it is  based on the default-provided `pysource.template.sh`. Either [download pysource.gfortranHPC.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/edf/pysource.gfortranHPC.sh) > *Save Link As...* > `~/telemac/configs/pysource.gfortranHPC.sh` or create a new pysource file with the following contents:

```
### TELEMAC settings -----------------------------------------------------------
###
# Path to telemac root dir
export HOMETEL=/home/USER-NAME/telemac/v8p4r0
# Adding python scripts to PATH
export PATH=$HOMETEL/scripts/python3:.:$PATH
# Configuration file
export SYSTELCFG=$HOMETEL/configs/systel.edfHy.cfg
# Name of the configuration to use
export USETELCFG=S10.gfortran.dyn
# Path to this file
export SOURCEFILE=$HOMETEL/configs/pysource.gfortranHPC.sh
### Python
# To force python to flush its output
export PYTHONUNBUFFERED='true'
### API
export PYTHONPATH=$HOMETEL/scripts/python3:$PYTHONPATH
export LD_LIBRARY_PATH=$HOMETEL/builds/$USETELCFG/lib:$HOMETEL/builds/$USETELCFG/wrap_api/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$HOMETEL/builds/$USETELCFG/wrap_api/lib:$PYTHONPATH
###
### EXTERNAL LIBRARIES -----------------------------------------------------------
###
### METIS ----------------------------
###
### COMPILERS -----------------------------------------------------------
###
# Here are a few examples for external libraries
export SYSTEL=$HOMETEL/optionals

### MPI -----------------------------------------------------------
export MPIHOME=/usr/bin/mpifort.openmpi
export PATH=/usr/lib/x86_64-linux-gnu/openmpi:$PATH
export LD_LIBRARY_PATH=$PATH/lib:$LD_LIBRARY_PATH
###
### EXTERNAL LIBRARIES -----------------------------------------------------------
###
### HDF5 -----------------------------------------------------------
export HDF5HOME=$SYSTEL/hdf5
export LD_LIBRARY_PATH=$HDF5HOME/lib:$LD_LIBRARY_PATH
export LD_RUN_PATH=$HDF5HOME/lib:$MEDHOME/lib:$LD_RUN_PATH
### MED  -----------------------------------------------------------
export MEDHOME=$SYSTEL/med-4.0.0
export LD_LIBRARY_PATH=$MEDHOME/lib:$LD_LIBRARY_PATH
export PATH=$MEDHOME/bin:$PATH
### MUMPS -------------------------------------------------------------
#export MUMPSHOME=$SYSTEL/LIBRARY/mumps/gnu
#export SCALAPACKHOME=$SYSTEL/LIBRARY/scalapack/gnu
#export BLACSHOME=$SYSTEL/LIBRARY/blacs/gnu
### METIS -------------------------------------------------------------
export METISHOME=$SYSTEL/metis/build/
export LD_LIBRARY_PATH=$METISHOME/lib:$LD_LIBRARY_PATH
```

**Make sure do adapt the variable `HOMETEL=/home/USER-NAME/telemac/v8p4r0`.**

```{admonition} AED2, MUMPS, and GOTM deactivated
:class: note

[AED2 (waqtel)](http://wiki.opentelemac.org/doku.php?id=installation_linux_aed), [MUMPS](http://mumps.enseeiht.fr/), and [GOTM (general ocean)](http://wiki.opentelemac.org/doku.php?id=installation_linux_gotm) are deactivated in our template. To activate them, uncomment (i.e., remove `#`) before the MUMPS variables, add AED2 and GOTM variables, and use the `systel.edf.cfg` configuration file.

```

````
````{tab-item} Custom Bash File

Here, we use the template to create our own Python source file called `pysource.gfortranHPC.sh` tailored for compiling the parallel version of TELEMAC on Debian Linux with the *Open MPI* library. The Python source file starts with the definition of the following variables:

* `HOMETEL`: The path to the `telemac/VERSION` folder (`<root>`).
* `SYSTELCFG`: The path to the above-modified configuration file  (`systel.edfHy.cfg`) relative to `HOMETEL`.
* `USETELCFG`: The name of the configuration to be used (`debgfopenmpi`). Configurations enabled are defined in the `systel.*.cfg` file, in the brackets (`[debgfopenmpi]`) directly below the header of every configuration section.
* `SOURCEFILE`: The path to this file and its name relative to `HOMETEL`.

More definitions are required to define TELEMAC's *Application Programming Interface* (*API*), (parallel) compilers to build TELEMAC with *Open MPI*, and external libraries located in the `optionals` folder. The following code block shows how the Python source file `pysource.gfortranHPC.sh` should look like. Make sure to **verify every directory on your local file system**, use your *USERNAME*, and take your time to get all directories right, without typos (critical task).

```
### TELEMAC settings -----------------------------------------------
###
# Path to Telemac s root dir
export HOMETEL=/home/USERNAME/telemac-mascaret
# Add Python scripts to PATH
export PATH=$HOMETEL/scripts/python3:.:$PATH
# Configuration file
export SYSTELCFG=$HOMETEL/configs/systel.edfHy.cfg
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
export MEDHOME=$SYSTEL/med-4.0.0
export LD_LIBRARY_PATH=$MEDHOME/lib:$LD_LIBRARY_PATH
export PATH=$MEDHOME/bin:$PATH
### METIS ----------------------------------------------------------
export METISHOME=$SYSTEL/metis/build/
export LD_LIBRARY_PATH=$METISHOME/lib:$LD_LIBRARY_PATH
### AED ------------------------------------------------------------
export AEDHOME=$SYSTEL/aed2
export LD_LIBRARY_PATH=$AEDHOME/obj:$LD_LIBRARY_PATH
```
````
`````

(tm-compile)=
### Compile

***Estimated duration: 20-30 minutes (compiling takes time).***

The compiler is called through Python and the above-created bash script ( `pysource.gfortranHPC.sh` or `pysource.openmpi.sh`). Thus, the Python source file `pysource.gfortranHPC.sh` knows where helper programs and libraries are located, and it knows the configuration to be used. With the Python source file, compiling TELEMAC becomes an easy task in Terminal. First, load the Python source file `pysource.gfortranHPC.sh` as source in Terminal, and then, test if it is correctly configured by running `config.py`:

```
cd ~/telemac/configs
source pysource.gfortranHPC.sh
config.py
```

Running `config.py` should produce a character-based image in Terminal and end with `My work is done`. If that is not the case and error messages occur, *attentively read the error messages* to identify the issue (e.g., there might be a typo in a directory or file name, or a misplaced character somewhere in `pysource.gfortranHPC.sh` or `systel.edfHy.cfg`).
When `config.py` ran successfully, start compiling TELEMAC with the `--clean` flag to avoid any interference with earlier installations:

```
compile_telemac.py --clean
```

The compilation should run for a while (can take more than 30 minutes) and successfully end with the phrase `My work is done`.

```{admonition} Troubleshoot errors in the compiling process
:class: attention
If an error occurred in the compiling process, traceback error messages and identify the component that did not work. Revise setting up the concerned component in this workflow very thoroughly. Do not try to re-invent the wheel - the most likely problem is a tiny little detail in the files that you created on your own. Troubleshooting may be a tough task, in particular, because you need to put into question your own work.
```

(testrun)=
### Test TELEMAC

***Estimated duration: 5-10 minutes.***

Once Terminal was closed or any clean system start-up requires to load the TELEMAC source environment in Terminal before running TELEMAC:

```
cd ~/telemac/configs
source pysource.gfortranHPC.sh
config.py
```

To run and test if TELEMAC works, use a pre-defined case from the provided `examples` folder:

```
cd ~/telemac/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
```

```{admonition} Examples are not working?
:class: error, dropdown

If running any test case provided in the `/examples/` folder crashes, **worry not!**. Your installation is most likely OK if the installation finished without errors and the `config.py` runs smoothly. However, for being able to run the examples, you will need to install {ref}`all git requirements (cf. above descriptions) <tm-git-requirements>`, re-download the TELEMAC git repository, and re-compile TELEMAC (basically: start over, beginning with the {ref}`git section <tm-git-requirements>`).
```


To test if parallelism works, install *htop* to visualize CPU usage:

```
sudo apt update
sudo apt install htop
```

Start htop's CPU monitor with:

```
htop
```

In a new Terminal tab run the above TELEMAC example with the flag `--ncsize=N` (NCSIZE), where `N` is the number of processors (CPUs) to use for parallel computation (make sure that `N` CPUs are also available on your machine):

```
cd ~/telemac/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas --ncsize=4
```

Alternatively, the `--nctile` and `--ncnode` flags can be used to define a number of core per node (NCTILE) and a number of nodes (NCNODE), respectively. The relationship between these flags is `NCSIZE = NCTILE * NCNODE`. Thus, the following two lines yield the same result (run in `cd ~/telemac/examples/telemac2d/donau`):

```
telemac2d.py t2d_donau.cas --nctile=4 --ncnode=2
telemac2d.py t2d_donau.cas --ncsize=8
```


```{admonition} Cannot find <<PARTEL.PAR>>?
:class: error, dropdown
If there is an error message such as **`Cannot find << PARTEL.PAR >>`** ... **`TypeError: can only concatenate str (not ...) to str`**, make sure that `par_cmdexec` is removed from the configuration file ({ref}`see above <parcmd>`).
```

When the computation is running, observe the CPU charge. If the CPUs are all working with different percentages, the parallel version is working well.

TELEMAC should startup, run the example case, and again end with the phrase `My work is done`. To assess the efficiency of the number of CPUs used, vary `ncsize`. For instance, the *donau* example (`cd ~/telemac/examples/telemac2d/donau`) ran with `telemac2d.py t2d_donau.cas --ncsize=4` may take approximately 1.5 minutes, while `telemac2d.py t2d_donau.cas --ncsize=2` (i.e., half the number of CPUs) takes approximately 2.5 minutes. The computing time may differ depending on your hardware, but note that doubling the number of CPUs does not cut the calculation time by a factor of two. So to optimize system resources, it can be reasonable to start several simulation cases on fewer cores than one simulation on multiple cores.

```{admonition} Troubleshoot *No such file or directory*
:class: attention, dropdown
If you interrupted the Terminal session and get an error message such as `No such file or directory`, you may need to re-define (re-load) the Python source file: In Terminal go (`cd`) to `~/telemac/configs`, type `source pysource.gfortranHPC.sh` > `config.py`, and then go back to the `examples` folder to re-run the example.
```

### Generate Telemac Docs

TELEMAC comes with many application examples in the subdirectory `~/telemac/examples/` and the documentation plus reference manuals can be generated locally. To this end, make sure to source the TELEMAC environment: 

```
source ~/telemac/configs/pysource.gfortranHPC.sh
```

To generate the user manual type (takes a while):

```
doc_telemac.py
```

To generate the reference manual type:

```
doc_telemac.py --reference
```

To create the documentation of all example causes use:

```
validate_telemac.py
```

```{note}
The `validate_telemac.py` essentially runs through all examples, but some of them are broken and will cause the script to crash. This may also happen if not all modules are installed (e.g., *Hermes* is missing).
```



## Utilities (Pre- & Post-processing)

```{admonition} More Pre- and Post-processing Software
:class: note

More software for dealing with Telemac pre- and post-processing is available in the form of {ref}`SALOME <salome-install>` and ParaView.
```

(qgis-telemac)=
### QGIS (Linux and Windows)

***Estimated duration: 5-10 minutes (depends on connection speed).***

QGIS is a powerful tool for viewing, creating, and editing geospatial data that can be useful in pre- and post-processing. Detailed installation guidelines are provided in the {ref}`qgis-install` installation instructions and the {ref}`QGIS tutorial <qgis-tutorial>`in this eBook. For working with TELEMAC, consider installing the following **QGIS Plugins** (*Plugins* > *Manage and Install Plugins...*):

* [Telemac Tools](https://plugins.qgis.org/plugins/telemac_tools/) is an experimental mesh generator plugin for `*.slf` files developed by *Artelia*. Make sure to check the **experimental plugins** box in the **Settings** of QGIS' plugins window.
* {ref}`BASEmesh <get-basemesh>` enables to create a {term}`SMS 2dm` file that can be converted to a selafin geometry for TELEMAC (read more in the {ref}`QGIS pre-processing tutorial for TELEMAC <tm-qgis-prepro>`).
* *PostTelemac* visualizes `*.slf` (and others such as `*.res`) geometry files at different time steps.
* *DEMto3D* enables to export *STL* geometry files for working with *SALOME* and creating 3D meshes.

Note that *DEMto3D* will be available in the *Raster* menu: *DEMto3D* > *DEM 3D printing*.

(bluekenue)=
### BlueKenue (Windows or Linux+Wine)

***Estimated duration: 10 minutes.***

[BlueKenue](https://nrc.canada.ca/en/research-development/products-services/software-applications/blue-kenuetm-software-tool-hydraulic-modellers)<sup>TM</sup> is a pre- and post-processing software provided by the [National Research Council Canada](https://nrc.canada.ca/en), which is compatible with TELEMAC. It provides similar functions as the [Fudaa](http://www.opentelemac.org/index.php/latest-news-development-and-distribution/240-fudaa-mascaret-3-6) software featured by the TELEMAC developers and additionally comes with a powerful mesh generator. It is particularly for the mesh generator that you want to install BlueKenue<sup>TM</sup> after [downloading the latest version](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (login details in the [Telemac Forum](http://www.opentelemac.org/index.php/assistance/forum5/blue-kenue)). Next, there are two options for installing BlueKenue<sup>TM</sup> depending on your platform:

1. On Windows: directly use the BLueKenue (`.msi`) installer.
1. On Linux: use [Wine amd64](https://wiki.debian.org/Wine) through {ref}`PlayOneLinux <play-on-linux>` to install BlueKenue<sup>TM</sup> on *Linux*. For Ubuntu (Debian) - based Linux, the {ref}`PlayOnLinux <play-on-linux>` section in this eBook provides detailed instructions. Direct installation of BlueKenue through Wine only is discouraged because of severe compatibility issues.

Note the typical installation directories of BlueKenue<sup>TM</sup> executable are:

* 32-bit version is typically installed in `"C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"`
* 64-bit version is typically installed in `"C:\\Program Files\\CHC\\BlueKenue\\BlueKenue.exe"`

Additionally, the Canadian Hydrological Model Stewardship (CHyMS) provides more guidance for installing BlueKenue<sup>TM</sup> on other platforms than *Windows* on their [FAQ](https://chyms.nrc.gc.ca/docs/FAQ.html) page in the troubleshooting section ([direct link to *how to run Blue Kenue on another operating system*](https://chyms.nrc.gc.ca/docs/FAQ.html#troubleshooting-how-run-on-another-os)).

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
* Start Fudaa-PrePro from Terminal or *Prompt*
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
