(telemac-autoinstall)=
# TELEMAC (Auto-Installation)


## Preface

This tutorial walks you through installing [open TELEMAC-MASCARET](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/) and Ubuntu-based systems with **automatic installer** scripts. **Plan for roughly 1-2 hours and a stable internet connection; the downloads exceed 1.4 GB.** For detailed installation instructions, go to the {ref}`detailed TELEMAC installation page <telemac-install>`.


(telemac-autoinstall-requirements)=
## Requirements

### System packages

`````{tab-set}
````{tab-item} Debian 12

On Debian 12, ask your system administrator to sudo-install the following packages via aptitude:

```bash
sudo apt update

sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-dev libmumps-seq-dev libscalapack-openmpi-dev libmedc-dev libmed-tools python3-pytest-cython python3-sphinx python3-alabaster python3-cftime libcminpack1 python3-docutils python3-h5py python3-imagesize clang python3-netcdf4 python3-nlopt python3-nose python3-numpydoc python3-patsy python3-psutil liblzf1 python3-stemmer python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev liblapacke-dev libxml2-dev llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff-dev libgeotiff-dev libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```

````

````{tab-item} Ubuntu 24 / Mint 22
On Ubuntu 24 (or Mint 22), ask your system administrator to sudo-install the following packages via aptitude:

```bash
sudo apt update
sudo apt install -y --no-install-recommends  python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1 libegl1 libxrandr2 libxss1 libxcursor1 libxcomposite1 alsa-base libxi6 libxtst6  python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins  libmedc11t64 libmedc-dev libmed-tools libmed11 libmed-dev libmedimport0v5 libmedimport-dev  libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-seq-dev libmumps-dev  libscalapack-openmpi-dev python3-pytest-cython python3-sphinx python3-alabaster python3-cftime  libcminpack1 python3-docutils libfreeimage3 python3-h5py python3-imagesize liblapacke  clang python3-netcdf4 libnlopt0 libnlopt-cxx0 python3-nlopt python3-nose python3-numpydoc  python3-patsy python3-psutil libtbb12 libxml++2.6-2v5 liblzf1 python3-stemmer  python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels  python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev  doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev libxml2-dev  llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev  libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev  libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev  libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff5-dev libgeotiff-dev  libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev  libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```
````
`````

Note that the automatic installer script might detect additional packages required.

### Set up installation paths

TELEMAC will be downloaded (git-cloned) from its GitLab repository into a directory you choose, and that will be referred to as **ROOT** directory in the following. Also, SALOME will be downloaded and installed in this ROOT directory. Select one of the following setups:

* Single user without admin rights: `ROOT=/home/<USERNAME>/opt` (that is, `ROOT=$HOME/opt`) (XDG-conformant alternative: `ROOT=$HOME/.local`)
* Shared use without root: only if a group-writable location already exists, for example an NFS share like `ROOT=/srv/shared/telemac`
* System-wide (admin required) on Debian-based systems: preferred `ROOT=/usr/local` (binaries in `/usr/local/bin`, libraries in `/usr/local/lib`); `ROOT=/opt` is also acceptable for a self-contained tree


### SALOME

Choosing the right version of SALOME cannot be reasonably automated, so find and download the latest version of SALOME, and save it in the ROOT directory where you want to install Telemac.

1. Confirm your Linux version: 
  * Debian: cat /etc/os-release
  * Mint: `lsb_release -a`
  * Ubuntu: `inxi -Sx` (also works on Mint)

