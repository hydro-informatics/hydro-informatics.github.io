---
description: Schritt für Schritt Installationsanleitung für offene TELEMAC-MASCARET auf Debian Linux und Ubuntu, die alle Abhängigkeiten, Zusammenstellung und Umgebungskonfiguration für hydromorphodynamische Simulationen abdeckt.
---

(telemac-install)=
# TELEMAC (Installation)


## Vorwort


This tutorial walks you through installing [open TELEMAC-MASCARET](http://www.opentelemac.org/) on [Debian Linux](https://www.debian.org/)-based systems (including Ubuntu and derivatives like Linux Mint). **Plan for roughly 1-2 hours and a stable internet connection; the downloads exceed 1.4 GB.**

```{admonition} Developer instructions
:class: note

Die TELEMAC-Entwickler bieten aktuelle Bauanleitungen unter [https://gitlab.pam-retd.fr/otm/telemac-mascaret/ > BUILDING.md](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/main/BUILDING.md), obwohl die Dokumentation für optionale Komponenten begrenzt bleibt.
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

Das österreichische Ingenieurbüro *Flussplan* bietet einen Docker Container von TELEMAC v8 auf ihrem [docker-telemac GitHub repository](https://github.com/flussplan/docker-telemac). Beachten Sie, dass ein Docker-Container eine einfach zu installierende virtuelle Umgebung darstellt, die die plattformübergreifende Kompatibilität nutzt, aber die Rechenleistung beeinflusst. Wenn Sie die proprietäre Docker-Software installiert und rechnerische Leistung ist nicht die primäre Sorge für Ihre Modelle, Flussplans Docker-Container könnte eine gute Wahl. So werden beispielsweise rein hydrodynamische Modelle mit geringen Anzahl von Netzknoten und ohne zusätzliche TELEMAC-Modul-Implikationen effizient im Docker-Container laufen.

````
`````

(modular-install)=
## Grundlegende Anforderungen

```{admonition} Good to know
:class: tip

* Die Installation von TELEMAC auf einem {ref}`Virtual Machine (VM) <chpt-vm-linux>` ist eine bequeme Möglichkeit, um zu starten und Muster-Fälle auszuführen, aber es ist nicht für Anwendungs-Skala-Modelle aufgrund der Leistung über Kopf von VMs empfohlen.
* Machen Sie sich mit dem {ref}`Linux Terminal <linux-terminal>` wohl; Sie brauchen es, um den Workflow von TELEMAC zu kompilieren und eventuell zu beheben.
* Während dieses Tutorials beziehen wir uns auf das Paket *open TELEMAC-MASCARET* als TELEMAC. *MASCARET* ist ein eindimensionales (1D) Modul, während die hier hervorgehobenen Methoden sich auf zweidimensionale (2d) und dreidimensionale (3d) Modellierung konzentrieren.
```

```{admonition} Admin (sudo) rights required for installing basic and optional requirements
:class: attention, dropdown

Superuser Privilegien (`sudo` für **su**per **do**ers-Liste) sind für viele Schritte in diesem Workflow erforderlich, wie z.B. die Installation von Paketen, die Systemkonfiguration und das Schreiben an Systemverzeichnisse. Bei Debian wird der sudo-Zugang typischerweise durch die Installation von `sudo`, das Hinzufügen Ihres Kontos an die `sudo`-Gruppe und die Verwaltung von Berechtigungen sicher mit `visudo` (die `/etc/sudoers` bearbeitet) gewährt. Detaillierte Setup-Anweisungen finden Sie im Tutorial {ref}`Debian Linux <user-rights>` und sprechen Sie mit Ihrem Systemadministrator.
```

Die Zusammenarbeit mit TELEMAC erfordert Software, um Quelldateien herunterzuladen, zu kompilieren und das Programm auszuführen. Die obligatorischen Softwarevoraussetzungen für die Installation von TELEMAC auf [Debian Linux](https://www.debian.org/)] werden in den folgenden Abschnitten erläutert.


### Python3

** Geschätzte Dauer: 5-8 Minuten.**

Python3 wurde standardmäßig auf Debian seit Version 10 (Buster) installiert und es ist erforderlich, TELEMACs Compiler/launcher-Skripte auszuführen. Um Python3 zu starten, öffnen Sie ein Terminal und führen Sie `python3`; um zu beenden, verwenden Sie `exit()` oder drücken Sie `Ctrl+D`.

TELEMAC benötigt die [NumPy](https://numpy.org/)Bibliothek; die meisten Workflows setzen sich auch auf [SciPy](https://scipy.org/) und [Matplotlib](https://matplotlib.org/). Da TELEMAC nicht standardmäßig ist, hilft Python Header und eine saubere Umgebung.

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

Um zu testen, ob die Installation erfolgreich war, geben Sie `python3` in Terminal ein und importieren Sie die drei Bibliotheken:

```bash
Python 3.11.1 (default, Jul  25 2030, 13:03:44) [GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> a = numpy.array((1, 1))
>>> print(a)
[1 1]
>>> exit()
```

Keiner der drei Bibliotheksimporte sollte eine `ImportError`-Nachricht zurückgeben. Um mehr über Python zu erfahren, lesen Sie den Abschnitt unter {ref}`sec-pypckg`.

(tm-git-requirements)=
### Gier

** Geschätzte Dauer: <5 Minuten**

Installation und Nutzung von Git sind unter der {ref}`git section of this eBook <chpt-git>`. Zusätzlich zu dem, was dort beschrieben wird, benötigen Sie Git Large File Storage (Git LFS), um große Vermögenswerte zu handhaben, wenn ein TELEMAC-bezogenes Repository es verwendet. Bei Debian benötigen Sie in der Regel nur `git` (nicht `git-all`, die viele Extras zieht), plus `git-lfs`. Installieren und initialisieren:

```bash
sudo apt update
sudo apt install git git-lfs
git lfs install
```

`git lfs install` richtet LFS für Ihr Benutzerkonto ein; so ist es harmlos, auch wenn ein bestimmtes Repository keine LFS verwendet.


### GNU Fortran 95 Compiler (gfortran)

** Geschätzte Dauer: 3-10 Minuten.***

Das Python-basierte Build-System von TELEMAC erfordert einen Fortran-Compiler; die gemeinsame Wahl auf Debian ist der GNU Fortran-Compiler (`gfortran`), der rückwärtskompatibel mit GNU Fortran 95 ist und neuere Standards unterstützt. Debian liefert `gfortran` aus seinen Standard-Repositories. Um es zu installieren, öffnen Sie ein Terminal und führen Sie:

```bash
sudo apt update
sudo apt install gfortran

```

Nach der Installation überprüfen Sie Ihr Setup mit `gfortran --version`; der Compiler muss auf Ihrem `PATH` für TELEMAC Skripte sein, um es zu finden.

```{admonition} If the gfortran installation fails...
:class: attention, dropdown


Ensure the standard Debian "main" component is enabled in your APT sources so the `gfortran` package is available. Edit `/etc/apt/sources.list` as root (or add a file in `/etc/apt/sources.list.d/`), then run `sudo apt update`. Verify availability with `apt-cache policy gfortran` or `apt search gfortran`; note that `gfortran` is a metapackage that installs the current default version (for example, `gfortran-12` or `gfortran-13`). Package details are listed here: [https://packages.debian.org/search?keywords=gfortran](https://packages.debian.org/search?keywords=gfortran).
```

### Mehr Compiler und Essentials

** Geschätzte Dauer: 2-5 Minuten.**

Für den Aufbau von TELEMAC und dessen Abhängigkeiten benötigen Sie C/C++ und CMake. Installieren Sie Debians `build-essential` (die `gcc`, `g++` und `make`) und `cmake` angibt; dies ist erforderlich, um Quellen zu kompilieren, einschließlich paralleler (MPI) Builds, obwohl MPI selbst von Paketen wie OpenMPI bereitgestellt wird, die Sie später installieren werden. Das `dialog`-Paket ist optional, aber nützlich, da einige Helper-Skripte einfache Textschnittstellen verwenden. Für die Bearbeitung von Shell-Skripten können Sie `gedit` ([weiterlesen](https://wiki.gnome.org/Apps/Gedit) oder Alternativen wie Nano oder Vim) verwenden. Lauft!

```bash
sudo apt update
sudo apt install -y build-essential cmake dialog gedit gedit-plugins
```


### Installationspfad einrichten

Bis zu diesem Punkt wurde Software über Debians Paketmanager (APTITUDE, `apt`) installiert. Im Gegensatz dazu wird TELEMAC (d.h. git-cloned) aus dem GitLab-Repository in ein Verzeichnis heruntergeladen, das Sie wählen. Sein Build/install Workflow ist insbesondere nicht standardmäßig, so dass Pfadwahlen wichtig sind. Wählen Sie eine der folgenden Einstellungen:

* Alleinbenutzer ohne Admin-Rechte: `ROOT=/home/<USERNAME>/opt` (also `ROOT=$HOME/opt`) (XDG-konforme Alternative: `ROOT=$HOME/.local`)
* Geteilte Nutzung ohne root: nur, wenn bereits ein gruppenbeschreibbarer Standort vorhanden ist, z.B. ein NFS-Aktien wie `ROOT=/srv/shared/telemac`
* Systemweit (admin erforderlich) auf Debian-basierten Systemen: Bevorzugt `ROOT=/usr/local` (Kombinationen in `/usr/local/bin`, Bibliotheken in `/usr/local/lib`); `ROOT=/opt` ist auch für einen selbstständigen Baum akzeptabel

In den folgenden Abschnitten zeigen wir eine Einzelbenutzerinstallation von TELEMAC (einschließlich SALOME) mit `ROOT=/home/HyInfo/opt`.


### Holen Sie sich TELEMAC Repo

** Geschätzte Dauer: 25-40 Minuten (große Downloads).***

Holen Sie die TELEMAC Quellen mit Git-LFS. Im Terminal erstellen oder wählen Sie Ihr Arbeitsverzeichnis (hier: `/home/HyInfo/opt` - siehe oben), und ändern Sie (`cd`) in es; zum Beispiel:

```bash
cd /home/HyInfo/opt
git clone https://gitlab.pam-retd.fr/otm/telemac-mascaret.git
```

Damit wird das Repository in ein Unterverzeichnis namens `telemac-mascaret`. Für schnellere Downloads können Sie einen flachen Klon mit `--depth=1` verwenden, um zu verstehen, dass diese Geschichte begrenzt.

````{admonition} There are many (experimental) branches of TELEMAC available
:class: tip, dropdown

Das TELEMAC git Repository bietet viele andere TELEMAC-Versionen in Form von Entwicklungs- oder Old-Versionen. Zum Beispiel, die folgenden Klone der `upwind_gaia` Zweig an einen lokalen Unterordner namens `telemac/gaia-upwind`. Nach dem Klonen dieses einzelnen Zweiges kann das Kompilieren von TELEMAC wie im folgenden beschrieben erfolgen.

```
git clone -b upwind_gaia --single-branch https://gitlab.pam-retd.fr/otm/telemac-mascaret.git telemac/gaia-upwind
```

Lesen Sie mehr über die Klonierung einzelner TELEMAC-Niederlassungen in der [TELEMAC wiki](http://wiki.opentelemac.org/doku.php?id=telemac-mascaret_git_repository).
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


## Optionale Anforderungen (Parallelismus und andere)

Dieser Abschnitt führt Sie durch die Installation zusätzlicher Pakete, die für die parallele Ausführung erforderlich sind und mit {ref}`SALOME <salome-install>`'s `.med`-Dateien arbeiten. Bestätigen Sie, dass das Terminal `gcc` (typischerweise über `build-essential`) mit `gcc --version` installiert ist. Die folgenden Pakete ermöglichen Parallelität und bieten erhebliche Geschwindigkeiten für Simulationen:

* Nachrichtenübermittlung (MPI)
* Metis

(tm-system-wide-opts)=
### Systembreite Installation
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

* `libopenmpi-dev` und `openmpi-bin` bieten MPI-Header und `mpirun/mpiexec`.
* `libmetis-dev` liefert den Partitionierer TELEMAC `partel`.
* `libhdf5-dev` wird von MED verlangt; `libmedc-dev` und `libmed-tools` bieten MED I/O-Unterstützung, die von SALOME-generierten Maschen verwendet wird.
* `libmumps-dev` und `libscalapack-openmpi-dev` sind häufige Solvenz-Backends für große, parallele Abläufe.

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

Die MED-Bibliothek (aus dem {ref}`SALOME <salome-install>`-Ökosystem) bietet mesh/result I/O, die von vielen TELEMAC-Workflows verwendet wird. Um MED selbst zu bauen, stellen Sie sicher, dass die HDF5-Version mit der zum Kompilieren verwendeten Version übereinstimmt und Python-Bindungen deaktivieren, es sei denn, Sie erfüllen auch die erforderlichen SWIG/Python-Header. Dann bauen Sie es:

```bash
./configure --prefix=$HOME/telemac/optionals/med-4.1.1 --disable-python
make
make install
```

Anmerkungen:
* `--disable-python` vermeidet SWIG-Versionskonflikte; die Aktivierung von Python erfordert übereinstimmende `python3-dev`-Header und eine kompatible SWIG-Veröffentlichung.
* MED-Versionskompatibilität mit Ihrem HDF5-Building ist kritisch; Mischsystem HDF5 mit einem maßgeschneiderten MED (oder umgekehrt) TELEMAC I/O bricht häufig.

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

Weitere MPI-Installationshinweise sind in der [opentelemac wiki](http://wiki.opentelemac.org/doku.php?id=installation_linux_mpi).
````


(salome-install)=
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

2. SALOME-Build herunterladen
   * Gehen Sie zum [offiziellen SALOME-Downloadformular](https://www.salome-platform.org/?page_id=2430)
   * Wählen Sie die neueste Version mit dem Ubuntu Build (das entspricht der Mint-Basis); oder wählen Sie die weniger häufig aktualisierte "Linux Universal"

3. Überprüfen Sie die Prüfsumme: von SALOMEs md5-Seite, holen Sie die passende `.md5`-Datei für Ihr Archiv und überprüfen Sie lokal
   * Beispiel für den 9.15-Terball: Im Download-Verzeichnis des Tarballs laufen Sie `md5sum SALOME-9.15.0.tar.gz` (terminal)
   * Gehen Sie zu SALOMEs [md5 page](https://www.salome-platform.org/?page_id=2818), wählen Sie die entsprechende md5-Datei und überprüfen Sie, ob deren Inhalte genau der Terminalantwort entsprechen
   * ** Nicht überspringen!**

4. Extrahieren Sie irgendwo sauber und gesund; zum Beispiel als `sudo` für das gesamte System (Anpassen Sie den Namen, wenn Sie ein anderes Archiv gewählt haben), oder folgen Sie diesem Workflow fow Installation TELEMAC in `/home/HyInfo/opt/`:
  
    ```bash
    mkdir -p /home/HyInfo/opt/salome
    tar -xzf ~/Downloads/SALOME-9.15.0.tar.gz -C /opt/salome --strip-components=1
    chown -R "$USER":"$USER" /home/HyInfo/opt/salome
    ```

````{admonition} Troubleshoot "chown: invalid group: ..."
:class: error, dropdown

Wenn Sie eine Nachricht wie `chown: invalid group: myuser:myuser` erhalten, bedeutet das, dass `chown` sich beschwert, weil es keine Gruppe namens `myuser` auf dem Computer gibt. Der Besitzer `myuser` existiert, aber die Gruppe myuser nicht. Um dies zu beheben, überprüfen Sie zuerst Ihre eigentliche Primärgruppe:

```bash
id
```

Dies sollte so etwas wie `uid=1234(myuser) gid=100(users) groups=100(users),123(othergroup)` zurückgeben. Jetzt haben Sie zwei Möglichkeiten zur Fehlerbehebung:

Option 1: Ersetzen Sie die zweite `$USER` mit Ihrer primären Gruppe von `id`:

```bash
chown -R "$USER":"$(id -gn "$USER")" /home/HyInfo/opt/salome
```

Option 2 ( robuster): Auto-Detektion Ihrer Primärgruppe verwenden:

```bash
chown -R "$USER":"$(id -gn "$USER")" /home/HyInfo/opt/salome
```
````


5. Lassen Sie SALOME Ihr System überprüfen und installieren, was es verlangt
   * Wählen Sie im extrahierten SALOME-Verzeichnis den Anwendungsnamen aus
   ```bash
   cd /home/HyInfo/opt/salome/sat
   ./sat config --list
   ```
   * Verwenden Sie den angegebenen Bewerbungsnamen; die folgenden Beschreibungen gehen davon aus, dass der Bewerbungsname `SALOME-9.15.0-native` ist
   * Führen Sie den eingebauten Checker aus; es druckt, welche Pakete fehlen könnten:
   ```bash
   cd /home/HyInfo/opt/salome/sat
   ./sat config SALOME-9.15.0-native --check_system
   ```
   * Installieren Sie die Pakete, die es über `apt` auflistet, und führen Sie dann den Scheck, bis er sauber ist.

6. Stellen Sie sicher, dass 3D/OpenGL in Ordnung ist: Überprüfen Sie den richtigen Treiberstapel (insbesondere für NVIDIA) vor dem Start; Lesen Sie mehr über [SALOME PLATFORM FAQ](https://www.salome-platform.org/?page_id=428)

7. Starten Sie SALOME aus dem Ordner SALOME:
  * wenn im Unterordner `/sat` der erste Typ `cd ..`
  * lauf salome: `./salome`

Wenn Sie Berechtigungsfehler treffen, stellen Sie sicher, dass Sie an einen Standort, den Sie besitzen, extrahiert oder das Eigentum repariert. Einige Benutzer liefen in Probleme, die seltsame Standorte oder WSL versuchen; halten Sie sich an einen normalen Dateisystempfad, den Sie steuern.

Es gibt auch eine Container-Option: man kann SALOME über Docker/Apptainer ausführen, aber ParaViS/ParaView Beschleunigung innerhalb von Containern ist ursächlich Buggy und bricht oft; die SALOME-Forumdokumente machen Probleme in Docker.



(compile-tm)=
## Compile TELEMAC

### Anpassung und Überprüfung der Konfigurationsdatei (systel.x.cfg)

** Geschätzte Dauer: 2-20 Minuten.***


Die `systel.x.cfg`-Datei sagt TELEMAC, wie Sie ihre Module auf Ihrem Computer erstellen und starten. Genauer gesagt, es ist die zentrale Konfiguration von TELEMAC, die Builds und Laufzeitumgebungen definiert, einschließlich Compiler, Compiler-Flags, MPI und zugehörige Optionen, externe Bibliotheken und Pfade. In der Praxis verwenden wir diese Datei, um Flaggen zu erklären und TELEMAC auf optionale Abhängigkeiten zu verweisen. Standardmäßig sucht TELEMAC Konfigurationsdateien unter `./configs/` (z.B. `configs/systel.cfg`) und man kann den Pfad mit der `SYSTELCFG`-Umgebungsvariable oder der `-f`-Option des Python Launchers überschreiben.

Dieser Abschnitt beschreibt die Einrichtung von `systel.x.cfg` für:

* Linux Mint 22 (getestet) und Ubuntu 24.04 (erwartet als identisch, noch nicht getestet)
* Debian 12 (Test im Fortschritt)

Beachten Sie, dass wir die Einweg-Installation von TELEMAC unter dem lokalen Home-Verzeichnis `/home/HyInfo/opt/telemac-mascaret` beschreiben und SALOME in `/home/HyInfo/opt/salome` installiert haben.

Beachten Sie, dass wir die API weder aktiviert haben noch die [AED2 (waqtel)](http://wiki.opentelemac.org/doku.php?id=installation_linux_aed) und [GOTM (general ocean)](http://wiki.opentelemac.org/doku.php?id=installation_linux_gotm)module.

Unsere `cfg` und `pysource`-Dateien definieren einen einzigen Build (z.B. `hyinfompiubu` auf Mint / Ubuntu) für [TELEMAC v9.0](https://www.opentelemac.org/)9@@@, der `mpi` und `dyn`-Optionen ermöglicht und GNU-Compiler verwendet (`cc=mpicc`,`fc=mpifort`, unterstützt von`gfortran`). Externe Bibliotheken werden über Bibliotheksblöcke für **OpenMPI, HDF5, MED** (via{ref}`SALOME <salome-install>`), **METIS und MUMPS** mit ScaLAPACK, BLAS und LAPACK verknüpft. RPATH-Einträge werden hinzugefügt, so dass die Laufzeit HDF5 und verwandte Bibliotheken lokalisieren kann, indem Pfade verwendet werden, die typisch Debian- und Ubuntu-Layouts entsprechen.


`````{tab-set}
````{tab-item} Mint 22 / Ubuntu 24

The following configuration provides a TELEMAC configuration called **hyinfompiubu**. It  enables optimized core flags, position-independent builds, and big-endian unformatted I/O with modified record markers, plus MPI settings on Linux Mint 22 / Ubuntu 24.04. Executables are launched with `mpirun -np <ncsize>`, and meshes are partitioned using `partel`. Build artifacts are placed under `<root>/builds/hyinfompiubu/{bin,lib,obj}`, and the file also defines suffixes, validation paths, and Python F2PY settings (`f2py`, `gnu95`).

Zum Kompilieren von TELEMAC:

1. Laden Sie [systel.mint22.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/systel.mint22.cfg) von unserem GitHub-Repository herunter oder kopieren Sie die untenstehenden Dateiinhalte in den Ordner TELEMAC`/configs`, hier: `/home/HyInfo/opt/telemac-mascaret/configs`.
2. Öffnen Sie `systel.mint22.cfg` in einem Texteditor (z.B. gedit) und ersetzen Sie die beiden `/home/HyInfo/opt/salome` path Intances durch Ihren SALOME-Installationspfad.
3. Überprüfen Sie Installationspfade von optionalen, insbesondere HDF5, MED und Mumps.
4. Sparen Sie `systel.mint22.cfg` und schließen Sie den Texteditor.


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

1. Laden Sie [systel.debian12.cfg](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/systel.debian12.cfg) von unserem GitHub-Repository herunter oder kopieren Sie die untenstehenden Dateiinhalte in den Ordner TELEMAC`/configs`, hier: `/home/HyInfo/opt/telemac-mascaret/configs`.
2. Öffnen Sie `systel.debian12.cfg` in einem Texteditor (z.B. gedit) und ersetzen Sie die beiden `/home/HyInfo/opt/salome` path Intances durch Ihren SALOME-Installationspfad.
3. Überprüfen Sie Installationspfade von optionalen, insbesondere HDF5, MED und Mumps.
4. Sparen Sie `systel.debian12.cfg` und schließen Sie den Texteditor.

Wo Pakete typischerweise auf Debian 12 leben:

* OpenMPI Wrapper und Launcher: `/usr/bin/mpifort`, `/usr/bin/mpicc`, `/usr/bin/mpirun` oder `/usr/bin/mpiexec`.
* Parallel HDF5: Header sind in `/usr/include/hdf5/openmpi`, libs in `/usr/lib/x86_64-linux-gnu/hdf5/openmpi` via `libhdf5-openmpi-dev`.
* METIS/ParMETIS: Header sind in `/usr/include`; libs in `/usr/lib/x86_64-linux-gnu`.

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

Die folgenden Erläuterungen geben Anleitungen zur Anpassung einer `cfg`-Datei und Referenzvorlagen im `/configs`-Ordner von TELEMAC. Diese Anweisungen sind für Benutzer gedacht, die keine Ap-Installationen von OpenMPI, MUMPS, Metis und HDF5 verwendet haben (siehe Infobox in der {ref}`installation instructions for optionals <tm-system-wide-opts>`.

Eine typische `systel.*.cfg`-Datei hat:
1. Eine optionale `[Configurations]`-Liste, die verfügbare Bauabschnitte auszählt.
2. Eine `[general]` Sektion mit Standardeinstellungen.
3. Eine oder mehrere Bauabschnitte wie `[debgfopenmpi]`, die von `[general]` und übergeordnete Spezifika erben. TELEMAC versendet Beispiel configs wie `systel.edf.cfg` mit diesen Mustern.

** Auswahl der richtigen Konfigurationsvorlage:**
* TELEMAC sendet zum Beispiel config-Dateien in `<root>/configs` (z.B. `systel.edf.cfg`) mit Parallel/Debug-Abschnitten für GNU/Intel; kopieren und anpassen eines für Debian 12.
* Der Python Launcher liest den aktiven Abschnitt von Ihrem `systel.*.cfg`; stellen Sie `USETELCFG`-Punkte an `[debgfopenmpi]` (oder Ihren gewählten Abschnitt) sicher.

Ein roher OpenMPI/gfortran-Bereich in der `cfg`-Datei könnte so aussehen für eine neu definierte Konfiguration namens `debgfopenmpi`:

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
 
* `par_cmdexec` sagt TELEMAC, der Befehl, Ihr Netz für einen Parallellauf zu teilen. `partel` ist der Splitter; die Umleitung `< <partel.par>` ernährt ihre Parameterdatei und die `>> <partel.log>` sammelt ihre Ausgabe. Sie halten diese Linie, um parallele Ausführung zu ermöglichen; entfernt es bricht Spaltung und liefert "PARTEL.PAR nicht gefunden" oder ähnliche Fehler. Die offiziellen Linux-Installationsnotizen benötigen einen Partitioner für Parallel-Builds.
* `mpi_cmdexec` ist der Laufzeitstarter. Auf Debian 12 werden sowohl `/usr/bin/mpirun` als auch `/usr/bin/mpiexec` durch OpenMPI-Pakete bereitgestellt und sind für unsere Zwecke gleichwertig. Der `<wdir>` placeholder ist das Arbeitsverzeichnis; `<ncsize>` ist die Zahl der MPI-Ranks; `<exename>` ist der produzierte Soldat.
* `cmd_obj`, `cmd_lib`, `cmd_exe` definieren die genauen Compile-, Archiv- und Link-Befehle. Man kann `mpifort` anstatt `gfortran` anrufen; der Wrapper setzt die richtigen MPI-Header und libs für das von Ihnen installierte OpenMPI ein. Damit wird eine spröde Hartcodierung von `-I/usr/lib/.../openmpi/include` oder `-lmpi` mit einem spezifischen SONAME vermieden. Open MPI ermutigt diese Praxis, weil die Flaggen je nach Aufbau und Paket variieren.
* Zu den `mods_all`-Appends gehören Pfade für Moduldateien, die TELEMAC während der Zusammenstellung erzeugt; unter `<config>` die Schnittstellen zwischen den Komponenten freigibt.
* `incs_all` und `libs_all` sind, wo Sie nicht-MPI-Optionen hinzufügen, die Sie tatsächlich aktiviert haben, wie AED2, MED, METIS, HDF5. Lassen Sie reine MPI aus diesen; lassen Sie die Wrapper Griff MPI.

**Importante Compiler-Flags:**
* `-cpp` ermöglicht die Vorverarbeitung von Fortran-Quellen so `#include`,`#if` und `#define`. TELEMAC-Quellen verwenden bedingte Zusammenstellung; ohne Vorverarbeitung werden diese Richtlinien ignoriert und die Zusammenstellung kann scheitern. Jeder moderne Fortran-Compiler mit einem C-ähnlichen Vorprozessor akzeptiert diese Form.
* `-DNAME` Makros wie `-DHAVE_MPI` oder `-DHAVE_AED2` definieren Präprozessorsymbole, die die Quelle in `#ifdef`-Blöcken überprüft, um die richtigen Codepfade zu kompilieren. Wenn AED2 anwesend ist, fügen Sie nur `-DHAVE_AED2` hinzu. Der `-D`-Mechanismus ist standardmäßig über Compiler.
* `-fconvert=big-endian` und `-frecord-marker=4` steuern unformatierte Dateibyte-Bestell- und Aufzeichnungsmarker, so dass Binäre aus verschiedenen Compilern und Plattformen mit den I/O-Erwartungen und Legacy-Dateien von TELEMAC kompatibel bleiben. GNU Fortran dokumentiert diese Optionen; der Standard-Rekorder ist 4 Bytes und die `-fconvert`-Einstellung beeinflusst die Darstellung von unformatierten Datensätzen. Verwenden Sie diese Flaggen konsequent über das Kompilieren und laufen für reproduzierbare unformatierte I/O.
* `-O3` ist eine Standard-Hochoptimierung für Release Builds. Sicher mit gfortran und TELEMAC Code-Basis.


** Allgemeine Anmerkungen:**
* Use `mpifort` (or `mpif90` symlink) and avoid hard-coding `libmpi.so` or MPI include paths. Open MPI's wrapper compilers inject the correct `-I`/`-L`/`-l` automatically; avoid adding MPI headers/libs to `incs_all`/`libs_all`.
* `mpirun` und `mpiexec` sind gültige Starter auf Debian 12; verwenden Sie, was immer Sie bevorzugen.
* METIS/ParMETIS: Verwenden Sie Shared libs (`-lmetis`, `-lparmetis`) anstatt eine statische `.a` in Ihrem Home-Verzeichnis zu codieren, wo Header in `/usr/include` sind; libs in `/usr/lib/x86_64-linux-gnu`.

**Gemeinsame Fallstricke:**
* Entfernen Sie `par_cmdexec` nicht auf "fix" PARTEL-Fehler. Prüfen Sie, dass `<partel.par>` produziert wird und dass METIS verfügbar ist, wenn Sie parallele Auflagen angefordert haben. TELEMAC's docs betonen, dass ein Trenner für den Parallelismus erforderlich ist.
* Schreibe `libs_all` nicht an eine buchstäbliche `.../openmpi/libmpi.so` oder an einen SONAME. Wrapper-Compiler existieren genau, um dies zu vermeiden; SONAMEs und Link-Lines unterscheiden sich durch OpenMPI Build.
* Fügen Sie optionale Bibliotheken nur hinzu, wenn Sie die Funktion tatsächlich aktiviert haben und die Header und Bibliotheken kennen. Beispiel für AED2 gebaut unter Ihrem Heimatverzeichnis:
`incs_all: [..existing..] -I $HOME/telemac/optionals/aed2/include`
`libs_all: [..existing..] -L $HOME/telemac/optionals/aed2 -laed2`
Lassen Sie MPI aus diesen Listen; die Verpackung fügt MPI.


Wenn Sie optionale Optionen aktivieren, fügen Sie nur diese an `incs_all`/`libs_all` (verwenden Sie spezielle Links für manuell installierte Pakete):
* METIS (für TEIL-Netzteiler)
   `incs_all: [inc_metis]` with `inc_metis: -I /usr/include`  
   `libs_all: [libs_metis]` with `libs_metis: -L /usr/lib/x86_64-linux-gnu -lmetis` 
* AED2 (falls Sie es unter `~/telemac/optionals/aed2/` aufgebaut haben)
Fügen Sie `-DHAVE_AED2` an `cmd_obj` an und beinhalten Sie Pfade/lib zu Ihrer AED2-Installation, zum Beispiel:
`incs_all: -I <config> -I $HOME/telemac/optionals/aed2/include`
`libs_all: -L $HOME/telemac/optionals/aed2 -laed2`
Lassen Sie MPI aus diesen Listen; die Verpackung fügt MPI.
* Parallel HDF5 und MED (wenn Sie Serafin/SELAFIN MED I/O in Ihrem Aufbau verwenden)
Beispielfahnen:
`incs_all: [..existing..] -I /usr/include/hdf5/openmpi -I /usr/include`
`libs_all: [..existing..] -L /usr/lib/x86_64-linux-gnu/hdf5/openmpi -lhdf5_fortran -lhdf5hl_fortran -lhdf5_hl -lhdf5 -L /usr/lib/x86_64-linux-gnu -lmedC -lmed`

** Checkliste vor der Zusammenstellung:**
1. `mpifort -show` druckt eine `gfortran`Link-Linie, die bereits MPI libs enthält. Wenn nicht, OpenMPI dev Pakete fehlen.
2. Wenn Sie parallel HDF5 verwenden, existiert `h5pfc -show` und zeigt `.../hdf5/openmpi` in seinem Ausgang; ansonsten installieren Sie `libhdf5-openmpi-dev`.
3. Der gewählte Name `.cfg` ist der unter `USETELCFG`. Die TELEMAC Python-Skripte weigern sich zu bauen, wenn dieser Abschnitt fehlt.
````
`````


### Setup Python Source File

** Geschätzte Dauer: 4-20 Minuten.***

Die Python Quelldatei lebt auch im `/configs`ordner von TELEMAC, wo eine Vorlage namens `pysource.template.sh` zur Verfügung steht. Konkret ist die pysource-Datei ein Shell "env"-Skript, das man in jedem Terminal `source` vor dem Bau oder der Ausführung von TELEMAC. Der Python Launcher setzt vier Anker: `HOMETEL`,`SYSTELCFG`, `USETELCFG` und `SOURCEFILE`. Die Python-Skripte von TELEMAC sehen `SYSTELCFG` aus und wählen den Abschnitt unter `USETELCFG`. Dieser Abschnitt führt entweder über unsere `pysource.mint22.sh` / `pysource.debian12.sh` (ohne AED2) oder eine angepasste Quelldatei.

`````{tab-set}
````{tab-item} Mint 22 / Ubuntu 24

Um die Einrichtung der `pysource.mint22.sh`-Datei auf Linux Mint 22 / Ubuntu 24 zu erleichtern, ist unsere Vorlage für den Einsatz mit der oben beschriebenen `systel.mint22.cfg`-Konfigurationsdatei konzipiert und basiert auf der standardmäßig bereitgestellten `pysource.template.sh`. Zum Kompilieren von TELEMAC:

1. Laden Sie [pysource.mint22.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/ubuntu24-mint22/pysource.mint22.sh) von unserem GitHub-Repository herunter oder kopieren Sie die Dateiinhalte unten in den Ordner TELEMAC`/configs`, hier: `/home/HyInfo/opt/telemac-mascaret/configs` und speichern Sie als `pysource.mint22.sh`.
2. Öffnen Sie `pysource.mint22.sh` in einem Texteditor (z.B. gedit) und überprüfen Sie Installationspfade. Beachten Sie, dass die Datei die folgende Definition enthält, die sie fast unabhängig von der Definition Ihres Installationspfades macht, solange Salome im gleichen Verzeichnis lebt, relativ zu dem, wo Sie TELEMAC heruntergeladen haben:
`_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
3. Überprüfen Sie Installationspfade von optionalen, insbesondere HDF5, MED (insbesondere SALOME) und Mumps.
4. Sparen Sie `pysource.mint22.sh` und schließen Sie den Texteditor.

Unsere `pysource.mint22.sh`-Datei sieht so aus:

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

Um die Einrichtung der `pysource.debian12.sh`-Datei auf Debian 12 zu erleichtern, ist unsere Vorlage für die Verwendung mit der oben beschriebenen `systel.debian12.cfg`-Konfigurationsdatei konzipiert und basiert auf der standardmäßig bereitgestellten `pysource.template.sh`. Zum Kompilieren von TELEMAC:

1. Laden Sie [pysource.debian12.sh](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/debian12/pysource.debian12.sh) von unserem GitHub-Repository herunter oder kopieren Sie die Dateiinhalte unten in den Ordner TELEMAC`/configs`, hier: `/home/HyInfo/opt/telemac-mascaret/configs` und speichern Sie als `pysource.debian12.sh`.
2. Öffnen Sie `pysource.debian12.sh` in einem Texteditor (z.B. gedit) und überprüfen Sie Installationspfade. Beachten Sie, dass die Datei die folgende Definition enthält, die sie fast unabhängig von der Definition Ihres Installationspfades macht, solange Salome im gleichen Verzeichnis lebt, relativ zu dem, wo Sie TELEMAC heruntergeladen haben:
`_THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
3. Überprüfen Sie Installationspfade von optionalen, insbesondere HDF5, MED (insbesondere SALOME) und Mumps.
4. Sparen Sie `pysource.debian12.sh` und schließen Sie den Texteditor.

Unsere `pysource.debian12.sh`-Datei sieht so aus:

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

**Anmerkungen:**
* `SYSTELCFG`-Punkte in Ihrer `.cfg`-Datei; `USETELCFG` muss dem von Ihnen gewünschten Abschnitts-Header entsprechen, z.B. `[debgfopenmpi]`. So entdeckt TELEMACs Python Launcher das "Baurezept".
* `PATH` umfasst sowohl `scripts/python3` als auch `scripts/unix`, so dass Sie `telemac.py`,`compile.py`,`runcode.py` und Shell-Helfer direkt ausführen können.
* `mpifort` and `mpirun` are the correct OpenMPI entry points on Debian 12. `mpif90` exists but is a legacy alias; OpenMPI recommends `mpifort`. `mpirun` and `mpiexec` are synonyms and ship in `/usr/bin`.
* Kein `MPIHOME` und kein `LD_LIBRARY_PATH` Hacking für OpenMPI. Wrapper-Compiler entfernen die Notwendigkeit, OpenMPI zu exportieren, beinhalten/lib-Pfade; Export `LD_LIBRARY_PATH`, um auf OpenMPI-Bibliotheken zu zeigen, ist sowohl unnötig als auch fragil auf Debian
* `wrap_api/lib` auf beiden `PYTHONPATH` und `LD_LIBRARY_PATH` ist der richtige Weg, um TelApy nach dem Bau zu importieren. Dies entspricht, wo TELEMAC die API-Artefakte ausgibt.
* Setzen Sie nicht `MPIHOME=/usr/bin/mpifort.mpich`, wenn Sie mit OpenMPI bauen. Dieser Wert weist auf eine MPICH-Binärin hin und wird falsche Header und Bibliotheken zu kompilieren oder Laufzeit verursachen. Verwenden Sie OpenMPI konsequent oder schalten Sie den gesamten Stack auf MPICH. OpenMPI’s eigenen Docs betonen Wrapper-Konsistenz.
* Do not add `LD_LIBRARY_PATH=$PATH/lib` or point it to `lib/x86_64-linux-gnu/openmpi`. `$PATH` is not a library directory, and hardcoding OpenMPI’s library dir in the env file is unnecessary when you compile and link with `mpifort`.
* Machen Sie keinen Hard-Code `libmpi.so` irgendwo in `pysource` oder in Ihrem `.cfg`, wenn Sie bereits Wrapper-Compiler verwenden. Lassen Sie `mpifort` die Link-Linie fahren.

Wenn Sie Distro-Pakete verwenden, müssen Sie in der Regel keine Pfade in `pysource` festlegen:
* OpenMPI-Tools: `/usr/bin/mpifort`, `/usr/bin/mpicc`, `/usr/bin/mpirun` oder `/usr/bin/mpiexec`.
* Parallel HDF5 (wenn in Ihrem cfg aktiviert): Header unter `/usr/include/hdf5/openmpi`, libs unter `/usr/lib/x86_64-linux-gnu/hdf5/openmpi` via`libhdf5-openmpi-dev`.
* METIS von Debian: Link als `-lmetis` von `libmetis-dev`; Header in `/usr/include`, libs in `/usr/lib/x86_64-linux-gnu`. Bitte über eine handgefertigte `libmetis.a` unter `~/telemac/optionals`.
````
`````

(tm-compile)=
### Zusammensetzen

** Geschätzte Dauer: 20-30 Minuten (Verknüpfung dauert Zeit).***

Der Compiler wird von den Python-Tools von TELEMAC über die Shell-Umgebung aufgerufen, die von Ihrem `pysource`Script (`pysource.mint22.sh` oder `pysource.debian12.sh`) gesetzt wird. Dieses Skript sagt TELEMAC, wo Hilfeprogramme und Bibliotheken leben und welche Konfiguration zu verwenden ist. Mit ihm an Ort und Stelle wird die Zusammenstellung von Terminal geradeaus. Wählen Sie zunächst die entsprechende `pysource`-Datei aus und verifizieren Sie dann das Setup mit `config.py`:

```bash
cd /home/HyInfo/opt/telemac-mascaret/configs    # adjust this path to your install
source pysource.mint22.sh                       # or: source pysource.debian12.sh
config.py
```

Mit den Skripten `pysource.mint22.sh` oder `pysource.debian12.sh` sollten Sie die TELEMAC-Pfade und den Konfigurationsnamen ansprechen. Laufen `config.py` sollte das ASCII-Banner anzeigen und mit `My work is done` beenden. Wenn nicht, lesen Sie die Fehlerausgabe sorgfältig; typische Ursachen sind typos in Pfaden oder Dateinamen, oder Fehler innerhalb `pysource.x.sh` oder Ihr `systel.*.cfg`.


```{admonition} Quick health checks after sourcing
:class: tip

* `mpifort -show` sollte eine `gfortran`-Befehlszeile mit MPI`-I` und `-L`-Flags injiziert drucken. Dies verifiziert Wrapper-Compiler sind vorhanden.
* Wenn Sie die parallele HDF5 in Ihrem `.cfg` aktiviert haben, sollte `h5pfc -show` erfolgreich sein und `.../hdf5/openmpi` in seinen Fahnen anzeigen. Wenn es fehlt, installieren Sie `libhdf5-openmpi-dev`.
* Running `telemac.py` or `compile.py` without a full path should work because `scripts/python3` and `scripts/unix` are on `PATH`. The TELEMAC Linux install notes follow this approach.
```

Nachdem `config.py` erfolgreich abgeschlossen ist, compile TELEMAC. Verwenden Sie die `--clean`-Flag, um alle Artefakte aus früheren Builds zu entfernen und Konflikte zu vermeiden:

```bash
compile_telemac.py --clean
```

Der Build wird eine Weile laufen und sollte mit der Nachricht `My work is done` beenden. Wenn es mit Fehlern aufhört, scrollen Sie bis zum ersten Fehler und fixieren Sie das gemeldete Problem, bevor Sie den Befehl erneut ausführen.

```{admonition} How to troubleshoot errors in the compiling process
:class: attention

Wenn die Zusammenstellung ausfällt, lesen Sie den Rückblick sorgfältig und identifizieren Sie die genaue Komponente, die brach. Überprüfen Sie die Setup-Schritte für diese Komponente und überprüfen Sie Pfade, Bibliotheksnamen, Umgebungsvariablen und Datei-Editionen gegen diese Anleitung. **Erfinden Sie das Rad nicht neu:* Die meisten Fehler kommen aus kleinen Typos oder falsch abgestimmten Versionen in Dateien, die Sie selbst erstellt haben. Fehlerbehebungen können frustrierend sein, also Ihre eigenen Annahmen herausfordern, den ersten Fehler im Log beheben und dann aus einem sauberen Zustand wieder aufbauen.
```

(testrun)=
### Prüfung TELEMAC

** Geschätzte Dauer: 5-10 Minuten.***


Nach dem Schließen des Terminals oder auf einem neuen Systemstart werden Sie die TELEMAC-Umgebung neu laden, bevor Sie es ausführen:

```bash
cd ~/opt/telemac-mascaret/configs    # adjust if you installed elsewhere
source pysource.mint22.sh            # or: source pysource.debian12.sh
```

Führen Sie einen vordefinierten Fall aus dem Ordner `examples` aus:

```bash
cd ~/opt/telemac-mascaret/examples/telemac2d/gouttedo
telemac2d.py t2d_gouttedo.cas
```

```{admonition} Examples not working?
:class: error, dropdown

Keine Panik. Wenn `config.py` erfolgreich ist und der Build mit "Meine Arbeit ist erledigt", ist Ihre Installation in der Regel gut. Die meisten Beispiel Fehler kommen aus Umweltproblemen oder fehlende große Dateien. Stellen Sie sicher, dass Sie die korrekte `pysource.*.sh`, installiert alle Git-Anforderungen ** einschließlich Git LFS, überprüft die richtige Version, ** und zog das vollständige Repository. Bei Bedarf aktivierte und recompile TELEMAC, ab der {ref}`git section <tm-git-requirements>`.
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

```{admonition} Cannot find <<PARTEL.PAR>>?
:class: error, dropdown
Wenn Sie `Cannot find << PARTEL.PAR >>` oder `TypeError: can only concatenate str (not ...) to str` sehen, stellen Sie sicher, dass `par_cmdexec` aus Ihrer Konfigurationsdatei entfernt wird.
```

Während die Berechnung läuft, sehen Sie die Gesamt-CPU-Nutzung. Wenn mehrere Kerne eine anhaltende Aktivität in unterschiedlichen Prozenten zeigen, funktioniert der Parallellauf.

TELEMAC sollte das Beispiel starten und mit `My work is done` beenden. Um Effizienz zu messen, variieren `--ncsize`. So läuft beispielsweise auf einem modernen Laptop der `donau` Fall oft in ca. 1 Minute mit `--ncsize=4` und ca. 2-3 Minuten mit `--ncsize=2`; genaue Timings hängen von Hardware, Maschengröße und I/O. **Scaling ist nicht linear* aufgrund von Domänen-Partition-Overhead, Speicherbandbreiten und Hyperthreading, so dass das Starten mehrerer kleinerer Jobs auf weniger Kerne effizienter als ein Job auf vielen Kernen sein kann.

````{admonition} Troubleshoot 'No such file or directory'
:class: attention, dropdown
Wenn Sie die Terminal-Session unterbrochen haben und `No such file or directory` sehen, laden Sie die TELEMAC-Umgebung erneut ein, bevor Sie Beispiele wiederholen:

```bash
cd ~/opt/telemac-mascaret/configs
source pysource.mint22.sh      # or: source pysource.debian12.sh
config.py
```

Dann kehren Sie in den `examples`-Ordner zurück und führen Sie den Fall erneut aus.
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


(install-telemac-utilities)=
## Utilities (Vor- und Nachbearbeitung)

```{admonition} More Pre- and Post-processing Software
:class: note

Mehr Software zum Umgang mit TELEMAC Vor- und Nachbearbeitung ist in Form von {ref}`SALOME <salome-install>` und ParaView erhältlich.
```

(qgis-telemac)=
### QGIS und das Q4TS Plugin (Linux und Windows)

** Geschätzte Dauer: 5-10 Minuten (abhängig von Verbindungsgeschwindigkeit).****

QGIS ist ein leistungsstarkes Tool zum Betrachten, Erstellen und Bearbeiten von geospatialen Daten und ist sowohl für die Vor- als auch Nachbearbeitung nützlich. Die Installationsanleitung erscheint in den {ref}`qgis-install`Anweisungen und der {ref}`QGIS tutorial <qgis-tutorial>` in diesem eBook. Das **Q4TS** Plugin unterstützt die Vorbereitung und Nachbearbeitung von Dateien für TELEMAC und kann mit {ref}`SALOME <salome-install>` an TELEMAC von einer GUI angeschlossen werden.

To install Q4TS, follow the developers’ instructions at [https://gitlab.pam-retd.fr/otm/q4ts](https://gitlab.pam-retd.fr/otm/q4ts):

* In QGIS öffnen Sie den **Plugin Manager** (Plugins > Plugins verwalten und installieren...).
* Gehen Sie zu **Einstellungen****Add...*, setzen Sie die URL auf `https://otm.gitlab-pages.pam-retd.fr/q4ts/plugins.xml`, wählen Sie einen **Name** (z.B. `q4ts`) und lassen Sie die anderen Felder unverändert. Klicken Sie auf **OK**.
* Klicken Sie auf **Reload aller Repositories**.
* In der Registerkarte **All** suchen Sie nach `Q4TS` und installieren Sie das Plugin.

```{admonition} Plugin not found?
:class: warning, dropdown

Q4TS requires QGIS 3.26 or newer. If your QGIS is older, the Plugin Manager will not list it. The reliable fix is to upgrade QGIS. As a temporary workaround, you can download the ZIP from [https://otm.gitlab-pages.pam-retd.fr/q4ts/q4ts.0.7.0.zip](https://otm.gitlab-pages.pam-retd.fr/q4ts/q4ts.0.7.0.zip) and use **Install from ZIP**, but upgrading QGIS is highly recommended.
```

Nach der Installation fügt Q4TS Tools in der QGIS Processing Toolbox für MED -- SLF-Konvertierung, Netzveredelung, Grenzerstellung, Friktionstabellenbearbeitung und mehr hinzu. Grundlegendes Dienstprogramm für die Nachbearbeitung wird in der `steady-flow simulation tutorial <tm-use-q4ts>` mit Telemac2d beschrieben.

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
```{figure} ../img/telemac/conf-windows.png
:alt: configure Q4TS on Windows
:name: q4ts-windows

Die Konfiguration des Q4TS unter Windows (Bildquelle: [gitlab.pam-retd.fr/otm/q4ts](https://gitlab.pam-retd.fr/otm/q4ts)). Um diese Pfade in QGIS einzustellen, gehen Sie zu **Einstellungen** (Top-Menü) > * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```
````
`````

```{admonition} Other (stale) plugins
:class: note, dropdown

Ältere, teilweise nicht arbeitende TELEMAC-bezogene Plugins für QGIS beinhalten:

* [Telemac Tools](https://plugins.qgis.org/plugins/telemac_tools/), ein experimenteller Netzgenerator für `*.slf`Dateien, entwickelt von *Artelia*. In QGIS aktivieren Sie **experimentelle Plugins** im Plugin Manager **Einstellungen** vor der Suche.
* {ref}`BASEmesh <get-basemesh>`, die ein {term}`SMS 2dm`Netz erstellen kann, das Sie für TELEMAC in eine SELAFIN-Geometrie umwandeln können (siehe {ref}`QGIS pre-processing tutorial for TELEMAC <tm-qgis-prepro>`).
* *PostTelemac*, das `*.slf` und damit verbundene Ergebnisformate (z.B. `*.res`) im Laufe der Zeit visualisiert.
* *DEMto3D*, die *STL* Geometrie exportiert, die für den Einsatz in *SALOME* und für die Erstellung von 3D-Netzen geeignet ist.

Beachten Sie, dass *DEMto3D* unter dem **Raster**-Menü erscheint: **DEMto3D***** **Digitales Oberflächenmodell (DOM) 3D-Druck***. Diese Plugins können mit aktuellen QGIS-Versionen veraltet oder unvereinbar sein; bevorzugen Q4TS für aktiv gepflegte TELEMAC-Workflows, wenn möglich.
```

(artelia-mesh)=
### Artelia Mesh Werkzeuge

Artelia provides a Python-based analysis toolkit on GitHub: [https://github.com/Artelia/Mesh_tools](https://github.com/Artelia/Mesh_tools). Hydro-informatics.com has not yet tested Mesh Tools, but it appears promising for inspecting and analyzing existing meshes rather than generating new ones; see the related discussion in the [TELEMAC forum](https://www.opentelemac.org/index.php/kunena/qgis-for-otm/14662-meshtools).

Nach der Installation des Plugins über den QGIS Plugin Manager, zugreifen Sie es aus **Mesh** > **Mesh Tools*.


(bluekenue)=
### BlueKenue (Windows oder Linux+Wine)

** Geschätzte Dauer: 10 Minuten.**

[BlueKenue](https://nrc.canada.ca/en/research-development/products-services/software-applications/blue-kenuetm-software-tool-hydraulic-modellers)<sup>TM</sup> is a Windows-based pre- and post-processing tool from the [National Research Council Canada](https://nrc.canada.ca/en), which is designed for TELEMAC. It offers functionality similar to [Fudaa](http://www.opentelemac.org/index.php/latest-news-development-and-distribution/240-fudaa-mascaret-3-6) and includes a capable mesh generator, which is the main reason to install BlueKenue<sup>TM</sup>. Download the installer from the developer site: [https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (credentials are noted in the [Telemac Forum](http://www.opentelemac.org/index.php/assistance/forum5/blue-kenue)). Then choose the install method for your platform:

1. Unter Windows: führen Sie den BlueKenue `.msi` Installer direkt aus.
2. On Linux: use [Wine amd64](https://wiki.debian.org/Wine) through {ref}`PlayOnLinux <play-on-linux>` to install BlueKenue<sup>TM</sup>. For Ubuntu/Debian systems, see the {ref}`PlayOnLinux <play-on-linux>` section in this eBook. Installing with plain Wine only is discouraged due to common compatibility issues.

Typical BlueKenue<sup>TM</sup> executable locations are:

* 32-bit: `"C:\\Program Files (x86)\\CHC\\BlueKenue\\BlueKenue.exe"`
* 64-bit: `"C:\\Program Files\\CHC\\BlueKenue\\BlueKenue.exe"`

Weitere plattformübergreifende Beratungen finden Sie in der [CHyMS FAQ](https://chyms.nrc.gc.ca/docs/FAQ.html), insbesondere in der Rubrik Blue Kenue auf [weitere Betriebssysteme](https://chyms.nrc.gc.ca/docs/FAQ.html#troubleshooting-how-run-on-another-os).


(fudaa)=
### Fudaa-PrePro (Linux und Windows)

*** Geschätzte Dauer: 5-15 Minuten (obere Zeitgrenze, falls Java installiert werden muss).***

Fudaa-PrePro ist ein Java-basiertes grafisches Frontend für das TELEMAC-System, das Ihnen hilft, Modelle durch die Definition von Maschen, Grenz- und Ausgangsbedingungen und Lenkung (`.cas`)-Dateien zu erstellen, und es kann auch Simulationen starten und die grundlegende Nachbearbeitung unterstützen. Es wird durch das Fudaa-Projekt gepflegt und mit Dokumentationen und Downloads auf ihrer Website verteilt, und es wird von den TELEMAC-Entwicklern als benutzerfreundlicher Vorprozessor zur Berechnung von Berechnungen referiert. Bereiten Sie sich mit der Vor- und Nachbearbeitungssoftware Fudaa-PrePro vor:

* *Java* installieren:
    + Auf Linux: `sudo apt install default-jdk` (die JRE alleine arbeitet für den Betrieb; die JDK ist sowohl für den Lauf als auch für die Werkzeuge sicher)
    + Unter Windows: Java von [java.com](https://java.com/)
* Laden Sie die neueste Version des [Fudaa-PrePro repository](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/237993985/Fudaa-Prepro+Downloads).
* Entpacken Sie die heruntergeladene Datei und fahren Sie je nach Plattform fort (siehe unten).
* `cd` in das Verzeichnis, in dem Sie die Fudaa-PrePro Programmdateien entpackt haben.
* Starten Sie Fudaa-PrePro von Terminal oder Command Prompt:
    + Auf *Linux*: lauf`sh supervisor.sh`
    + Auf *Windows*: laufen Sie `supervisor.bat`

Wenn Sie einen Fehler wie:

```bash
Error: Could not find or load main class org.fudaa.fudaa.tr.TrSupervisor
```
Bearbeiten Sie `supervisor.sh` und ersetzen Sie `$PWD Fudaa` mit `$(pwd)/Fudaa`, so dass der Klassenpfad richtig entscheidet. Sie können die Standard-RAM-Einstellung auch unter `supervisor.sh` (oder `supervisor.bat`) einstellen. Fudaa-PrePro wird oft mit `-Xmx6144m` (≈6 GB) verschifft, für sehr große Maschen (Millionen Knoten) erhöht oder auf Low-RAM-Systemen reduziert. Setzen Sie `-Xmx` auf ein vernünftiges Vielfaches von 512 MB. Zum Beispiel, um 2 GB zu verwenden und den Klassenpfad zu beheben:

```bash
#!/bin/bash
cd "$(dirname "$0")"
java -Xmx2048m -Xms512m -cp "$(pwd)/Fudaa-Prepro-1.4.2-SNAPSHOT.jar" org.fudaa.fudaa.tr.TrSupervisor "$@"
```
