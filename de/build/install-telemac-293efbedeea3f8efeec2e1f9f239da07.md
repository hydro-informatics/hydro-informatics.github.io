---
description: Schritt für Schritt Installationsanleitung für offene TELEMAC-MASCARET auf Debian Linux und Ubuntu, die alle Abhängigkeiten, Zusammenstellung und Umgebungskonfiguration für hydromorphodynamische Simulationen abdeckt.
---

(telemac-install)=
# TELEMAC (Installation)


Vorwort


This tutorial walks you through installing [open TELEMAC-MASCARET](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/)-based systems (including Ubuntu and derivatives like Linux Mint). **Plan for roughly 1-2 hours and a stable internet connection; the downloads exceed 1.4 GB.**

```{admonition} Developer instructions
:class: note

The TELEMAC developers provide up-to-date build guidance at [https://gitlab.pam-retd.fr/otm/telemac-mascaret/ > BUILDING.md](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/main/BUILDING.md), though documentation for optional components remains limited.
```

***


Dieser Abschnitt umfasst nur die **Installation* von TELEMAC. Für Tutorials zu hydro(-morpho)dynamischen Modellen mit TELEMAC siehe die {ref}`TELEMAC tutorials section <chpt-telemac>`.

Einige Installationsmöglichkeiten stehen zur Verfügung:


`````{tab-set}
````{tab-item} Custom Installation (Recommended)
Weiter lesen und gehen Sie durch die folgenden Abschnitte.
````

````{tab-item} Mint Hyfo VM

Wenn Sie die {ref}`Mint Hyfo Virtual Machine <hyfo-vm>` verwenden, können Sie die Setup-Tutorials hier überspringen. TELEMAC v8p3 ist bereits installiert und konfiguriert, so dass Sie direkt an die {ref}`TELEMAC tutorials <chpt-telemac>`. Behandeln Sie diese VM als Trainingsumgebung: Es ist toll für das Lernen und die Durchführung von Probenfällen, aber es ist nicht für leistungskritische, anwendungstechnische Modellierung gedacht.

Laden Sie die TELEMAC-Umgebung und überprüfen Sie, ob es mit:

```
cd ~/telemac/v8p3/configs
source pysource.hyfo.sh
config.py
```
````
````{tab-item} SALOME-HYDRO
TELEMAC ist auch über die SALOME-HYDRO Software Suite erhältlich, die ein Spinoff von SALOME ist. Die wichtigsten Funktionalitäten von SALOME-HYDRO können jedoch auf ein neues QGIS-Plugin migrieren. Daher empfiehlt dieses eBook die Installation von TELEMAC unabhängig von einer Vor- oder Nachbearbeitungssoftware.
````

````{tab-item} Docker Image

The Austrian engineering office *Flussplan* provides a Docker container of TELEMAC v8 on their [docker-telemac GitHub repository](https://github.com/flussplan/docker-telemac). Note that a Docker container represents an easy-to-install virtual environment that leverages cross-platform compatibility, but affects computational performance. If you have the proprietary Docker software installed and computational performance is not the primary concern for your models, Flussplan's Docker container might be a good choice. For instance, purely hydrodynamic models with small numbers of grid nodes and without additional TELEMAC module implications will efficiently run in the Docker container.

````
`````

(modular-install)=
Grundvoraussetzungen

```{admonition} Good to know
:class: tip

* Installing TELEMAC on a {ref}`Virtual Machine (VM) <chpt-vm-linux>` is a convenient way to get started and to run sample cases, but it is not recommended for application-scale models due to the performance overhead of VMs.
* Get comfortable with the {ref}`Linux Terminal <linux-terminal>`; you will need it to compile and potentially troubleshoot TELEMAC's build workflow.
* Throughout this tutorial, we refer to the package *open TELEMAC-MASCARET* as TELEMAC. *MASCARET* is a one-dimensional (1D) module, while the methods emphasized here focus on two-dimensional (2d) and three-dimensional (3d) modeling.
```

```{admonition} Admin (sudo) rights required for installing basic and optional requirements
:class: attention, dropdown

Superuser privileges (`sudo` for **su**per **do**ers list) are required for many steps in this workflow, such as installing packages, editing system configuration, and writing to system directories. On Debian, sudo access is typically granted by installing `sudo`, adding your account to the `sudo` group, and managing permissions safely with `visudo` (which edits `/etc/sudoers`). For detailed setup instructions, see the tutorial {ref}`Debian Linux <user-rights>` and talk to your system administrator.
```

