---
description: Schritt für Schritt Tutorial zur automatischen Installation von offenen TELEMAC-MASCARET auf Debian Linux und Ubuntu-basierten Systemen mit Installationsskripten.
---

(telemac-autoinstall)=
# TELEMAC (Auto-Installation)


## Vorwort

Dieses Tutorial führt Sie durch die Installation von [open TELEMAC-MASCARET](http://www.opentelemac.org/) auf [Debian Linux](https://www.debian.org/) und Ubuntu-basierten Systemen mit **automatische Installer*** Scripten. **Plan für ca. 1-2 Stunden und eine stabile Internetverbindung; die Downloads über 1,4 GB* Für detaillierte Installationsanweisungen gehen Sie an die {ref}`detailed TELEMAC installation page <telemac-install>`.


(telemac-autoinstall-requirements)=
## Anforderungen

### Systempakete

`````{tab-set}
````{tab-item} Debian 12

Auf Debian 12, fragen Sie Ihren Systemadministrator, ob Sie die folgenden Pakete per aptitude sudo-installieren:

```bash
sudo apt update

sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins libopenmpi-dev openmpi-bin libhdf5-dev hdf5-tools libmetis-dev libmumps-dev libmumps-seq-dev libscalapack-openmpi-dev libmedc-dev libmed-dev libmedimport-dev libmed-tools python3-pytest-cython python3-sphinx python3-alabaster python3-cftime libcminpack1 python3-docutils python3-h5py python3-imagesize clang python3-netcdf4 python3-nlopt python3-nose python3-numpydoc python3-patsy python3-psutil liblzf1 python3-stemmer python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev liblapacke-dev libxml2-dev llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff-dev libgeotiff-dev libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```

````

````{tab-item} Ubuntu 24 / Mint 22
Auf Ubuntu 24 (oder Mint 22) fragen Sie Ihren Systemadministrator, ob Sie die folgenden Pakete per Aptitude sudo-installieren:

```bash
sudo apt update
sudo apt install -y --no-install-recommends  python3-numpy python3-scipy python3-matplotlib python3-pip python3-dev python3-venv libgl1 libegl1 libxrandr2 libxss1 libxcursor1 libxcomposite1 alsa-base libxi6 libxtst6  python-is-python3 git git-lfs gfortran build-essential cmake dialog gedit gedit-plugins  libmedc11t64 libmedc-dev libmed-tools libmed11 libmed-dev libmedimport0v5 libmedimport-dev  libopenmpi-dev openmpi-bin libhdf5-dev libhdf5-openmpi-dev hdf5-tools libmetis-dev libmumps-seq-dev libmumps-dev  libscalapack-openmpi-dev python3-pytest-cython python3-sphinx python3-alabaster python3-cftime  libcminpack1 python3-docutils libfreeimage3 python3-h5py python3-imagesize liblapacke  clang python3-netcdf4 libnlopt0 libnlopt-cxx0 python3-nlopt python3-nose python3-numpydoc  python3-patsy python3-psutil libtbb12 libxml++2.6-2v5 liblzf1 python3-stemmer  python3-sphinx-rtd-theme python3-sphinxcontrib.websupport sphinx-intl python3-statsmodels  python3-toml pyqt5-dev pyqt5-dev-tools libboost-all-dev libcminpack-dev libcppunit-dev  doxygen libeigen3-dev libfreeimage-dev libgraphviz-dev libjsoncpp-dev libxml2-dev  llvm-dev libnlopt-dev libnlopt-cxx-dev libqwt-qt5-dev libfontconfig1-dev libglu1-mesa-dev  libxcb-dri2-0-dev libxkbcommon-dev libxkbcommon-x11-dev libxi-dev libxmu-dev libxpm-dev  libxft-dev libicu-dev libsqlite3-dev libxcursor-dev libtbb-dev libqt5svg5-dev  libqt5x11extras5-dev qtxmlpatterns5-dev-tools libpng-dev libtiff5-dev libgeotiff-dev  libgif-dev libgeos-dev libgdal-dev texlive-latex-base libxml++2.6-dev libfreetype6-dev  libgmp-dev libmpfr-dev libxinerama-dev python3-sip-dev tcl-dev tk-dev
```
````
`````

Beachten Sie, dass das automatische Installer-Skript zusätzliche Pakete erkennen kann, die erforderlich sind.

### Installationspfade einrichten

TELEMAC wird aus dem GitLab-Repository in ein von Ihnen gewähltes Verzeichnis (git-cloned) heruntergeladen und im folgenden als **ROOT**-Verzeichnis bezeichnet. Außerdem wird SALOME in diesem ROOT-Verzeichnis heruntergeladen und installiert. Wählen Sie eine der folgenden Einstellungen:

* Alleinbenutzer ohne Admin-Rechte: `ROOT=/home/<USERNAME>/opt` (also `ROOT=$HOME/opt`) (XDG-konforme Alternative: `ROOT=$HOME/.local`)
* Geteilte Nutzung ohne root: nur, wenn bereits ein gruppenbeschreibbarer Standort vorhanden ist, z.B. ein NFS-Aktien wie `ROOT=/srv/shared/telemac`
* Systemweit (admin erforderlich) auf Debian-basierten Systemen: Bevorzugt `ROOT=/usr/local` (Kombinationen in `/usr/local/bin`, Bibliotheken in `/usr/local/lib`); `ROOT=/opt` ist auch für einen selbstständigen Baum akzeptabel


### SALOME

Die Wahl der richtigen Version von SALOME kann nicht einfach automatisiert werden, so finden und laden Sie die neueste Version von SALOME und speichern Sie sie im ROOT-Verzeichnis, wo Sie Telemac installieren möchten.

```{admonition} How TELEMAC binds to MED files and SALOME
:class: important

TELEMAC liest und schreibt `.med` meshes durch seine HERMES-Schicht, die gegen die **system MED-Bibliotheken* kompiliert wird (die `libmedc-dev` /`libmed-dev` / `libmedimport-dev`pakete) - **not** gegen die MED-Bibliotheken, die innerhalb von SALOME gebündelt sind. SALOME versendet seinen eigenen MED, der mit einem anderen ABI (64-bit `med_int` und einem anderen HDF5 Build) gebaut wurde und zusammen mit TELEMAC Triggers `size of symbol 'med_' changed`link warnen und dem Laufzeitfehler `HERMES_WRONG_MED_FORMAT_ERR` ansteuert.

SALOME wird daher nur für die GUI- und Netzwerkzeuge verwendet. Das Einzelstück, das der Installateur von SALOME ausleiht, ist der Fortran Header `med_parameter.hf`, den Debian/Ubuntu von `libmed-dev` (eine Verpackungslücke) ausgibt; er enthält nur Konstanten und ist ABI-neutral. Aus diesem Grund **installieren Sie SALOME (d.h., stellen Sie `--salome-tar`) vor dem Installieren des Installers, wenn Sie MED-Unterstützung* möchten - ansonsten der Installer nicht `med_parameter.hf` finden kann und MED I/O im generierten Config deaktiviert ist. Der generierte `pysource.*.sh` entfernt zusätzlich alle SALOME MED/HDF5-Verzeichnisse von `LD_LIBRARY_PATH` at runtime, so dass das System MED immer derjenige ist, der geladen wird.
```

1. Bestätigen Sie Ihre Linux-Version:
  * Debian: Katze /etc/os-Release
  * Mint: `lsb_release -a`
  * Ubuntu: `inxi -Sx` (auch auf Mint)

2. SALOME-Build herunterladen
  * Gehen Sie zum [offiziellen SALOME-Downloadformular](https://www.salome-platform.org/?page_id=2430)
  * Wählen Sie die neueste Version mit dem Debian/Ubuntu Build (das entspricht der Ubuntu/Mint-Basis); oder wählen Sie die weniger häufig aktualisierte "Linux Universal"

3. Überprüfen Sie die Prüfsumme: von SALOMEs md5-Seite, holen Sie die passende `.md5`-Datei für Ihr Archiv und überprüfen Sie lokal
  * Beispiel für den 9.15-Terball: Im Download-Verzeichnis des Tarballs laufen Sie `md5sum SALOME-9.15.0.tar.gz` (terminal)
  * Gehen Sie zu SALOMEs [md5 page](https://www.salome-platform.org/?page_id=2818), wählen Sie die entsprechende md5-Datei und überprüfen Sie, ob deren Inhalte genau der Terminalantwort entsprechen
  * ** Nicht überspringen!**

### Die Installationsskripte erhalten

* Debian 12-Benutzer herunterladen:
  * [telemac debian12 installer.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/telemac_debian12_installer.sh) und speichern es im ROOT-Verzeichnis.
  * [systel.debian12.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/systel.debian12.cfg) und speichern es im ROOT-Verzeichnis.
  * [pysource.debian12.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/pysource.debian12.sh) und speichern es im ROOT-Verzeichnis.
* Mint 22 / Ubuntu 24 Benutzer herunterladen:
  * [telemac ubuntu24 installer.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/telemac_ubuntu24_installer.sh) und speichern es im ROOT-Verzeichnis.
  * [systel.mint22.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/systel.mint22.cfg) und speichern es im ROOT-Verzeichnis.
  * [pysource.mint22.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/pysource.mint22.sh) und speichern es im ROOT-Verzeichnis.

Stellen Sie sicher, dass alle Dateien im gleichen (ROOT Installation) Verzeichnis auf Ihrem Computer sind.

## Installateure ausführen

### Installationsmuster
Note that you might need **admin (sudo) rights** for installing additional system packages and that the installation can take a while because the script downloads Telemac. The script installs by default Telemac v9.1.1. To install another version, use the `--tag "TAG"` option when running the scripts; latest tags can be found at [https://gitlab.pam-retd.fr/otm/telemac-mascaret.git](https://gitlab.pam-retd.fr/otm/telemac-mascaret.git). Both installers also install the system MED packages and compile TELEMAC automatically at the end of the run (unless you pass `--skip-compile`).

Um den Installer auszuführen, tippen Sie auf (ersetzen Sie `ROOT` mit Ihrem ROOT-Verzeichnis und `SALOME-x.xx.xSRC.tar.gz` mit dem Namen des von Ihnen heruntergeladenen SALOME-Terballs):

`````{tab-set}
````{tab-item} Debian 12
```bash
cd ROOT
chmod +x telemac_debian12_installer.sh
./telemac_debian12_installer.sh --root "ROOT" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
```

Der Installateur kompilierte bereits TELEMAC am Ende seines Laufs (es sei denn, Sie haben `--skip-compile` geschickt). Um die Umgebung zu laden - und ggf. von Grund auf wieder aufbauen - laufen:
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

Die Installer-Skripte werden den `telemac-mascaret` GitLab repo (mit dem zugewiesenen Tag) und einen `salome`-Ordner klonen, in dem er den SALOME-Terball auspackt. Wenn Sie mit SALOME Fehler machen, überprüfen Sie im Abschnitt die {ref}`detailed SALOME installation instructions <salome-install>` auf der "manuellen" Installation von Telemac.

````{admonition} Test SALOME
:class: tip

SALOME ist jetzt in der `ROOT/salome` installiert und Sie können die GUI wie folgt ausführen:

```bash
cd ROOT/salome
./salome
```
````

Um die Installation zu testen, führen Sie das Skript `config.py` (nach Quellung der Telemac-Umgebung):

```bash
config.py
```


### Installationsbeispiel

Angenommen, Sie arbeiten an Debian 12, entsprechend haben Sie `SALOME-9.15.0-native-DB12-SRC.tar.gz` heruntergeladen, das ROOT-Verzeichnis als `/home/HyInfo/opt/` definiert und `telemac_debian12_installer.sh` heruntergeladen. So kann die Installation mit diesen Befehlen gestartet werden:

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

Angenommen, Sie arbeiten an Debian 12, dementsprechend haben Sie `SALOME-9.15.0-native-DB12-SRC.tar.gz` heruntergeladen, das ROOT-Verzeichnis als `/home/HyInfo/opt/`, heruntergeladen `telemac_debian12_installer.sh` definiert und möchten ** Telemac v9.5.0*** installieren (wenn es unter https://gitlab.pam-retd.fr/otm/telemac-mascaret.git existiert). Diese Installation kann mit diesen Befehlen gestartet werden:

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

Um eine bestehende Installation zu fixieren/zu installieren:

1. Navigieren Sie zu Ihrem TELEMAC-Verzeichnis:

  ```bash
  cd ~/opt/telemac-mascaret
  ```

2. Führen Sie den Installer mit `--skip-apt` um Konfiig-Dateien zu regenerieren (begründet, dass Sie eine neuere Version des Installer-Skripts verwenden)
  
  ```bash
  chmod +x ./telemac_debian12_installer.sh
  ./telemac_debian12_installer.sh --skip-apt --root "/ROOTDIR" --salome-tar "ROOT/SALOME-x.xx.xSRC.tar.gz"
  ```

3. Regenerate von re-running config und compile:

  ```bash
  source configs/pysource.debian12.sh
  compile_telemac.py --clean
  ```


(testrun-autoinstaller)=
## Prüfung TELEMAC

** Geschätzte Dauer: 5-10 Minuten.***

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


Führen Sie einen vordefinierten Fall aus dem Ordner `examples` aus:

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
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

In einem neuen Terminal-Tab führen Sie ein TELEMAC-Beispiel mit der `--ncsize=N`fahne, wobei `N` die Anzahl der logischen CPUs ist, die verwendet werden sollen (mindestens `N` stehen zur Verfügung):

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas --ncsize=4
```

Alternativ verwenden Sie `--nctile` und `--ncnode`, um Kerne pro Knoten (NCTILE) und Anzahl der Knoten (NCNODE) mit `NCSIZE = NCTILE * NCNODE` anzugeben. Die folgenden beiden Befehle sind gleichwertig (von `~/opt/telemac-mascaret/examples/telemac2d/donau`):

```bash
telemac2d.py t2d_donau.cas --nctile=4 --ncnode=2
telemac2d.py t2d_donau.cas --ncsize=8
```

```{admonition} Got errors?
:class: error, dropdown

Wenn es schwere Fehler gibt, hat der automatische Installer möglicherweise nicht für Ihr System (oder Subversion) gearbeitet. In diesem Fall ist es sicher, zu starten und {ref}`install Telemac manually <telemac-install>`.

````


### TELEMAC generieren Dokumentation

TELEMAC enthält viele Anwendungsbeispiele unter `/telemac-mascaret/examples/` und Sie können die Benutzer- und Referenzhandbücher lokal erstellen. Zuerst die TELEMAC-Umgebung laden:

```bash
source ~/opt/telemac-mascaret/configs/pysource.mint22.sh
```

Um das Benutzerhandbuch zu generieren (dies kann eine Weile dauern und erfordert Latex, d.h. `texlive` auf Debian/Ubuntu):

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
`validate_telemac.py` iteriert durch viele Beispiele. Einige können scheitern, wenn optionale Module nicht installiert sind (z.B. HERMES) oder wenn ein Beispiel veraltet ist. Die Erstellung von PDFs erfordert in der Regel eine LaTeX-Toolchain (z.B. `texlive` auf Debian/Ubuntu); installieren Sie sie, wenn der Dokumentationsschritt fehlende LaTeX-Executables meldet.
```



## Utilities (Vor- und Nachbearbeitung)

Um Vor- und Nachbearbeitungsprogramme zu installieren, finden Sie die Anweisungen im {ref}`manual installation section <install-telemac-utilities>`, wie BlueKenue oder dem Q4TS-Plugin in QGIS. Beachten Sie, dass für das Q4TS-Plugin Ihr SALOME ausführbarer Pfad `/ROOT/salome/salome` ist und Ihr Telemac *environnement*-Skript `/ROOT/telemac-mascaret/configs/pysource.debian12.sh` (oder `/ROOT/telemac-mascaret/configs/pysource.mint22.sh` wenn Sie auf Ubuntu/Mint installiert sind).