2. Download the SALOME build
  * Go to the [official SALOME download form](https://www.salome-platform.org/?page_id=2430) 
  * Pick the latest version with the Debian/Ubuntu build (that matches the Ubuntu/Mint base); or pick the less frequently updated "Linux Universal"

3. Verify the checksum: from SALOME's md5 page, fetch the matching `.md5` file for your archive and verify locally
  * Example for the 9.15 tarball: `md5sum SALOME-9.15.0.tar.gz`
  * Compare with "SALOME-9.15.0.tar.gz.md5" from the [md5 page](https://www.salome-platform.org/?page_id=2818) - **don't skip this!**

### Get the installer scripts

* Debian 12 users download [telemac_debian12_installer.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/telemac_debian12_installer.sh) and save it in the ROOT directory.
* Mint 22 / Ubuntu 24 users download [telemac_ubuntu24_installer.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/telemac_ubuntu24_installer.sh) and save it in the ROOT directory.

## Run installers

### Installation pattern
Note that you might need **admin (sudo) rights** for installing additional system packages and that the installation can take a while because the script downloads Telemac. The script installs by default Telemac v9.0.0. To install another version, use the `--tag "TAG"` option when running the scripts; latest tags can be found at [https://gitlab.pam-retd.fr/otm/telemac-mascaret.git](https://gitlab.pam-retd.fr/otm/telemac-mascaret.git).

To run the installer, tap (replace `ROOT` with your ROOT directory and `SALOME-x.xx.xSRC.tar.gz` with the name of the SALOME tarball that you downloaded):

`````{tab-set}
````{tab-item} Debian 12
```bash
cd ROOT
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

After finishing the installation, the Telemac environment can be loaded and compiled as follows:
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

Note that recompiling is necessary in the case of the Debian12 installer (not required for Ubuntu/Mint).

````

````{tab-item} Ubuntu 24 / Mint 22
```bash
cd ROOT
chmod +x telemac_ubuntu24_installer.sh
./telemac_ubuntu24_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

After finishing the installation, the Telemac environment can be loaded as follows:
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.mint22.sh
```
````
`````

The installer scripts will clone the `telemac-mascaret` GitLab repo (with the assigned tag), and a `salome` folder, in which it unpacks the SALOME tarball. If you encounter errors with SALOME, check out the {ref}`detailed SALOME installation instructions <salome-install>` in the section on the "manual" installation of Telemac.

````{admonition} Test SALOME
:class: tip

SALOME is installed in the `ROOT/salome` now, and you can run the GUI as follows:

```bash
cd ROOT/salome
./salome
```
````

To test the installation, run the `config.py` script (after source-ing of the Telemac environment):

```bash
config.py
```


### Installation example

Assume you are working on Debian 12, accordingly you downloaded `SALOME-9.15.0-native-DB12-SRC.tar.gz`, defined the ROOT directory as `/home/HyInfo/opt/`, and downloaded `telemac_debian12_installer.sh`. Thus, the installation can be started with these commands:

```bash
cd /home/HyInfo/opt
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "/home/HyInfo/opt" --salome-tar "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz" --salome-md5 "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz"
```

Now, activate the Telemac environment and compile as follows:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

### Installation example with another version

Assume you are working on Debian 12, accordingly you downloaded `SALOME-9.15.0-native-DB12-SRC.tar.gz`, defined the ROOT directory as `/home/HyInfo/opt/`, downloaded `telemac_debian12_installer.sh`, and want to **install Telemac v9.5.0** (if that existed at https://gitlab.pam-retd.fr/otm/telemac-mascaret.git). This installation can be started with these commands:

```bash
cd /home/HyInfo/opt
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "/home/HyInfo/opt" --tag="v9.5.0" --salome-tar "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz" --salome-md5 "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz"
```

Now, activate the Telemac environment and compile Telemac as follows:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

### Re-Install

To fix/reinstall an an existing installation:

1. Navigate to your TELEMAC directory: 

  ```bash
  cd ~/opt/telemac-mascaret
  ```

2. Re-run the installer with `--skip-apt` to regenerate config files (assumes you are using a newer version of the installer script)
  
  ```bash
  chmod +x ./telemac_debian12_installer.sh
  ./telemac_debian12_installer.sh --skip-apt --root "/ROOTDIR" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
  ```

3. Regenerate by re-running config and compile:

  ```bash
  source configs/pysource.debian12.sh
  compile_telemac.py --clean
  ```


(testrun-autoinstaller)=
## Test TELEMAC

***Estimated duration: 5-10 minutes.***

Load the TELEMAC environment:

`````{tab-set}
````{tab-item} Debian 12
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.debian12.sh
```
````

````{tab-item} Ubuntu 24 / Mint 22
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.mint22.sh
```
````
`````


Run a predefined case from the `examples` folder:

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
```

To verify parallelism, install *htop* to visualize CPU usage:

```bash
sudo apt update
sudo apt install htop
```

Start the CPU monitor:

```bash
htop
```

In a new terminal tab, run a TELEMAC example with the `--ncsize=N` flag, where `N` is the number of logical CPUs to use (ensure at least `N` are available):

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas --ncsize=4
```

Alternatively, use `--nctile` and `--ncnode` to specify cores per node (NCTILE) and number of nodes (NCNODE), respectively, with `NCSIZE = NCTILE * NCNODE`. The following two commands are equivalent (from `~/opt/telemac-mascaret/examples/telemac2d/donau`):

```bash
telemac2d.py t2d_donau.cas --nctile=4 --ncnode=2
telemac2d.py t2d_donau.cas --ncsize=8
```

```{admonition} Got errors?
:class: error, dropdown

If there are severe errors, the automatic installer might not have worked for your system (or subversion). In this case, it is safest, to start over and {ref}`install Telemac manually <telemac-install>`.

````


### Generate TELEMAC Documentation

TELEMAC includes many application examples under `/telemac-mascaret/examples/`, and you can build the user and reference manuals locally. First, load the TELEMAC environment:

```bash
source ~/opt/telemac-mascaret/configs/pysource.mint22.sh
```

To generate the user manual (this can take a while and requires latex, that is, `texlive` on Debian/Ubuntu):

```bash
doc_telemac.py
```

To generate the reference manual:

```bash
doc_telemac.py --reference
```

To create documentation and validation reports for all example cases:

```bash
validate_telemac.py
```

```{note}
`validate_telemac.py` iterates through many examples. Some may fail if optional modules are not installed (e.g., HERMES) or if an example is outdated. Building PDFs typically requires a LaTeX toolchain (for example, `texlive` on Debian/Ubuntu); install it if the documentation step reports missing LaTeX executables.
```



## Utilities (Pre- & Post-processing)

To install pre- and post-processing utilities, refer to the instructions in the {ref}`manual installation section <install-telemac-utilities>`, such as BlueKenue or the Q4TS plugin in QGIS. Note that for the Q4TS plugin, your SALOME executable path is `/ROOT/salome/salome`, and your Telemac *environnement* script is `/ROOT/telemac-mascaret/configs/pysource.debian12.sh` (or `/ROOT/telemac-mascaret/configs/pysource.mint22.sh` if you installed on Ubuntu/Mint).



