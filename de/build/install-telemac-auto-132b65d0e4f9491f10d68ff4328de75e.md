---
description: Schritt-für-Schritt-Tutorial für die automatische Installation von offenen TELEMAC-MASCARET auf Debian Linux und Ubuntu-basierten Systemen mit Installationsskripten.
---

(telemac-autoinstall)=
# TELEMAC (Auto-Installation)


## Vorwort

This tutorial walks you through installing [open TELEMAC-MASCARET](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/) and Ubuntu-based systems with **automatic installer** scripts. **Plan for roughly 1-2 hours and a stable internet connection; the downloads exceed 1.4 GB.** For detailed installation instructions, go to the {ref}`detailed TELEMAC installation page <telemac-install>`.


(telemac-autoinstall-requirements)=
## Anforderungen

### Systempakete

`````{tab-set}
````{tab-item} Debian 12

Unter Debian 12 bitten Sie Ihren Systemadministrator, die folgenden Pakete über aptitude zu sudo-installieren:

```bash
sudo apt update

sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-dev libmumps-seq-dev libscalapack-openmpi-dev libmedc-dev libmed-dev libmedimport-dev libmed-tools python3-pytest-cython python3-sphinx python3-alabaster python3-cftime libcminpack1 python3-docutils python3-h5py python3-imagesize clang python3-netcdf4 python3-nlopt python3-nose python3-numpydoc python3-patsy python3-psutil liblzf1 python3-stemmer python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev liblapacke-dev libxml2-dev llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff-dev libgeotiff-dev libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```

````

````{tab-item} Ubuntu 24 / Mint 22
Bitten Sie unter Ubuntu 24 (oder Mint 22) Ihren Systemadministrator, die folgenden Pakete über aptitude zu installieren:

```bash
sudo apt update
sudo apt install -y --no-install-recommends  python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1 libegl1 libxrandr2 libxss1 libxcursor1 libxcomposite1 alsa-base libxi6 libxtst6  python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins  libmedc11t64 libmedc-dev libmed-tools libmed11 libmed-dev libmedimport0v5 libmedimport-dev  libopenmpi-dev openmpi-bin libhdf5-dev libhdf5-openmpi-dev hdf5-tools libmetis-dev libmumps-seq-dev libmumps-dev  libscalapack-openmpi-dev python3-pytest-cython python3-sphinx python3-alabaster python3-cftime  libcminpack1 python3-docutils libfreeimage3 python3-h5py python3-imagesize liblapacke  clang python3-netcdf4 libnlopt0 libnlopt-cxx0 python3-nlopt python3-nose python3-numpydoc  python3-patsy python3-psutil libtbb12 libxml++2.6-2v5 liblzf1 python3-stemmer  python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels  python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev  doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev libxml2-dev  llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev  libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev  libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev  libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff5-dev libgeotiff-dev  libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev  libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```
````
`````

Beachten Sie, dass das automatische Installationsskript möglicherweise zusätzliche erforderliche Pakete erkennt.

### Einrichtung von Anlagenpfaden

TELEMAC wird aus seinem GitLab-Repository in ein von Ihnen gewähltes Verzeichnis heruntergeladen (git-cloned) und im Folgenden als **ROOT**-Verzeichnis bezeichnet. Außerdem wird SALOME heruntergeladen und in diesem ROOT-Verzeichnis installiert. Wählen Sie eines der folgenden Setups aus:

* Einzelner Benutzer ohne Admin-Rechte: `ROOT=/home/<USERNAME>/opt` (dh `ROOT=$HOME/opt`) (XDG-konforme Alternative: `ROOT=$HOME/.local`)
* Gemeinsame Nutzung ohne root: nur wenn bereits ein gruppenbeschreibbarer Standort existiert, z. B. eine NFS-Freigabe wie `ROOT=/srv/shared/telemac`
* Systemweit (Administrator erforderlich) auf Debian-basierten Systemen: bevorzugt `ROOT=/usr/local` (Binärdateien in `/usr/local/bin`, Bibliotheken in `/usr/local/lib`); `ROOT=/opt` ist auch für einen in sich geschlossenen Baum akzeptabel


### SALOME

Die Auswahl der richtigen Version von SALOME kann nicht automatisiert werden, also suchen und laden Sie die neueste Version von SALOME herunter und speichern Sie sie im ROOT-Verzeichnis, in dem Sie Telemac installieren möchten.