Working with TELEMAC requires software to download source files, compile them, and run the program. The mandatory software prerequisites for installing TELEMAC on [Debian Linux](https://www.debian.org/) are explained in the following sections.


### Python3

** Geschätzte Dauer: 5-8 Minuten.**

Python3 has been installed by default on Debian since version 10 (Buster), and it is required to run TELEMAC's compiler/launcher scripts. To start Python3, open a Terminal and run `python3`; to exit, use `exit()` or press `Ctrl+D`.

TELEMAC needs the [NumPy](https://numpy.org/) library; most workflows also rely on [SciPy](https://scipy.org/) and [Matplotlib](https://matplotlib.org/). Because TELEMAC is non-standard, having Python headers and a clean environment helps.

Um die gemeinsamen Systempakete zu installieren, führen Sie:

```bash
sudo apt update
sudo apt install python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv
```

````{admonition} Got Qt Errors?
:class: warning, dropdown
Wenn während der Installation ein Fehler auftritt, installieren Sie die erweiterten Abhängigkeiten (includes Qt) mit dem folgenden Befehl:

```
sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
```

Dann wieder versuchen, die Bibliotheken zu installieren.
````

Wenn Sie auf einer älteren Debian-Version sind, die nicht `distutils` in der Standard-Python enthalten ist, installieren Sie auch `python3-distutils`.

To test if the installation was successful, type `python3` in Terminal and import the three libraries:

```bash
Python 3.11.1 (default, Jul  25 2030, 13:03:44) [GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> a = numpy.array((1, 1))
>>> print(a)
[1 1]
>>> exit()
```

None of the three library imports should return an `ImportError` message. To learn more about Python read the section on {ref}`sec-pypckg`.

(tm-git-Anforderungen)=
### Git

** Geschätzte Dauer: <5 Minuten**

Installation and usage of Git are covered in the {ref}`git section of this eBook <chpt-git>`. In addition to what is described there, you will need Git Large File Storage (Git LFS) to handle large assets if a TELEMAC-related repository uses it. On Debian, you usually only need `git` (not `git-all`, which pulls many extras), plus `git-lfs`. Install and initialize:

```bash
sudo apt update
sudo apt install git git-lfs
git lfs install
```

`git lfs install` richtet LFS für Ihr Benutzerkonto ein; so ist es harmlos, auch wenn ein bestimmtes Repository keine LFS verwendet.


### GNU Fortran 95 Compiler (gfortran)

** Geschätzte Dauer: 3-10 Minuten.***

TELEMAC's Python-based build system requires a Fortran compiler; the common choice on Debian is the GNU Fortran compiler (`gfortran`), which is backward-compatible with GNU Fortran 95 and supports newer standards. Debian provides `gfortran` from its standard repositories. To install it, open a terminal and run:

```bash
sudo apt update
sudo apt install gfortran

```

Nach der Installation überprüfen Sie Ihr Setup mit `gfortran --version`; der Compiler muss auf Ihrem `PATH` für TELEMAC Skripte sein, um es zu finden.

```{admonition} If the gfortran installation fails...
:class: attention, dropdown


Ensure the standard Debian "main" component is enabled in your APT sources so the `gfortran` package is available. Edit `/etc/apt/sources.list` as root (or add a file in `/etc/apt/sources.list.d/`), then run `sudo apt update`. Verify availability with `apt-cache policy gfortran` or `apt search gfortran`; note that `gfortran` is a metapackage that installs the current default version (for example, `gfortran-12` or `gfortran-13`). Package details are listed here: [https://packages.debian.org/search?keywords=gfortran](https://packages.debian.org/search?keywords=gfortran).
```

### More Compilers and Essentials

** Geschätzte Dauer: 2-5 Minuten.**

For building TELEMAC and its dependencies, you need C/C++ and CMake. Install Debian's `build-essential` (which provides `gcc`, `g++`, and `make`) and `cmake`; these are required to compile sources, including parallel (MPI) builds, though MPI itself is provided by packages like OpenMPI that you will install later. The `dialog` package is optional but useful because some helper scripts use simple text interfaces. For editing shell scripts you can use `gedit` ([read more](https://wiki.gnome.org/Apps/Gedit), or alternatives such as Nano or Vim). Run:

```bash
sudo apt update
sudo apt install -y build-essential cmake dialog gedit gedit-plugins
```


### Installationspfad einrichten

Bis zu diesem Punkt wurde Software über Debians Paketmanager (APTITUDE, `apt`) installiert. Im Gegensatz dazu wird TELEMAC (d.h. git-cloned) aus dem GitLab-Repository in ein Verzeichnis heruntergeladen, das Sie wählen. Sein Build/install Workflow ist insbesondere nicht standardmäßig, so dass Pfadwahlen wichtig sind. Wählen Sie eine der folgenden Einstellungen:

* Single user without admin rights: `ROOT=/home/<USERNAME>/opt`  (that is, `ROOT=$HOME/opt`)  (XDG-conformant alternative: `ROOT=$HOME/.local`)
* Shared use without root: only if a group-writable location already exists, for example an NFS share like `ROOT=/srv/shared/telemac`
* System-wide (admin required) on Debian-based systems: preferred `ROOT=/usr/local` (binaries in `/usr/local/bin`, libraries in `/usr/local/lib`); `ROOT=/opt` is also acceptable for a self-contained tree

In den folgenden Abschnitten zeigen wir eine Einzelbenutzerinstallation von TELEMAC (einschließlich SALOME) mit `ROOT=/home/HyInfo/opt`.


### Get the TELEMAC Repo

** Geschätzte Dauer: 25-40 Minuten (große Downloads).***

Fetch the TELEMAC sources with Git-LFS. In terminal, create or choose your working directory (here: `/home/HyInfo/opt` - see above), and change (`cd`) into it; for example:

```bash
cd /home/HyInfo/opt
git clone https://gitlab.pam-retd.fr/otm/telemac-mascaret.git
```

Damit wird das Repository in ein Unterverzeichnis namens `telemac-mascaret`. Für schnellere Downloads können Sie einen flachen Klon mit `--depth=1` verwenden, um zu verstehen, dass diese Geschichte begrenzt.

````{admonition} There are many (experimental) branches of TELEMAC available
:class: tip, dropdown

The TELEMAC git repository provides many other TELEMAC versions in the form of development or old-version branches. For instance, the following clones the `upwind_gaia` branch to a local sub-folder called `telemac/gaia-upwind`. After cloning this single branch, compiling TELEMAC can be done as described in the following.

```
git clone -b upwind_gaia --single-branch https://gitlab.pam-retd.fr/otm/telemac-mascaret.git telemac/gaia-upwind
```

Read more about cloning single TELEMAC branches in the [TELEMAC wiki](http://wiki.opentelemac.org/doku.php?id=telemac-mascaret_git_repository).
````

Nach dem Klonen des Repository, identifizieren Sie die neueste markierte Veröffentlichung. Aktualisieren Sie zuerst Ihre Tagliste und zeigen Sie verfügbare Versionen an:

```bash
cd telemac-mascaret
git fetch --tags
git tag -l
```

Ab November 2025 ist die jüngste offizielle Veröffentlichung der GitLab "Releases" Seite `v9.0.0`. Schauen Sie sich das genaue Tag (entdeckt HEAD) an oder erstellen Sie einen Zweig daraus:

```bash
git checkout tags/v9.0.0
```

Wenn ein neuerer Tag später erscheint, ersetzen Sie seinen Namen entsprechend.


Optionale Anforderungen (Parallelismus und andere)

This section walks you through installing additional packages required for parallel execution and working with {ref}`SALOME <salome-install>`'s `.med` files. Confirm that the Terminal finds `gcc` (typically installed via `build-essential`) by running `gcc --version`. The packages below enable parallelism and provide substantial speedups for simulations:

* Nachrichtenübermittlung (MPI)
* Metis

(tm-system-wide-opts)=
### Systemweite Installation
Installieren Sie Voraussetzungen für MPI, Metis, HDF5, MED und MUMPS. Paketnamen unterscheiden sich leicht zwischen Debian und Ubuntu-Derivaten (Mint), so verwenden Sie das unten stehende Paket.

**Debian (aktuelle Stallungen und Tests):**
```bash
sudo apt update
sudo apt install -y libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmetis5 libmumps-dev libmumps-seq-dev libscalapack-openmpi-dev libmedc-dev libmed-tools
```

**Ubuntu und Derivate (fähiges Universum zuerst, wenn noch nicht getan):**
```bash
sudo add-apt-repository -y universe
sudo apt update
sudo apt install -y sudo apt install -y libmedc11t64 libmedc-dev libmed-tools libmed11 libmed-dev libmedimport0v5 libmedimport-dev libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-seq-dev libmumps-dev libscalapack-openmpi-dev
```

Anmerkungen:

* `libopenmpi-dev` and `openmpi-bin` provide MPI headers and `mpirun/mpiexec`.
* `libmetis-dev` supplies the partitioner TELEMAC’s `partel` can use.
* `libhdf5-dev` is required by MED; `libmedc-dev` and `libmed-tools` provide MED I/O support used by SALOME-generated meshes.
* `libmumps-dev` and `libscalapack-openmpi-dev` are common solver backends for large, parallel runs.

Wenn Ihre Veröffentlichung "t64" Pakete verwendet (z.B. `libmedc11t64`), akzeptieren Sie diese Namen wie von `apt` angeboten.

````{admonition} What is behind this (for the blue detail lovers)?
:class: tip, dropdown

***Parallelismus: MPI und Metis***

Um sich nicht auf Distro-Pakete zu verlassen, holen die folgenden Befehle eine gepflegte Gabel von METIS für TELEMAC erstellt. Führen Sie als normaler Benutzer:

```bash
cd ~/telemac/optionals
git clone https://github.com/hydro-informatics/metis.git
cd metis
```

Dieses Repository enthält eine Gabel von Karypis Lab *GKlib*, die zuerst gebaut werden muss:

```bash
cd GKlib
make config cc=gcc prefix=~/telemac/optionals/metis/GKlib openmp=set
make
make install
cd ..
```

Bearbeiten Sie `~/telemac/optionals/metis/Makefile` und stellen Sie oben:

```bash
prefix = ~/telemac/optionals/metis/build/
cc = gcc
```

Dann bauen und installieren Metis:

```bash
make config
make
make install
```

***HDF5 für MED Format-Handler***

**HDF5** ist die zugrunde liegende I/O-Bibliothek von MED. Um eine bestimmte HDF5-Release zu kompilieren, konfigurieren Sie es, um unter einem nicht-System-Präfix zu installieren und Pfade in Ihrem Shell-Profil zu exportieren. Beispiel (genaue Version und Präfix nach Bedarf):

```bash
# build as a normal user
./configure --prefix=$HOME/opt/hdf5
make
make install

# add to your environment
echo 'export PATH=$HOME/opt/hdf5/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$HOME/opt/hdf5/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# verify
h5cc -showconfig
```

**MED Dateibibliothek***

The MED library (from the {ref}`SALOME <salome-install>` ecosystem) provides mesh/result I/O used by many TELEMAC workflows. To build MED yourself, ensure its HDF5 version matches the one used at compile time and disable Python bindings unless you also satisfy the required SWIG/Python headers. Then build it:

```bash
./configure --prefix=$HOME/telemac/optionals/med-4.1.1 --disable-python
make
make install
```

Notes:
* `--disable-python` avoids SWIG version conflicts; enabling Python requires matching `python3-dev` headers and a compatible SWIG release.
* MED version compatibility with your HDF5 build is critical; mixing system HDF5 with a custom-built MED (or vice versa) frequently breaks TELEMAC I/O.

Wenn Sie temporäre Bauverzeichnisse erstellt haben, können Sie sie entfernen:

```bash
cd ~/telemac/optionals
rm -rf temp
```
````

````{admonition} Verify installations
:class: tip

Prüfkopf (Ubuntu/Mint):

```bash
test -d /usr/lib/x86_64-linux-gnu/openmpi/include && echo "OK: Open MPI headers"
test -d /usr/include/hdf5/openmpi && echo "OK: HDF5 (OpenMPI) headers"
```

Testen Sie, dass Bibliotheken lösen:

```bash
ldconfig -p | grep -E 'libmpi\.so|libmedC\.so|libmed\.so|libmetis\.so|libhdf5_openmpi\.so|libhdf5_serial\.so|libhdf5\.so'
```

Test MPI Compiler Wrappers:

```bash
mpif90 --help || true
mpifort --showme:compile --showme:link
```

Sie sollten Fortran-Optionen von den MPI-Wrappers berichtet sehen. Für eine schnelle Laufzeitkontrolle:

```bash
mpirun -n 2 /bin/true && echo "OK: mpirun executes"
```

Additional MPI installation notes are available in the [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).
````


(Salome-install)=
### SALOME

Dieser Workflow erklärt die Installation von SALOME auf Linux Mint / Ubuntu. Die Mindestlaufzeitabhängigkeiten erfordern (mindestens) folgende Anlagen:

```bash
sudo apt update
sudo apt install python3-pytest-cython python3-sphinx python3-alabaster python3-cftime libcminpack1 python3-docutils libfreeimage3 python3-h5py python3-imagesize liblapacke clang python3-netcdf4 libnlopt0 libnlopt-cxx0 python3-nlopt python3-nose python3-numpydoc python3-patsy python3-psutil libtbb12 libxml++2.6-2v5 liblzf1 python3-stemmer python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels python3-toml python-is-python3

```

Die minimalen Kompilierungsabhängigkeiten erfordern folgende Anlagen:

```bash
sudo apt update
sudo apt install pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev liblapacke-dev libxml2-dev llvm-dev libnlopt-dev libnlopt-cxx-dev python3-patsy libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff5-dev libgeotiff-dev libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev python3-statsmodels tcl-dev tk-dev 
```

1. Bestätigen Sie Ihre Linux-Version:
* Debian: Katze /etc/os-Release
* Mint: `lsb_release -a`
* Ubuntu: `inxi -Sx` (auch auf Mint)

2. Download the SALOME build
   * Go to the [official SALOME download form](https://www.salome-platform.org/?page_id=2430) 
   * Pick the latest version with the Ubuntu build (that matches the Mint base); or pick the less frequently updated "Linux Universal"

3. Verify the checksum: from SALOME's md5 page, fetch the matching `.md5` file for your archive and verify locally
   * Example for the 9.15 tarball: `md5sum SALOME-9.15.0.tar.gz`
   * Compare with "SALOME-9.15.0.tar.gz.md5" from the [md5 page](https://www.salome-platform.org/?page_id=2818) - **don't skip this**

4. Wählen Sie irgendwo sauber und gesund; zum Beispiel als `sudo` für das gesamte System (Anpassen Sie den Namen, wenn Sie ein anderes Archiv wählen), oder folgen Sie diesem Workflow fow Installation TELEMAC in `/home/HyInfo/opt/`:
  
    ```bash
    mkdir -p /home/HyInfo/opt/salome
    tar -xzf ~/Downloads/SALOME-9.15.0.tar.gz -C /opt/salome --strip-components=1
    chown -R "$USER":"$USER" /home/HyInfo/opt/salome
    ```

````{admonition} Troubleshoot "chown: invalid group: ..."
:class: error, dropdown

Wenn Sie eine Nachricht wie `chown: invalid group: myuser:myuser` erhalten, bedeutet das, dass `chown` sich beschwert, weil es keine Gruppe namens `myuser` auf dem Computer gibt. Der Besitzer `myuser`@ existiert, aber die Gruppe myuser nicht. Um dies zu beheben, überprüfen Sie zuerst Ihre eigentliche Primärgruppe:

```bash
id
```

Dies sollte so etwas wie `uid=1234(myuser) gid=100(users) groups=100(users),123(othergroup)` zurückgeben. Jetzt haben Sie zwei Möglichkeiten zur Fehlerbehebung:

Option 1: Replace the second `$USER` with your primary group from `id`:

```bash
chown -R "$USER":"$(id -gn "$USER")" /home/HyInfo/opt/salome
```

Option 2 ( robuster): Auto-Detektion Ihrer Primärgruppe verwenden:

```bash
chown -R "$USER":"$(id -gn "$USER")" /home/HyInfo/opt/salome
```
````


5. Lassen SALOME überprüfen Sie Ihr System und installieren, was es verlangt
* Aus dem extrahierten SALOME-Verzeichnis den Anwendungsnamen identifizieren
   ```bash
   cd /home/HyInfo/opt/salome/sat
   ./sat config --list
   ```
   * Use the provided application name; the following descriptions assume the application name is `SALOME-9.15.0-native`
   * Run the built-in checker; it prints what packages might be missing:
   ```bash
   cd /home/HyInfo/opt/salome/sat
   ./sat config SALOME-9.15.0-native --check_system
   ```
* Installieren Sie die Pakete, die es über `apt` auflistet, und führen Sie dann den Scheck, bis er sauber ist.

6. Make sure 3D/OpenGL is OK: verify the proper driver stack (especially for NVIDIA) before launching; read more on [SALOME PLATFORM FAQ](https://www.salome-platform.org/?page_id=428)

7. Launch SALOME from the SALOME folder:
  * if in the `/sat` subfolder first type `cd ..`
  * run salome: `./salome`

Wenn Sie Berechtigungsfehler treffen, stellen Sie sicher, dass Sie an einen Standort, den Sie besitzen, extrahiert oder das Eigentum repariert. Einige Benutzer liefen in Probleme, die seltsame Standorte oder WSL versuchen; halten Sie sich an einen normalen Dateisystempfad, den Sie steuern.

Es gibt auch eine Container-Option: man kann SALOME über Docker/Apptainer ausführen, aber ParaViS/ParaView Beschleunigung innerhalb von Containern ist ursächlich Buggy und bricht oft; die SALOME-Forumdokumente machen Probleme in Docker.



(kompiliert-tm)=
TELEMAC

### Adapt and Verify Configuration File (systel.x.cfg)

** Geschätzte Dauer: 2-20 Minuten.***


The `systel.x.cfg` file tells TELEMAC how to compile and launch its modules on your computer. More specifically, it is TELEMAC's central configuration that defines builds and runtime environments, including compilers, compiler flags, MPI and related options, external libraries, and paths. In practice we use this file to declare flags and to point TELEMAC to optional dependencies. By default, TELEMAC looks for configuration files under `./configs/` (for example `configs/systel.cfg`), and one can override the path with the `SYSTELCFG` environment variable or the `-f` option of the Python launcher.

This section describes the setup of `systel.x.cfg` for:

* Linux Mint 22 (getestet) und Ubuntu 24.04 (erwartet als identisch, noch nicht getestet)
* Debian 12 (Test im Fortschritt)

Beachten Sie, dass wir die Einweg-Installation von TELEMAC unter dem lokalen Home-Verzeichnis `/home/HyInfo/opt/telemac-mascaret` beschreiben und SALOME in `/home/HyInfo/opt/salome` installiert haben.

Note that we did not enable the API, nor the [AED2 (waqtel)](http://wiki.opentelemac.org/doku.php?id=installation_linux_aed) and [GOTM (general ocean)](http://wiki.opentelemac.org/doku.php?id=installation_linux_gotm) modules.

Our `cfg` and `pysource` files define a single build (e.g., `hyinfompiubu` on Mint / Ubuntu) for [TELEMAC v9.0](https://www.opentelemac.org/), enabling `mpi` and `dyn` options and using GNU compilers (`cc=mpicc`, `fc=mpifort` backed by `gfortran`). External libraries are linked via include and library blocks for **OpenMPI, HDF5, MED** (via {ref}`SALOME <salome-install>`), **METIS, and MUMPS** with ScaLAPACK, BLAS, and LAPACK. RPATH entries are added so the runtime can locate HDF5 and related libraries, using paths that match typical Debian and Ubuntu layouts.


`````{tab-set}
````{tab-item} Mint 22 / Ubuntu 24

The following configuration provides a TELEMAC configuration called **hyinfompiubu**. It  enables optimized core flags, position-independent builds, and big-endian unformatted I/O with modified record markers, plus MPI settings on Linux Mint 22 / Ubuntu 24.04. Executables are launched with `mpirun -np <ncsize>`, and meshes are partitioned using `partel`. Build artifacts are placed under `<root>/builds/hyinfompiubu/{bin,lib,obj}`, and the file also defines suffixes, validation paths, and Python F2PY settings (`f2py`, `gnu95`).

Zum Kompilieren von TELEMAC:

1. Download [systel.mint22.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/systel.mint22.cfg) from our GitHub repository, or copy the file contents below into the TELEMAC `/configs` folder, here: `/home/HyInfo/opt/telemac-mascaret/configs`.
2. Open `systel.mint22.cfg` in a text editor (e.g., gedit) and replace the two `/home/HyInfo/opt/salome` path intances with your SALOME installation path.
3. Verify installation paths of optionals, especially HDF5, MED, and Mumps.
4. Save `systel.mint22.cfg` and close the text editor.


```bash
# _____                              _______________________________
# ____/ TELEMAC Project Definitions /______________________________/
#
[Configurations]
configs: hyinfompiubu
#
# _____          _________________________________________________
# ____/ General /_________________________________________________/
#
[general]
language: 2
modules:  system
version:  9.0
options:  mpi dyn
hash_char: #
# Suffixes
sfx_zip:  .tar.gz
sfx_lib:  .a
sfx_obj:  .o
sfx_exe:
sfx_mod:  .mod
# Validation paths
val_root:      <root>/examples
val_rank:      all
# Compilers
cc:      mpicc
cflags:  -fPIC -O3
fc:      mpifort
# Core Fortran flags; TELEMAC expects big-endian unformatted files
fflags:  -cpp -O3 -fPIC -fconvert=big-endian -frecord-marker=4 -DHAVE_MPI
# Build commands
cmd_obj_c: [cc] [cflags] -c <srcName> -o <objName>
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# Splitter and MPI run
par_cmdexec:   <config>/partel < <partel.par> >> <partel.log>
mpi_cmdexec:   mpirun -np <ncsize> <exename>
mpi_hosts:
# ----- Optional library blocks merged in libs_all / incs_all -----
# OpenMPI include dir (Ubuntu 24.04)
inc_mpi:       -I /usr/lib/x86_64-linux-gnu/openmpi/include
# HDF5 (Ubuntu serial headers; change to /usr/include/hdf5/openmpi if using libhdf5-openmpi-dev)
inc_hdf5:  -I /usr/include/hdf5/openmpi
libs_hdf5: -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5
ldflags_opt:   -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi
ldflags_debug: -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi

# MED (from SALOME packages)
inc_med:       -I /home/HyInfo/opt/salome/BINARIES-UB24.04/medfile/include
libs_med:      -L /home/HyInfo/opt/salome/BINARIES-UB24.04/medfile/lib -lmedC -lmed -lmedimport
# METIS
inc_metis:     -I /usr/include
libs_metis:    -L /usr/lib/x86_64-linux-gnu -lmetis
# MUMPS + ScaLAPACK (MPI build)
inc_mumps:     -I /usr/include
libs_mumps:    -L /usr/lib/x86_64-linux-gnu -ldmumps -lmumps_common -lpord -lscalapack-openmpi -lblas -llapack
# Aggregate include and library flags
incs_all: [inc_mpi] [inc_hdf5] [inc_med] [inc_metis] [inc_mumps]
libs_all: [libs_hdf5] [libs_med] [libs_metis] [libs_mumps]

# ===== Build section =====
[hyinfompiubu]
brief: Ubuntu 24.04 gfortran + OpenMPI + MED/HDF5 + METIS + MUMPS/ScaLAPACK
system: linux
mpi:   openmpi
compiler: gfortran
pyd_fcompiler: gnu95
f2py_name: f2py
# build tree under <root>=HOMETEL
bin_dir: <root>/builds/hyinfompiubu/bin
lib_dir: <root>/builds/hyinfompiubu/lib
obj_dir: <root>/builds/hyinfompiubu/obj
# override/extend general flags if needed
options: mpi dyn
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# inherit mods_all/incs_all/libs_all from [general]
mods_all:  -I <config>
```
````

````{tab-item} Debian 12

The following configuration provides a TELEMAC configuration called **hyinfompideb12**. It enables optimized core flags, position-independent builds, and big-endian unformatted I/O with modified record markers, plus MPI settings on Debian 12. Executables are launched with `mpirun -np <ncsize>`, and meshes are partitioned using `partel`. Build artifacts are placed under `<root>/builds/hyinfompideb12/{bin,lib,obj}`, and the file also defines suffixes, validation paths, and Python F2PY settings (`f2py`, `gnu95`).

Zum Kompilieren von TELEMAC:

1. Download [systel.debian12.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/systel.debian12.cfg) from our GitHub repository, or copy the file contents below into the TELEMAC `/configs` folder, here: `/home/HyInfo/opt/telemac-mascaret/configs`.
2. Open `systel.debian12.cfg` in a text editor (e.g., gedit) and replace the two `/home/HyInfo/opt/salome` path intances with your SALOME installation path.
3. Verify installation paths of optionals, especially HDF5, MED, and Mumps.
4. Save `systel.debian12.cfg` and close the text editor.

Wo Pakete typischerweise auf Debian 12 leben:

* OpenMPI wrappers and launcher: `/usr/bin/mpifort`, `/usr/bin/mpicc`, `/usr/bin/mpirun` or `/usr/bin/mpiexec`. 
* Parallel HDF5: headers are in `/usr/include/hdf5/openmpi`, libs in `/usr/lib/x86_64-linux-gnu/hdf5/openmpi` via `libhdf5-openmpi-dev`. 
* METIS/ParMETIS: headers are in `/usr/include`; libs in `/usr/lib/x86_64-linux-gnu`.

```bash
# _____                              _______________________________
# ____/ TELEMAC Project Definitions /______________________________/
#
[Configurations]
configs: hyinfompideb12
#
# _____          _________________________________________________
# ____/ General /_________________________________________________/
#
[general]
language: 2
modules:  system
version:  9.0
options:  mpi dyn
hash_char: #
# Suffixes
sfx_zip:  .tar.gz
sfx_lib:  .a
sfx_obj:  .o
sfx_exe:
sfx_mod:  .mod
# Validation paths
val_root:      <root>/examples
val_rank:      all
# Compilers (use MPI wrappers on Debian 12/OpenMPI)
cc:      mpicc
cflags:  -fPIC -O3
fc:      mpifort
# Core Fortran flags; TELEMAC expects big-endian unformatted files
fflags:  -cpp -O3 -fPIC -fconvert=big-endian -frecord-marker=4 -DHAVE_MPI
# Build commands
cmd_obj_c: [cc] [cflags] -c <srcName> -o <objName>
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# Splitter and MPI run
par_cmdexec:   <config>/partel < <partel.par> >> <partel.log>
mpi_cmdexec:   mpirun -np <ncsize> <exename>

# ===== Common includes/libs for Debian 12 (OpenMPI / HDF5-openmpi / MED / METIS / MUMPS / ScaLAPACK) =====
# MPI headers (OpenMPI)
inc_mpi:       -I /usr/lib/x86_64-linux-gnu/openmpi/include

# HDF5 parallel (from libhdf5-openmpi-dev)
inc_hdf5:      -I /usr/include/hdf5/openmpi
libs_hdf5:     -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5

# MED-fichier (from SALOME)
inc_med:       -I /home/HyInfo/opt/salome/BINARIES-DB12/medfile/include
libs_med:      -L /home/HyInfo/opt/salome/BINARIES-DB12/medfile/lib -lmedC -lmed -lmedimport

# METIS (from libmetis-dev)
inc_metis:     -I /usr/include
libs_metis:    -L /usr/lib/x86_64-linux-gnu -lmetis

# MUMPS + ScaLAPACK (OpenMPI build)
inc_mumps:     -I /usr/include
libs_mumps:    -L /usr/lib/x86_64-linux-gnu -ldmumps -lmumps_common -lpord -lscalapack-openmpi -lblas -llapack

# Aggregate libraries used by TELEMAC link step
libs_all: [libs_hdf5] [libs_med] [libs_metis] [libs_mumps]

# ===== Build section =====
[hyinfompideb12]
brief: Debian 12 gfortran + OpenMPI + MED/HDF5 + METIS + MUMPS/ScaLAPACK
system: linux
mpi:   openmpi
compiler: gfortran
pyd_fcompiler: gnu95
f2py_name: f2py
# Build tree under <root>=HOMETEL
bin_dir: <root>/builds/hyinfompideb12/bin
lib_dir: <root>/builds/hyinfompideb12/lib
obj_dir: <root>/builds/hyinfompideb12/obj
# Override/extend general flags if needed
options: mpi dyn
cmd_obj:   [fc] [fflags] -c <mods> <incs> <f95name>
cmd_lib:   ar cru <libname> <objs>
cmd_exe:   [fc] [fflags] -o <exename> <objs> <libs>
# Inherit mods_all/incs_all/libs_all from [general]
mods_all:  -I <config>
incs_all:  [inc_mpi] [inc_hdf5] [inc_med] [inc_metis] [inc_mumps]
libs_all:  [libs_hdf5] [libs_med] [libs_metis] [libs_mumps]
# rpath for HDF5-openmpi so executables run without extra env
ldflags_opt:   -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi
ldflags_debug: -Wl,-rpath,/usr/lib/x86_64-linux-gnu/hdf5/openmpi
```
````

````{tab-item} Customization

The following explanations provide guidance on customizing a `cfg` file and reference available templates in TELEMAC's `/configs` folder. These instructions are intended for users who did not use apt-installations of OpenMPI, MUMPS, Metis, and HDF5 (see info box in the {ref}`installation instructions for optionals <tm-system-wide-opts>`.

A typical `systel.*.cfg` file has:
1. An optional `[Configurations]` list enumerating available build sections.
2. A `[general]` section with defaults.
3. One or more build sections like `[debgfopenmpi]` that inherit from `[general]` and override specifics. TELEMAC ships example configs such as `systel.edf.cfg` with these patterns.

**Finding and selecting the right config template:**
* TELEMAC ships example config files in `<root>/configs` (e.g., `systel.edf.cfg`) with parallel/debug sections for GNU/Intel; copy and adapt one for Debian 12. 
* The Python launcher reads the active section from your `systel.*.cfg`; ensure `USETELCFG` points to `[debgfopenmpi]` (or your chosen section). 

A raw OpenMPI/gfortran section in the `cfg` file might look like this for a newly defined configuration called `debgfopenmpi`:

```bash
# _____                          ___________________________________
# ____/ Debian gfortran OpenMPI /__________________________________/
[debgfopenmpi]

par_cmdexec:   <config>/partel < <partel.par> >> <partel.log>
mpi_cmdexec:   /usr/bin/mpirun -wdir <wdir> -np <ncsize> <exename>

cmd_obj:    /usr/bin/mpifort -cpp -c -O3 -DHAVE_MPI -fconvert=big-endian -frecord-marker=4 <mods> <incs> <f95name>
cmd_lib:    ar cru <libname> <objs>
cmd_exe:    /usr/bin/mpifort -fconvert=big-endian -frecord-marker=4 -lpthread -v -lm -o <exename> <objs> <libs>

mods_all:   -I <config>

incs_all:   -I /usr/include/hdf5/openmpi -I /usr/include
libs_all:   -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5 \
            -L /usr/lib/x86_64-linux-gnu -lmetis
```

Der Debian 12 OpenMPI + gfortran Abschnitt verwendet immer noch die Wrapper-Compiler von OpenMPI und enthält keine MPI-Festcodes oder Bibliothekspfade in `libs_all`, es sei denn, Sie haben einen ungewöhnlichen lokalen Build. Die Wrappers injizieren die richtigen Header und Bibliotheken.

**Importierte Schlüssel:**:
 
* `par_cmdexec` tells TELEMAC which command to use to split your mesh for a parallel run. `partel` is the splitter; the redirection `< <partel.par>` feeds it its parameter file and the `>> <partel.log>` collects its output. You keep this line to enable parallel execution; removing it breaks splitting and yields "PARTEL.PAR not found" or similar errors. The official Linux install notes require a partitioner for parallel builds. 
* `mpi_cmdexec` is the runtime launcher. On Debian 12 both `/usr/bin/mpirun` and `/usr/bin/mpiexec` are provided by OpenMPI packages and are equivalent for our purposes. The `<wdir>` placeholder is the working directory; `<ncsize>` is the number of MPI ranks; `<exename>` is the produced solver. 
* `cmd_obj`, `cmd_lib`, `cmd_exe` define the exact compile, archive, and link commands. One can call `mpifort` rather than `gfortran`; the wrapper inserts the correct MPI headers and libs for the OpenMPI you have installed. This avoids brittle hardcoding of `-I/usr/lib/.../openmpi/include` or `-lmpi` with a specific SONAME. Open MPI strongly encourages this practice because the flags vary by build and package.
* `mods_all` appends include paths for module files that TELEMAC generates during compilation; pointing it at `<config>` exposes interfaces between components.
* `incs_all` and `libs_all` are where you add non-MPI optionals you actually enabled such as AED2, MED, METIS, HDF5. Leave pure MPI out of these; let the wrapper handle MPI.

**Important compiler flags:**
* `-cpp` enables preprocessing of Fortran sources so `#include`, `#if`, and `#define` work. TELEMAC sources use conditional compilation; without preprocessing those directives are ignored and compilation may fail. Any modern Fortran compiler with a C-like preprocessor accepts this form.
* `-DNAME` macros such as `-DHAVE_MPI` or `-DHAVE_AED2` define preprocessor symbols that the source checks in `#ifdef` blocks to compile the correct code paths. You only add `-DHAVE_AED2` if AED2 is present. The `-D` mechanism is standard across compilers. 
* `-fconvert=big-endian` and `-frecord-marker=4` control unformatted file byte order and record markers so binaries from different compilers and platforms remain compatible with TELEMAC’s I/O expectations and legacy files. GNU Fortran documents these options; the default record marker is 4 bytes and the `-fconvert` setting affects the representation of unformatted records. Use these flags consistently across compile and run for reproducible unformatted I/O.
* `-O3` is a standard high optimization for release builds. Safe with gfortran and TELEMAC's code base.


**General notes:**
* Use `mpifort` (or `mpif90` symlink) and avoid hard-coding `libmpi.so` or MPI include paths. Open MPI's wrapper compilers inject the correct `-I`/`-L`/`-l` automatically; avoid adding MPI headers/libs to `incs_all`/`libs_all`.
* `mpirun` and `mpiexec` are valid launchers on Debian 12; use whichever you prefer.
* METIS/ParMETIS: use shared libs (`-lmetis`, `-lparmetis`) instead of hard-coding a static `.a` in your home directory, where headers are in `/usr/include`; libs in `/usr/lib/x86_64-linux-gnu`.

**Common pitfalls:**
* Do not remove `par_cmdexec` to "fix" PARTEL errors. Check that `<partel.par>` is produced and that METIS is available if you requested parallel runs. TELEMAC's docs emphasize a partitioner is required for parallelism.
* Do not pin `libs_all` to a literal `.../openmpi/libmpi.so` or to a SONAME. Wrapper compilers exist precisely to avoid this; SONAMEs and link lines differ by OpenMPI build.
* Add optional libraries only when you actually enabled the feature and know the headers and libs exist. Example for AED2 built under your home directory:  
   `incs_all: [..existing..] -I $HOME/telemac/optionals/aed2/include`  
   `libs_all: [..existing..] -L $HOME/telemac/optionals/aed2 -laed2`  
   Leave MPI out of those lists; the wrapper adds MPI. 


If you enable optionals, add only those to `incs_all`/`libs_all` (use specific links for manually installed packages):
* METIS (for PARTEL mesh partitioning)  
   `incs_all: [inc_metis]` with `inc_metis: -I /usr/include`  
   `libs_all: [libs_metis]` with `libs_metis: -L /usr/lib/x86_64-linux-gnu -lmetis` 
* AED2 (if you built it under `~/telemac/optionals/aed2/`)  
   Add `-DHAVE_AED2` to `cmd_obj` and include/lib paths to your AED2 install, for example:  
   `incs_all: -I <config> -I $HOME/telemac/optionals/aed2/include`  
   `libs_all: -L $HOME/telemac/optionals/aed2 -laed2`  
   Leave MPI out of these lists; the wrapper adds MPI.
* Parallel HDF5 and MED (if you use Serafin/SELAFIN MED I/O in your build)  
   Example flags:  
   `incs_all: [..existing..] -I /usr/include/hdf5/openmpi -I /usr/include`  
   `libs_all: [..existing..] -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5 -L /usr/lib/x86_64-linux-gnu -lmedC -lmed`

**Checklist before compiling:**
1. `mpifort -show` prints a `gfortran` link line that already contains MPI libs. If it does not, OpenMPI dev packages are missing.
2. If using parallel HDF5, `h5pfc -show` exists and shows `.../hdf5/openmpi` in its output; otherwise install `libhdf5-openmpi-dev`.
3. The chosen `.cfg` section name is the one exported in `USETELCFG`. The TELEMAC Python scripts will refuse to build if that section is absent. 
````
`````


### Setup Python Source File

** Geschätzte Dauer: 4-20 Minuten.***

The Python source file also lives in TELEMAC's `/configs` folder, where a template called `pysource.template.sh` is available. Specifically, the pysource file is a shell "env" script that one can `source` in every terminal before building or running TELEMAC. It sets four anchors the Python launcher uses: `HOMETEL`, `SYSTELCFG`, `USETELCFG`, and `SOURCEFILE`. TELEMAC's Python scripts look up `SYSTELCFG` and selects the section named in `USETELCFG`. This section guides through either using our `pysource.mint22.sh` / `pysource.debian12.sh` (without AED2), or a customized source file.

`````{tab-set}
````{tab-item} Mint 22 / Ubuntu 24

To facilitate setting up the `pysource.mint22.sh` file on Linux Mint 22 / Ubuntu 24, our template is designed for use with the above-described `systel.mint22.cfg` configuration file, and it is  based on the default-provided `pysource.template.sh`. To use it for compiling TELEMAC:

1. Download [pysource.mint22.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/pysource.mint22.sh) from our GitHub repository, or copy the file contents below into the TELEMAC `/configs` folder, here: `/home/HyInfo/opt/telemac-mascaret/configs` and save as `pysource.mint22.sh`.
2. Open `pysource.mint22.sh` in a text editor (e.g., gedit) and verify installation paths. Note that the file contains the following definition, which makes it almost independent of the definition of your installation path, as long as salome lives in the same directory relative to where you downloaded TELEMAC:
   `_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
3. Verify installation paths of optionals, especially HDF5, MED (especially SALOME), and Mumps.
4. Save `pysource.mint22.sh` and close the text editor.

Our `pysource.mint22.sh` file looks like this:

```bash
#!/usr/bin/env bash
# TELEMAC environment for Linux Mint 22 (Ubuntu 24.04 base) with MPI/HDF5/METIS/MED/MUMPS/ScaLAPACK

# Resolve this script's directory and HOMETEL from it so it works no matter where you cloned TELEMAC
# Expected layout: ~/opt/telemac/{configs, scripts, sources, ...}
_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOMETEL="$(cd "${_THIS_DIR}/.." && pwd)"
export SOURCEFILE="${_THIS_DIR}"

# Configuration file and config name used by telemac.py
# Adjust USETELCFG to match a section present in your systel.mint22.cfg
export SYSTELCFG="${HOMETEL}/configs/systel.mint22.cfg"
export USETELCFG="hyinfompiubu"

# Make TELEMAC Python utilities available
# (Both python3 helpers and legacy unix scripts are often useful)
if [ -d "${HOMETEL}/scripts/python3" ]; then
  export PATH="${HOMETEL}/scripts/python3:${PATH}"
fi
if [ -d "${HOMETEL}/scripts/unix" ]; then
  export PATH="${HOMETEL}/scripts/unix:${PATH}"
fi

# Compilers and MPI (OpenMPI from APT)
export MPI_ROOT="/usr"
export CC="mpicc"
export FC="mpifort"
export MPIRUN="mpirun"

# Library/include roots from Ubuntu 24.04 packages
# OpenMPI libraries
_OMPI_LIB="/usr/lib/x86_64-linux-gnu/openmpi/lib"
_OMPI_INC="/usr/lib/x86_64-linux-gnu/openmpi/include"

# HDF5 (serial headers via libhdf5-dev; libs in the multiarch lib dir)
# If you later install parallel HDF5 (libhdf5-openmpi-dev), set _HDF5_INC="$_OMPI_INC"
_HDF5_INC="/usr/include/hdf5/openmpi/"
_HDF5_LIB="/usr/lib/x86_64-linux-gnu/hdf5/openmpi"

# MED (optional - not actively used in the corrent setup)
_MED_INC="/usr/include/med"
_MED_LIB="/usr/lib/x86_64-linux-gnu"

# METIS
_METIS_INC="/usr/include"
_METIS_LIB="/usr/lib/x86_64-linux-gnu"

# MUMPS (both seq and mpi dev packages provide headers+libs under multiarch dir)
_MUMPS_INC="/usr/include"
_MUMPS_LIB="/usr/lib/x86_64-linux-gnu"

# ScaLAPACK (OpenMPI build)
_SCALAPACK_LIB="/usr/lib/x86_64-linux-gnu"

# Expose common hints some TELEMAC configs look for (non-fatal if unused)
export MPI_INCLUDE="${_OMPI_INC}"
export MPI_LIBDIR="${_OMPI_LIB}"

export HDF5_ROOT="/usr"
export HDF5_INCLUDE_PATH="${_HDF5_INC}"
export HDF5_LIBDIR="${_HDF5_LIB}"

export MED_ROOT="$HOME/opt/salome/BINARIES-UB24.04/medfile/"
export MED_INCLUDE_PATH="$HOME/opt/salome/BINARIES-UB24.04/medfile/include"
export MED_LIBDIR="$HOME/opt/salome/BINARIES-UB24.04/medfile/lib"

export METIS_ROOT="/usr"
export METIS_INCLUDE_PATH="${_METIS_INC}"
export METIS_LIBDIR="${_METIS_LIB}"

export MUMPS_ROOT="/usr"
export MUMPS_INCLUDE_PATH="${_MUMPS_INC}"
export MUMPS_LIBDIR="${_MUMPS_LIB}"

export SCALAPACK_LIBDIR="${_SCALAPACK_LIB}"

# Build and wrapped API locations (created after you compile)
# Keep these early in the path so Python can import the TELEMAC modules and extensions
if [ -d "${HOMETEL}/builds/${USETELCFG}/wrap_api/lib" ]; then
  export PYTHONPATH="${HOMETEL}/builds/${USETELCFG}/wrap_api/lib:${PYTHONPATH}"
fi

# TELEMAC Python helpers
if [ -d "${HOMETEL}/scripts/python3" ]; then
  export PYTHONPATH="${HOMETEL}/scripts/python3:${PYTHONPATH}"
fi

# Runtime search paths
# Put OpenMPI first to avoid picking up non-MPI BLAS/LAPACK accidentally
# The standard multiarch directory is added as a safety net
for _libdir in \
  "${_OMPI_LIB}" \
  "${_MED_LIB}" \
  "${_METIS_LIB}" \
  "${_MUMPS_LIB}" \
  "${_SCALAPACK_LIB}" \
  "/usr/lib/x86_64-linux-gnu"
do
  case ":${LD_LIBRARY_PATH}:" in
    *:"${_libdir}":*) ;;
    *) export LD_LIBRARY_PATH="${_libdir}:${LD_LIBRARY_PATH}";;
  esac
done

# Add include directories to CPATH so builds find headers without extra flags
for _incdir in \
  "${_OMPI_INC}" \
  "${_HDF5_INC}" \
  "${_MED_INC}" \
  "${_METIS_INC}" \
  "${_MUMPS_INC}"
do
  case ":${CPATH}:" in
    *:"${_incdir}":*) ;;
    *) export CPATH="${_incdir}:${CPATH}";;
  esac
done

# Convenience: print a one-line summary so you know which config is active
echo "TELEMAC set: HOMETEL='${HOMETEL}', SYSTELCFG='${SYSTELCFG}', USETELCFG='${USETELCFG}'"

# Make Python unbuffered for clearer build logs
export PYTHONUNBUFFERED="1"
```
````

````{tab-item} Debian 12

To facilitate setting up the `pysource.debian12.sh` file on Debian 12, our template is designed for use with the above-described `systel.debian12.cfg` configuration file, and it is  based on the default-provided `pysource.template.sh`. To use it for compiling TELEMAC:

1. Download [pysource.debian12.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/pysource.debian12.sh) from our GitHub repository, or copy the file contents below into the TELEMAC `/configs` folder, here: `/home/HyInfo/opt/telemac-mascaret/configs` and save as `pysource.debian12.sh`.
2. Open `pysource.debian12.sh` in a text editor (e.g., gedit) and verify installation paths. Note that the file contains the following definition, which makes it almost independent of the definition of your installation path, as long as salome lives in the same directory relative to where you downloaded TELEMAC:
   `_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
3. Verify installation paths of optionals, especially HDF5, MED (especially SALOME), and Mumps.
4. Save `pysource.debian12.sh` and close the text editor.

Our `pysource.debian12.sh` file looks like this:

```bash
#!/usr/bin/env bash
# TELEMAC environment for Debian 12 with MPI/HDF5/MED/METIS/MUMPS/ScaLAPACK
# Assumes all optional dependencies are installed from from apt on Debian 12
# Only SALOME is user-installed

# Resolve script directory and HOMETEL from it
_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOMETEL="$(cd "${_THIS_DIR}/.." && pwd)"
export SOURCEFILE="${_THIS_DIR}"

# Configuration file and config name used by telemac.py
# Adjust USETELCFG to match a section present in configs/systel.debian12.cfg
export SYSTELCFG="${HOMETEL}/configs/systel.debian12.cfg"
export USETELCFG="hyinfompideb12"

# Make TELEMAC Python utilities available
if [ -d "${HOMETEL}/scripts/python3" ]; then
    case ":${PATH}:" in *:"${HOMETEL}/scripts/python3":*) ;; *) export PATH="${HOMETEL}/scripts/python3:${PATH}";; esac
fi
if [ -d "${HOMETEL}/scripts/unix" ]; then
  case ":${PATH}:" in *:"${HOMETEL}/scripts/unix":*) ;; *) export PATH="${HOMETEL}/scripts/unix:${PATH}";; esac
fi

# Detect Debian multiarch lib directory and common include roots
_arch="$(gcc -dumpmachine 2>/dev/null || echo x86_64-linux-gnu)"
_archlib="/usr/lib/${_arch}"

# Helper to pick the first existing directory
_first_dir() {
  for _d in "$@"; do
    [ -d "$_d" ] && { printf '%s' "$_d"; return 0; }
  done
  return 1
}

# MPI. Prefer OpenMPI wrappers if present
_MPI_BIN="$(dirname "$(command -v mpif90 2>/dev/null || command -v mpifort 2>/dev/null || command -v mpicc 2>/dev/null || echo /usr/bin/mpif90)")"
_MPI_INC="$(_first_dir \
  "${_archlib}/openmpi/include" \
  "/usr/include/openmpi" \
  "/usr/include/mpi" \
  "${_archlib}/mpi/include")"
_MPI_LIB="$(_first_dir \
  "${_archlib}/openmpi/lib" \
  "${_archlib}" \
  "/usr/lib")"

# HDF5 parallel. Debian installs OpenMPI-flavored headers in /usr/include/hdf5/openmpi
_HDF5_INC="$(_first_dir \
  "/usr/include/hdf5/openmpi" \
  "/usr/include/hdf5/serial")"
_HDF5_LIB="$(_first_dir \
  "${_archlib}/hdf5/openmpi" \
  "${_archlib}/hdf5/serial" \
  "${_archlib}")"

# MED-fichier
export _MED_ROOT="$HOME/opt/salome/BINARIES-DB12/medfile/"
export _MED_INC="$HOME/opt/salome/BINARIES-DB12/medfile/include"
export _MED_LIB="$HOME/opt/salome/BINARIES-DB12/medfile/lib"

# METIS and ParMETIS
_METIS_INC="$(_first_dir "/usr/include")"
_METIS_LIB="$(_first_dir "${_archlib}")"
_PARMETIS_INC="$(_first_dir "/usr/include")"
_PARMETIS_LIB="$(_first_dir "${_archlib}")"

# MUMPS and ScaLAPACK
_MUMPS_INC="$(_first_dir "/usr/include/mumps" "/usr/include")"
_MUMPS_LIB="$(_first_dir "${_archlib}")"
_SCALAPACK_LIB="$(_first_dir "${_archlib}")"

# Add useful binaries to PATH
for _bindir in \
  "${_MPI_BIN}" \
  "/usr/bin"
do
  case ":${PATH}:" in *:"${_bindir}":*) ;; *) export PATH="${_bindir}:${PATH}";; esac
done

# Library search path
for _libdir in \
  "${_MPI_LIB}" \
  "${_HDF5_LIB}" \
  "${_SCALAPACK_LIB}" \
  "${_MUMPS_LIB}" \
  "${_METIS_LIB}" \
  "${_PARMETIS_LIB}" \
  "${_MED_LIB}"
do
  [ -n "${_libdir}" ] || continue
  case ":${LD_LIBRARY_PATH}:" in *:"${_libdir}":*) ;; *) export LD_LIBRARY_PATH="${_libdir}:${LD_LIBRARY_PATH}";; esac
done

# Include search path for some build helpers that honor CPATH
for _incdir in \
  "${_MPI_INC}" \
  "${_HDF5_INC}" \
  "${_MED_INC}" \
  "${_METIS_INC}" \
  "${_PARMETIS_INC}" \
  "${_MUMPS_INC}"
do
  [ -n "${_incdir}" ] || continue
  case ":${CPATH}:" in *:"${_incdir}":*) ;; *) export CPATH="${_incdir}:${CPATH}";; esac
done

# Convenience: print a one-line summary
echo "TELEMAC set: HOMETEL='${HOMETEL}', SYSTELCFG='${SYSTELCFG}', USETELCFG='${USETELCFG}'"
echo "MPI bin='${_MPI_BIN}', MPI inc='${_MPI_INC}', MPI lib='${_MPI_LIB}'"
echo "HDF5 inc='${_HDF5_INC}', HDF5 lib='${_HDF5_LIB}'"
echo "MED inc='${_MED_INC}', MED lib='${_MED_LIB}'"

# Unbuffered Python for clearer build logs
export PYTHONUNBUFFERED="1"
```

````
````{tab-item} Customization

As a general note, one should expose TELEMAC's Python utilities on `PATH` and `PYTHONPATH` so `telemac2d.py` etc. are found. Prefer OpenMPI wrapper compilers (`mpifort`, `mpicc`) instead of hardcoding MPI headers and libraries. OpenMPI explicitly recommends this; the wrappers inject the right `-I`/`-L`/`-l` for your installation. For optional features like TelApy, TELEMAC builds a small "wrap_api" tree in the build directory; adding that to `PYTHONPATH` and `LD_LIBRARY_PATH` is the correct way to make the Python API importable. Use the following as a starting point; replace `USERNAME` and adjust `SYSTELCFG` and `USETELCFG`:

```bash
#!/usr/bin/env bash
# TELEMAC environment for Debian 12 + OpenMPI

# 1) Core paths
export HOMETEL="/home/USERNAME/telemac-mascaret"
export SYSTELCFG="${HOMETEL}/configs/systel.cis-debian.cfg"
export USETELCFG="debgfopenmpi"
export SOURCEFILE="${HOMETEL}/configs/pysource.gfortranHPC.sh"

# 2) Make TELEMAC tools available
case ":$PATH:" in *:"${HOMETEL}/scripts/python3":*) ;; *) export PATH="${HOMETEL}/scripts/python3:${PATH}";; esac
case ":$PATH:" in *:"${HOMETEL}/scripts/unix":*)   ;; *) export PATH="${HOMETEL}/scripts/unix:${PATH}";; esac
case ":$PYTHONPATH:" in *:"${HOMETEL}/scripts/python3":*) ;; *) export PYTHONPATH="${HOMETEL}/scripts/python3:${PYTHONPATH}";; esac

# 3) Unbuffered Python for clearer build logs
export PYTHONUNBUFFERED="1"

# 4) TelApy (Python API) - populated after a build; harmless if absent
_wrap_api_lib="${HOMETEL}/builds/${USETELCFG}/wrap_api/lib"
[ -d "$_wrap_api_lib" ] && export LD_LIBRARY_PATH="${_wrap_api_lib}:${LD_LIBRARY_PATH}"
[ -d "$_wrap_api_lib" ] && export PYTHONPATH="${_wrap_api_lib}:${PYTHONPATH}"

# 5) MPI - use OpenMPI wrappers; do NOT point to MPICH
# on Debian 12, mpifort/mpirun live in /usr/bin via openmpi-bin/libopenmpi-dev
command -v mpifort >/dev/null 2>&1 || echo "Warning: mpifort not found; install openmpi-bin libopenmpi-dev"
command -v mpirun  >/dev/null 2>&1 || echo "Warning: mpirun not found; install openmpi-bin"

# 6) Optional libs installed from Debian packages need no path tweaks - otherwise,
# if you compiled optionals under $HOMETEL/optionals (e.g., AED2), add them explicitly:
# export LD_LIBRARY_PATH="${HOMETEL}/optionals/aed2:${LD_LIBRARY_PATH}"
# export PYTHONPATH="${HOMETEL}/optionals/aed2:${PYTHONPATH}"

echo "TELEMAC env set: HOMETEL=${HOMETEL}, USETELCFG=${USETELCFG}"
```

**Notes:**
* `SYSTELCFG` points at your `.cfg` file; `USETELCFG` must match the section header you intend to use, for example `[debgfopenmpi]`. This is how TELEMAC's Python launcher discovers the "build recipe".
* `PATH` includes both `scripts/python3` and `scripts/unix` so you can run `telemac.py`, `compile.py`, `runcode.py`, and shell helpers directly. 
* `mpifort` and `mpirun` are the correct OpenMPI entry points on Debian 12. `mpif90` exists but is a legacy alias; OpenMPI recommends `mpifort`. `mpirun` and `mpiexec` are synonyms and ship in `/usr/bin`.
* No `MPIHOME` and no `LD_LIBRARY_PATH` hacking for OpenMPI. Wrapper compilers remove the need to export OpenMPI include/lib paths; exporting `LD_LIBRARY_PATH` to point at OpenMPI libraries is both unnecessary and fragile on Debian
* `wrap_api/lib` on both `PYTHONPATH` and `LD_LIBRARY_PATH` is the correct way to make TelApy importable after you build it. This matches where TELEMAC emits the API artifacts.
* Do not set `MPIHOME=/usr/bin/mpifort.mpich` if you are building with OpenMPI. That value points to an MPICH binary and will cause mismatched headers and libraries at compile or run time. Use OpenMPI consistently or switch the whole stack to MPICH. OpenMPI’s own docs emphasize wrapper consistency.
* Do not add `LD_LIBRARY_PATH=$PATH/lib` or point it to `lib/x86_64-linux-gnu/openmpi`. `$PATH` is not a library directory, and hardcoding OpenMPI’s library dir in the env file is unnecessary when you compile and link with `mpifort`.
* Do not hard-code `libmpi.so` anywhere in `pysource` or in your `.cfg` if you are already using wrapper compilers. Let `mpifort` drive the link line. 

If you use distro packages, you typically do not need to set any paths in `pysource`:
* OpenMPI tools: `/usr/bin/mpifort`, `/usr/bin/mpicc`, `/usr/bin/mpirun` or `/usr/bin/mpiexec`.
* Parallel HDF5 (if enabled in your cfg): headers under `/usr/include/hdf5/openmpi`, libs under `/usr/lib/x86_64-linux-gnu/hdf5/openmpi` via `libhdf5-openmpi-dev`.
* METIS from Debian: link as `-lmetis` from `libmetis-dev`; headers in `/usr/include`, libs in `/usr/lib/x86_64-linux-gnu`. Prefer this over a hand-built `libmetis.a` under `~/telemac/optionals`.
````
`````

(tm-compil)=
### Compile

** Geschätzte Dauer: 20-30 Minuten (Verknüpfung dauert Zeit).***

The compiler is invoked by TELEMAC's Python tools using the shell environment set by your `pysource` script (`pysource.mint22.sh` or `pysource.debian12.sh`). That script tells TELEMAC where helper programs and libraries live and which configuration to use. With it in place, compiling becomes straightforward from Terminal. First, source the appropriate `pysource` file and then verify the setup by running `config.py`:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs    # adjust this path to your install
source pysource.mint22.sh                       # or: source pysource.debian12.sh
config.py
```

Sourcing the our `pysource.mint22.sh` or `pysource.debian12.sh` scripts should echo the TELEMAC paths and the configuration name. Running `config.py` should display the ASCII banner and finish with `My work is done`. If not, read the error output carefully; typical causes are typos in paths or filenames, or mistakes inside `pysource.x.sh` or your `systel.*.cfg`.


```{admonition} Quick health checks after sourcing
:class: tip

* `mpifort -show` should print a `gfortran` command line with MPI `-I` and `-L` flags injected. This verifies wrapper compilers are in place.
* If you enabled parallel HDF5 in your `.cfg`, `h5pfc -show` should succeed and display `.../hdf5/openmpi` in its flags. If it is missing, install `libhdf5-openmpi-dev`.
* Running `telemac.py` or `compile.py` without a full path should work because `scripts/python3` and `scripts/unix` are on `PATH`. The TELEMAC Linux install notes follow this approach.
```

After `config.py` completes successfully, compile TELEMAC. Use the `--clean` flag to remove any artifacts from prior builds and avoid conflicts:

```bash
compile_telemac.py --clean
```

Der Build wird eine Weile laufen und sollte mit der Nachricht `My work is done` beenden. Wenn es mit Fehlern aufhört, scrollen Sie bis zum ersten Fehler und fixieren Sie das gemeldete Problem, bevor Sie den Befehl erneut ausführen.

```{admonition} How to troubleshoot errors in the compiling process
:class: attention

Wenn die Zusammenstellung ausfällt, lesen Sie den Rückblick sorgfältig und identifizieren Sie die genaue Komponente, die brach. Überprüfen Sie die Setup-Schritte für diese Komponente und überprüfen Sie Pfade, Bibliotheksnamen, Umgebungsvariablen und Datei-Editionen gegen diese Anleitung. **Erfinden Sie das Rad nicht neu:* Die meisten Fehler kommen aus kleinen Typos oder falsch abgestimmten Versionen in Dateien, die Sie selbst erstellt haben. Fehlerbehebungen können frustrierend sein, also Ihre eigenen Annahmen herausfordern, den ersten Fehler im Log beheben und dann aus einem sauberen Zustand wieder aufbauen.
```

(Testrun)=
### Test TELEMAC

** Geschätzte Dauer: 5-10 Minuten.***


Nach dem Schließen des Terminals oder auf einem neuen Systemstart werden Sie die TELEMAC-Umgebung neu laden, bevor Sie es ausführen:

```bash
cd ~/opt/telemac-mascaret/configs    # adjust if you installed elsewhere
source pysource.mint22.sh            # or: source pysource.debian12.sh
```

Run a predefined case from the `examples` folder:

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
```

```{admonition} Examples not working?
:class: error, dropdown

Do not panic. If `config.py` succeeded and the build ended with "My work is done", your installation is usually fine. Most example failures come from environment issues or missing large files. Ensure you have sourced the correct `pysource.*.sh`, installed all Git requirements **including Git LFS, checked out the right version,** and pulled the full repository. If needed, re-clone with Git LFS enabled and recompile TELEMAC, starting from the {ref}`git section <tm-git-requirements>`.
```

Um die Parallelität zu überprüfen, installieren Sie *htop*, um die CPU-Nutzung zu visualisieren:

```bash
sudo apt update
sudo apt install htop
```

Starten Sie den CPU-Monitor:

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

```{admonition} Cannot find <<PARTEL.PAR>>?
:class: error, dropdown
If you see `Cannot find << PARTEL.PAR >>` or `TypeError: can only concatenate str (not ...) to str`, ensure `par_cmdexec` is removed from your configuration file.
```

Während die Berechnung läuft, sehen Sie die Gesamt-CPU-Nutzung. Wenn mehrere Kerne eine anhaltende Aktivität in unterschiedlichen Prozenten zeigen, funktioniert der Parallellauf.

TELEMAC should start, run the example, and finish with `My work is done`. To gauge efficiency, vary `--ncsize`. For instance, on a contemporary laptop the `donau` case often runs in approx. 1 minute with `--ncsize=4` and approx. 2-3 minutes with `--ncsize=2`; exact timings depend on hardware, mesh size, and I/O. **Scaling is not linear** due to domain-partition overhead, memory bandwidth limits, and hyperthreading, so launching several smaller jobs on fewer cores can be more efficient than one job on many cores.

````{admonition} Troubleshoot 'No such file or directory'
:class: attention, dropdown
Wenn Sie die Terminal-Session unterbrochen haben und `No such file or directory` sehen, laden Sie die TELEMAC-Umgebung erneut ein, bevor Sie Beispiele wiederholen:

```bash
cd ~/opt/telemac-mascaret/configs
source pysource.mint22.sh      # or: source pysource.debian12.sh
config.py
```

Then return to the `examples` folder and run the case again.
````

### TELEMAC Dokumentation generieren

TELEMAC enthält viele Anwendungsbeispiele unter `/telemac-mascaret/examples/` und Sie können die Benutzer- und Referenzhandbücher lokal erstellen. Zuerst die TELEMAC-Umgebung laden:

```bash
source ~/opt/telemac-mascaret/configs/pysource.mint22.sh
```

To generate the user manual (this can take a while and requires latex, that is, `texlive` on Debian/Ubuntu):

```bash
doc_telemac.py
```

Um das Referenzhandbuch zu erzeugen:

```bash
doc_telemac.py --reference
```

Um Dokumentations- und Validierungsberichte für alle Beispielfälle zu erstellen:

```bash
validate_telemac.py
```

```{note}
`validate_telemac.py` iterates through many examples. Some may fail if optional modules are not installed (e.g., HERMES) or if an example is outdated. Building PDFs typically requires a LaTeX toolchain (for example, `texlive` on Debian/Ubuntu); install it if the documentation step reports missing LaTeX executables.
```


(install-telemac-utilities)=
(Vor- und Nachbearbeitung)

```{admonition} More Pre- and Post-processing Software
:class: note

More software for dealing with TELEMAC pre- and post-processing is available in the form of {ref}`SALOME <salome-install>` and ParaView.
```

(qgis-telemac)=
### QGIS und das Q4TS Plugin (Linux und Windows)

** Geschätzte Dauer: 5-10 Minuten (abhängig von Verbindungsgeschwindigkeit).****

QGIS is a powerful tool for viewing, creating, and editing geospatial data and is useful for both pre- and post-processing. Installation guidance appears in the {ref}`qgis-install` instructions and the {ref}`QGIS tutorial <qgis-tutorial>` in this eBook. The **Q4TS** plugin supports preparing and post-processing files for TELEMAC and can be linked with {ref}`SALOME <salome-install>` to launch TELEMAC from a GUI.

To install Q4TS, follow the developers’ instructions at [https://gitlab.pam-retd.fr/otm/q4ts](https://gitlab.pam-retd.fr/otm/q4ts):

* In QGIS öffnen Sie den **Plugin Manager** (Plugins > Plugins verwalten und installieren...).
* Go to **Einstellungen****Add...*, setze die URL an `https://otm.gitlab-pages.pam-retd.fr/q4ts/plugins.xml`, wähle einen **Name** (z.B. `q4ts`) und lasse die anderen Felder unverändert. Klicken Sie auf **OK**.
* Klicken Sie auf **Reload aller Repositories**.
* In der Registerkarte **All** suchen Sie nach `Q4TS` und installieren Sie das Plugin.

```{admonition} Plugin not found?
:class: warning, dropdown

Q4TS requires QGIS 3.26 or newer. If your QGIS is older, the Plugin Manager will not list it. The reliable fix is to upgrade QGIS. As a temporary workaround, you can download the ZIP from [https://otm.gitlab-pages.pam-retd.fr/q4ts/q4ts.0.7.0.zip](https://otm.gitlab-pages.pam-retd.fr/q4ts/q4ts.0.7.0.zip) and use **Install from ZIP**, but upgrading QGIS is highly recommended.
```

After installation, Q4TS adds tools in the QGIS Processing Toolbox for MED -- SLF conversion, mesh refinement, boundary creation, friction table editing, and more. Basic utility for post-processing is described in the `steady-flow simulation tutorial <tm-use-q4ts>` with Telemac2d.

To get started with the Q4TS plugin, see {numref}`Fig. %s <q4ts-ubuntu>` (Windows: {numref}`Fig. %s <q4ts-windows>`) and consult the developers' user manual on GitLab: [https://gitlab.pam-retd.fr/otm/q4ts/](https://gitlab.pam-retd.fr/otm/q4ts/-/blob/develop/docs/user_manual/user_manual.md).

`````{tab-set}
````{tab-item} Linux (Ubuntu)
```{figure} ../img/telemac/conf-mint22.jpg
:alt: configure Q4TS on Ubuntu Linux
:name: q4ts-ubuntu

Die Konfiguration des Q4TS auf Ubuntu Linux. Um diese Pfade in QGIS einzustellen, gehen Sie zu **Einstellungen** (Top-Menü) > * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```
````
````{tab-item} Windows
```{figure} https://gitlab.pam-retd.fr/otm/q4ts/-/raw/develop/docs/images/conf_windows.png
:alt: configure Q4TS on Windows
:name: q4ts-windows

Die Konfiguration des Q4TS unter Windows (Links an https://gitlab.pam-retd.fr). Um diese Pfade in QGIS einzustellen, gehen Sie zu **Einstellungen** (Top-Menü) > * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```
````
`````

```{admonition} Other (stale) plugins
:class: note, dropdown

Ältere, teilweise nicht arbeitende TELEMAC-bezogene Plugins für QGIS beinhalten:

* [Telemac Tools](https://plugins.qgis.org/plugins/telemac_tools/), an experimental mesh generator for `*.slf` files developed by *Artelia*. In QGIS, enable **experimental plugins** in the Plugin Manager **Settings** before searching.
* {ref}`BASEmesh <get-basemesh>`, which can create an {term}`SMS 2dm` mesh that you can convert to a SELAFIN geometry for TELEMAC (see the {ref}`QGIS pre-processing tutorial for TELEMAC <tm-qgis-prepro>`).
* *PostTelemac*, which visualizes `*.slf` and related result formats (for example, `*.res`) over time.
* *DEMto3D*, which exports *STL* geometry suitable for use in *SALOME* and for creating 3D meshes.

Beachten Sie, dass *DEMto3D* unter dem **Raster**-Menü erscheint: **DEMto3D***** **Digitales Oberflächenmodell (DOM) 3D-Druck***. Diese Plugins können mit aktuellen QGIS-Versionen veraltet oder unvereinbar sein; bevorzugen Q4TS für aktiv gepflegte TELEMAC-Workflows, wenn möglich.
```

(artelia-mesh)=
### Artelia Mesh Tools

Artelia provides a Python-based analysis toolkit on GitHub: [https://github.com/Artelia/Mesh_tools](https://github.com/Artelia/Mesh_tools). Hydro-informatics.com has not yet tested Mesh Tools, but it appears promising for inspecting and analyzing existing meshes rather than generating new ones; see the related discussion in the [TELEMAC forum](https://www.opentelemac.org/index.php/kunena/qgis-for-otm/14662-meshtools).

Nach der Installation des Plugins über den QGIS Plugin Manager, zugreifen Sie es aus **Mesh** > **Mesh Tools*.


(Bluekenue)=
### BlueKenue (Windows oder Linux+Wine)

** Geschätzte Dauer: 10 Minuten.**

[BlueKenue](https://nrc.canada.ca/en/research-development/products-services/software-applications/blue-kenuetm-software-tool-hydraulic-modellers)<sup>TM</sup> is a Windows-based pre- and post-processing tool from the [National Research Council Canada](https://nrc.canada.ca/en), which is designed for TELEMAC. It offers functionality similar to [Fudaa](http://www.opentelemac.org/index.php/latest-news-development-and-distribution/240-fudaa-mascaret-3-6) and includes a capable mesh generator, which is the main reason to install BlueKenue<sup>TM</sup>. Download the installer from the developer site: [https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (credentials are noted in the [Telemac Forum](http://www.opentelemac.org/index.php/assistance/forum5/blue-kenue)). Then choose the install method for your platform:

1. On Windows: run the BlueKenue `.msi` installer directly.
2. On Linux: use [Wine amd64](https://wiki.debian.org/Wine) through {ref}`PlayOnLinux <play-on-linux>` to install BlueKenue<sup>TM</sup>. For Ubuntu/Debian systems, see the {ref}`PlayOnLinux <play-on-linux>` section in this eBook. Installing with plain Wine only is discouraged due to common compatibility issues.

Typisch BlueKenue<sup>@</sup> ausführbare Standorte sind:

* 32-bit: `"C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"`
* 64-bit: `"C:\\Program Files\\CHC\\BlueKenue\\BlueKenue.exe"`

For additional cross-platform guidance, see the [CHyMS FAQ](https://chyms.nrc.gc.ca/docs/FAQ.html), especially the section on running Blue Kenue on [other operating systems](https://chyms.nrc.gc.ca/docs/FAQ.html#troubleshooting-how-run-on-another-os).


(fudaa)=
### Fudaa-PrePro (Linux und Windows)

*** Geschätzte Dauer: 5-15 Minuten (obere Zeitgrenze, falls Java installiert werden muss).***

Fudaa-PrePro ist ein Java-basiertes grafisches Frontend für das TELEMAC-System, das Ihnen hilft, Modelle durch die Definition von Maschen, Grenz- und Ausgangsbedingungen und Lenkung (`.cas`)-Dateien zu erstellen, und es kann auch Simulationen starten und die grundlegende Nachbearbeitung unterstützen. Es wird durch das Fudaa-Projekt gepflegt und mit Dokumentationen und Downloads auf ihrer Website verteilt, und es wird von den TELEMAC-Entwicklern als benutzerfreundlicher Vorprozessor zur Berechnung von Berechnungen referiert. Bereiten Sie sich mit der Vor- und Nachbearbeitungssoftware Fudaa-PrePro vor:

* Install *Java*:
    + On Linux: `sudo apt install default-jdk`  (the JRE alone works for running; the JDK is safe for both running and tools)
    + On Windows: get Java from [java.com](https://java.com/)
* Download the latest version from the [Fudaa-PrePro repository](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/237993985/Fudaa-Prepro+Downloads).
* Unzip the downloaded file and proceed depending on your platform (see below).
* `cd` to the directory where you unzipped the Fudaa-PrePro program files.
* Start Fudaa-PrePro from Terminal or Command Prompt:
    + On *Linux*: run `sh supervisor.sh`
    + On *Windows*: run `supervisor.bat`

Wenn Sie einen Fehler wie:

```bash
Error: Could not find or load main class org.fudaa.fudaa.tr.TrSupervisor
```
edit `supervisor.sh` and replace `$PWD Fudaa` with `$(pwd)/Fudaa` so the classpath resolves correctly. You can also adjust the default RAM setting in `supervisor.sh` (or `supervisor.bat`). Fudaa-PrePro often ships with `-Xmx6144m` (≈6 GB); increase it for very large meshes (millions of nodes) or decrease it on low-RAM systems. Set `-Xmx` to a sensible multiple of 512 MB. For example, to use 2 GB and fix the classpath:

```bash
#!/bin/bash
cd "$(dirname "$0")"
java -Xmx2048m -Xms512m -cp "$(pwd)/Fudaa-Prepro-1.4.2-SNAPSHOT.jar" org.fudaa.fudaa.tr.TrSupervisor "$@"
```