```{admonition} How TELEMAC binds to MED files and SALOME
:class: important

TELEMAC liest und schreibt `.med` meshes durch seine HERMES-Schicht, die gegen die ** System-MED-Bibliotheken** (die `libmedc-dev` / `libmed-dev` / `libmedimport-dev`-Pakete) kompiliert wird - **nicht** gegen die MED-Bibliotheken, die in SALOME gebündelt sind. SALOME liefert sein eigenes MED, das mit einem anderen ABI (64-Bit `med_int` und einem anderen HDF5-Build) erstellt wurde, und verbindet oder lädt es zusammen mit TELEMAC auslöst `size of symbol 'med_' changed` Link-Warnungen und den Laufzeitfehler `HERMES_WRONG_MED_FORMAT_ERR`.

SALOME is therefore used only for the GUI and mesh tools. The single piece the installer borrows from SALOME is the Fortran header `med_parameter.hf`, which Debian/Ubuntu omit from `libmed-dev` (a packaging gap); it contains constants only and is ABI-neutral. For this reason, **install SALOME (i.e., provide `--salome-tar`) before running the installer if you want MED support** - otherwise the installer cannot find `med_parameter.hf` and MED I/O is disabled in the generated config. The generated `pysource.*.sh` additionally removes any SALOME MED/HDF5 directories from `LD_LIBRARY_PATH` at runtime, so the system MED is always the one that gets loaded.
```

1. Bestätigen Sie Ihre Linux Version:
  * Debian: cat /etc/os-release
  * Minze: `lsb_release -a`
  * Ubuntu: `inxi -Sx` (funktioniert auch auf Mint)

2. Laden Sie den SALOME Build herunter
  * Gehen Sie zum [offiziellen SALOME-Downloadformular](https://www.salome-platform.org/?page_id=2430)]
  * Wählen Sie die neueste Version mit dem Debian/Ubuntu-Build (die mit der Ubuntu/Mint-Basis übereinstimmt); oder wählen Sie das weniger häufig aktualisierte "Linux Universal"

3. Verify the checksum: from SALOME's md5 page, fetch the matching `.md5` file for your archive and verify locally
  * Beispiel für den 9.15 Tarball: im Download-Verzeichnis des Tarballs laufen `md5sum SALOME-9.15.0.tar.gz` (Terminal)
  * Gehen Sie zu SALOMEs [md5 page](https://www.salome-platform.org/?page_id=2818)], wählen Sie die entsprechende md5-Datei aus und überprüfen Sie, ob ihr Inhalt genau der Antwort des Terminals entspricht.
  * ** Überspringen Sie das nicht! **

### Holen Sie sich die Installer-Scripts

* Debian 12-Benutzer herunterladen:
  * [telemac debian12 installer.sh](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/debian12/telemac_debian12_installer.sh) und speichern Sie es im ROOT-Verzeichnis.
  * [systel.debian12.cfg](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/debian12/systel.debian12.cfg) und speichern Sie es im ROOT-Verzeichnis.
  * [pysource.debian12.sh](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/debian12/pysource.debian12.sh)] und speichern Sie es im ROOT-Verzeichnis.
* Mint 22 / Ubuntu 24 Benutzer herunterladen:
  * [telemac ubuntu24 installer.sh](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/ubuntu24-mint22/telemac_ubuntu24_installer.sh) und speichern Sie es im ROOT-Verzeichnis.
  * [systel.mint22.cfg](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/ubuntu24-mint22/systel.mint22.cfg)] und speichern Sie es im ROOT-Verzeichnis.
  * [pysource.mint22.sh](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/ubuntu24-mint22/pysource.mint22.sh)] und speichern Sie es im ROOT-Verzeichnis.

Stellen Sie sicher, dass sich alle Dateien im selben (ROOT-Installations-) Verzeichnis auf Ihrem Computer befinden.

## Laufinstallateure

### Einbaumuster
Note that you might need **admin (sudo) rights** for installing additional system packages and that the installation can take a while because the script downloads Telemac. The script installs by default Telemac v9.1.1. To install another version, use the `--tag "TAG"` option when running the scripts; latest tags can be found at [https://gitlab.pam-retd.fr/otm/telemac-mascaret.git](https://gitlab.pam-retd.fr/otm/telemac-mascaret.git). Both installers also install the system MED packages and compile TELEMAC automatically at the end of the run (unless you pass `--skip-compile`).

Um das Installationsprogramm auszuführen, tippen Sie auf (ersetzen Sie `ROOT` durch Ihr ROOT-Verzeichnis und `SALOME-x.xx.xSRC.tar.gz` durch den Namen des SALOME-Tarballs, den Sie heruntergeladen haben):

`````{tab-set}
````{tab-item} Debian 12
```bash
cd ROOT
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

The installer already compiled TELEMAC at the end of its run (unless you passed `--skip-compile`). To load the environment - and optionally rebuild from scratch - run:
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean   # only needed for a fresh rebuild
```

````

````{tab-item} Ubuntu 24 / Mint 22
```bash
cd ROOT
chmod +x telemac_ubuntu24_installer.sh
./telemac_ubuntu24_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

Nach Abschluss der Installation kann die Telemac-Umgebung wie folgt geladen werden:
```bash
cd ROOT/telemac-mascaret/configs/
source pysource.mint22.sh
```
````
`````

Die Installationsskripte klonen das `telemac-mascaret` GitLab-Repo (mit dem zugewiesenen Tag) und einen `salome`-Ordner, in dem der SALOME-Tarball ausgepackt wird. Wenn bei SALOME Fehler auftreten, schauen Sie sich {ref}`detailed SALOME installation instructions <salome-install>` im Abschnitt "manuelle" Installation von Telemac an.

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


### Installationsbeispiel

Angenommen, Sie arbeiten an Debian 12, entsprechend haben Sie `SALOME-9.15.0-native-DB12-SRC.tar.gz` heruntergeladen, das ROOT-Verzeichnis als `/home/HyInfo/opt/` definiert und `telemac_debian12_installer.sh` heruntergeladen. Somit kann die Installation mit diesen Befehlen gestartet werden:

```bash
cd /home/HyInfo/opt
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "/home/HyInfo/opt" --salome-tar "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz" --salome-md5 "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz.md5"
```

Aktivieren Sie nun die Telemac-Umgebung und kompilieren Sie wie folgt:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

### Installationsbeispiel mit einer anderen Version

Angenommen, Sie arbeiten an Debian 12, entsprechend haben Sie `SALOME-9.15.0-native-DB12-SRC.tar.gz` heruntergeladen, das ROOT-Verzeichnis als `/home/HyInfo/opt/` definiert, `telemac_debian12_installer.sh` heruntergeladen und möchten ** Telemac v9.5.0** installieren (wenn das unter https://gitlab.pam-retd.fr/otm/telemac-mascaret.git existiert). Diese Installation kann mit folgenden Befehlen gestartet werden:

```bash
cd /home/HyInfo/opt
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "/home/HyInfo/opt" --tag "v9.5.0" --salome-tar "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz" --salome-md5 "/home/HyInfo/opt/SALOME-9.15.0-native-DB12-SRC.tar.gz.md5"
```

Aktivieren Sie nun die Telemac-Umgebung und kompilieren Sie Telemac wie folgt:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs/
source pysource.debian12.sh
compile_telemac.py --clean
```

### Re-Install

Um eine bestehende Installation zu reparieren / neu zu installieren:

1. Navigieren Sie zu Ihrem TELEMAC-Verzeichnis:

  ```bash
  cd ~/opt/telemac-mascaret
  ```

2. Re-run the installer with `--skip-apt` to regenerate config files (assumes you are using a newer version of the installer script)
  
  ```bash
  chmod +x ./telemac_debian12_installer.sh
  ./telemac_debian12_installer.sh --skip-apt --root "/ROOTDIR" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
  ```

3. Regenerieren durch erneutes Ausführen von config and compile:

  ```bash
  source configs/pysource.debian12.sh
  compile_telemac.py --clean
  ```


(testrun-autoinstaller)=
## Test TELEMAC

***Geschätzte Dauer: 5-10 Minuten.***

Laden Sie die TELEMAC-Umgebung:

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

Um die Parallelität zu überprüfen, installieren Sie *htop*, um die CPU-Auslastung zu visualisieren:

```bash
sudo apt update
sudo apt install htop
```

Starten Sie den CPU-Monitor:

```bash
htop
```

Führen Sie in einem neuen Terminal-Tab ein TELEMAC-Beispiel mit dem `--ncsize=N`-Flag aus, wobei `N` die Anzahl der zu verwendenden logischen CPUs ist (stellen Sie sicher, dass mindestens `N` verfügbar sind):

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


### TELEMAC erzeugen Dokumentation

TELEMAC includes many application examples under `/telemac-mascaret/examples/`, and you can build the user and reference manuals locally. First, load the TELEMAC environment:

```bash
source ~/opt/telemac-mascaret/configs/pysource.mint22.sh
```

To generate the user manual (this can take a while and requires latex, that is, `texlive` on Debian/Ubuntu):

```bash
doc_telemac.py
```

Zur Erstellung des Referenzhandbuchs:

```bash
doc_telemac.py --reference
```

Erstellen von Dokumentations- und Validierungsberichten für alle Beispielfälle:

```bash
validate_telemac.py
```

```{note}
`validate_telemac.py` iteriert durch viele Beispiele. Einige können fehlschlagen, wenn optionale Module nicht installiert sind (z. B. HERMES) oder wenn ein Beispiel veraltet ist. Das Erstellen von PDFs erfordert in der Regel eine LaTeX-Toolchain (z. B. `texlive` auf Debian/Ubuntu); installieren Sie sie, wenn der Dokumentationsschritt fehlende LaTeX-Ausführungsdateien meldet.
```



## Versorgungsunternehmen (Vor- und Nachbearbeitung)

To install pre- and post-processing utilities, refer to the instructions in the {ref}`manual installation section <install-telemac-utilities>`, such as BlueKenue or the Q4TS plugin in QGIS. Note that for the Q4TS plugin, your SALOME executable path is `/ROOT/salome/salome`, and your Telemac *environnement* script is `/ROOT/telemac-mascaret/configs/pysource.debian12.sh` (or `/ROOT/telemac-mascaret/configs/pysource.mint22.sh` if you installed on Ubuntu/Mint).



