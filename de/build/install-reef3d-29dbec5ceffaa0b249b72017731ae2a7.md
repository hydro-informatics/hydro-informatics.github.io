---
description: Installationsanleitung für REEF3D Open Source CFD Software und DIVEMesh auf Debian, Ubuntu, Linux Mint und verwandten Debian-basierten Linux Systemen.
---

# REEF3D (Installation)

REEF3D ist ein Open-Source-Hydrodynamik-Framework für freiflächige CFD-, Wellenmodellierung, nicht-hydrostatische Durchfluss- und Flachstromanwendungen. Es ist für hydraulische und küstentechnische Fälle von Bedeutung, in denen lokale 3D-Flows, hydraulische Strukturen, komplexe Badymetrie oder Sedimenttransporte wichtig sind.

Diese Seite beschreibt einen praktischen Workflow für Debian-basierte Linux-Systeme, darunter Debian, Ubuntu, Linux Mint, LMDE, Lubuntu und ähnliche Distributionen. Der untenstehende Workflow wurde gegen das aktuelle stromaufwärtige GitHub-Layout und Release-Informationen über **2026-06-26** geprüft. Upstream-Änderungen sind häufig, so behandeln Sie hart codierte Versionsnummern als Beispiele anstatt permanente Installationsanweisungen.

```{note}
Für Linux Mint 22.x folgen Sie dem Workflow im Ubuntu 24.04-Stil. Für LMDE folgen Sie dem Debian-Workflow. In beiden Fällen ist das eigentliche Problem in der Regel nicht das Betriebssystem, sondern die Makefile-Annahmen von REEF3D über den HYPRE-Installationspfad.
```

## Montageelemente

Ein typisches lokales Setup braucht zwei Ausführbare:

- `REEF3D`, der wichtigste Hydrodynamiklöser.
- `DiveMESH`, das mit REEF3D verwendete Mesh- und Geometrie-Präparationstool.

REEF3D wird mit MPI parallelisiert und baut derzeit mit `mpicxx`. DIVEMesh ein separates Repository und baut mit `g++`.


## Automatische Installation mit Hilfeskript

Für die meisten Debian-basierten Desktop- oder Workstation-Installationen ist die einfachste Route, das REEF3D-Helferskript zu verwenden, anstatt die unten stehenden manuellen Befehle auszuführen. Das Skript erkennt die Linux-Distribution, installiert die erforderlichen Systempakete, lädt die neuesten GitHub-Releases von DIVEMesh und REEF3D herunter, erstellt die bekannten Debian/Ubuntu/Mint Makefile-Pfadprobleme, erstellt beide Programme und erstellt optional einen Desktop-Starter.

### Die kurze Version

[Download the installer script `install_reef3d.sh`](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/reef3d-installer/install_reef3d.sh), then run:

```bash
chmod +x install_reef3d.sh
./install_reef3d.sh
```

Am Ende einer interaktiven Installation fragt das Skript, ob ein Desktop/Menu Launcher erstellt werden soll. Antwort `Y`, um es zu schaffen. Bei nicht interaktiven Systemen oder wenn die Antwort im Voraus festgelegt werden sollte, verwenden Sie:

```bash
REEF3D_CREATE_DESKTOP=1 ./install_reef3d.sh
```

Standardmäßig installiert das Skript REEF3D und DIVEMesh unter:

```bash
~/opt/reef3d
```

Es schafft auch symbolische Links in:

```bash
~/.local/bin
```

Nach der Installation überprüfen Sie, ob die Ausführbaren sichtbar sind:

```bash
which REEF3D
which DiveMESH
REEF3D || true
DiveMESH || true
```

Wenn `which REEF3D` oder `which DiveMESH` nichts zurückgibt, öffnen Sie ein neues Terminal oder fügen Sie `~/.local/bin` an die Shell`PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Anpassung

Ein benutzerdefiniertes Installationsverzeichnis kann mit `--prefix` ausgewählt werden:

```bash
./install_reef3d.sh --prefix "$HOME/software/reef3d"
```

Um die Anzahl der parallelen Compiler-Jobs zu steuern, verwenden Sie `-j` oder `--jobs`:

```bash
./install_reef3d.sh -j 8
```

Um einen sauberen Wiederaufbau zu zwingen, verwenden Sie:

```bash
./install_reef3d.sh --force
```

Um den Desktop Launcher explizit zu überspringen, verwenden Sie:

```bash
REEF3D_CREATE_DESKTOP=0 ./install_reef3d.sh
```

```{note}
Der Autoinstaller zielt absichtlich nur auf apt-basierte Debian-Systeme ab, darunter Debian, Ubuntu, Linux Mint, LMDE und Close-Derivate. Andere Linux-Distributionen können noch REEF3D ausführen, aber der Paket-Installationsteil des Skripts muss angepasst werden.
```

```{warning}
Das Skript lädt die neuesten Upstream-Versionen von GitHub herunter. Das ist praktisch für eine erste Installation, aber nicht ideal für reproduzierbare Anwendungen. So erfassen Sie für Fallstudien die installierten REEF3D- und DIVEMesh-Release-Tags, Compiler-Versionen, die OpenMPI-Version und die Betriebssystemversion in der Projektdokumentation.
```

In den folgenden Abschnitten wird beschrieben, was das Skript intern macht und für Fehlerbehebungen nützlich sind.



## Schritt für Schritt Installation

### Systempakete installieren

Aktualisieren Sie den Paketindex und installieren Sie die Build-Toolchain, MPI, HYPRE und Eigen:

```bash
sudo apt update
sudo apt install \
  build-essential gfortran git wget ca-certificates pkg-config dpkg-dev \
  libopenmpi-dev openmpi-bin \
  libhypre-dev libeigen3-dev
```

Optionale aber nützliche Pakete:

```bash
sudo apt install paraview htop tree
```

Überprüfen Sie, ob die wichtigen Werkzeuge sichtbar sind:

```bash
g++ --version
mpicxx --version
which mpicxx
mpirun --version
```

Überprüfen Sie, wo Debian/Ubuntu HYPRE und Eigen installiert hat:

```bash
dpkg -L libhypre-dev | grep -E 'HYPRE\.h|libHYPRE\.so'
dpkg -L libeigen3-dev | grep 'Eigen/Dense' | head
```

Auf Debian/Ubuntu/Mint-Systemen sind HYPRE-Header in der Regel unter `/usr/include/hypre`, während die Bibliothek normalerweise unter einem mehrjährigen Pfad wie `/usr/lib/x86_64-linux-gnu/` steht. Deshalb braucht die vorgeschaltete REEF3D Makefile oft eine lokale Pfadanpassung.

### Erhalten Sie den Quellcode

Verwenden Sie Git anstatt ein zufälliges Quellarchiv, wenn möglich. Die aktuelle REEF3D Makefile setzt Git-Verzweigung ein und verpflichtet Metadaten in den Build, so dass ein Git-Checkout verwirrende Versionsstrings vermeidet.

```bash
mkdir -p ~/src
cd ~/src

git clone https://github.com/REEF3D/REEF3D.git
git clone https://github.com/REEF3D/DIVEMesh.git
```

Verfügbare REEF3D-Versionen:

```bash
cd ~/src/REEF3D
git tag --sort=-v:refname | head
```

Für eine reproduzierbare Installation, überprüfen Sie ein bestimmtes Release-Tag statt zu bauen, was auf `master`:

```bash
# Example only. Replace with the release tag you want to use.
git checkout 26.05
```

```{warning}
Halten Sie alte Installationshinweise nicht auf, die z.B. `cd REEF3D-25.02` als ob das die neueste Version wäre. Verwenden Sie die GitHub Release-Seite oder `git tag --sort=-v:refname | head` und fügen Sie die Version explizit in Ihre Projekthinweise.
```

### Bauen Sie DIVEMesh

DIVEMesh ist von REEF3D getrennt und sollte zuerst gebaut werden:

```bash
cd ~/src/DIVEMesh
make clean
make -j"$(nproc)"
```

Die erwartete Ausführung ist:

```bash
ls -lh bin/DiveMESH
```

Wenn Sie die ausführbare verfügbare systemweite wünschen:

```bash
sudo install -m 755 bin/DiveMESH /usr/local/bin/DiveMESH
```

**DIVEMesh compiler-line fix*

Zum Zeitpunkt der Überprüfung enthielt die vorgeschaltete DIVEMesh Makefile:

```make
CXX := -g++
```

Das ist kein gültiger Compilerbefehl auf einer normalen Debian/Ubuntu/Mint Shell. Wenn Ihr Build mit einer Nachricht wie `-g++: command not found` ausfällt, fügen Sie die Zeile ein:

```bash
cd ~/src/DIVEMesh
sed -i 's/^CXX := -g++/CXX := g++/' Makefile
make clean
make -j"$(nproc)"
```

### REEF3D mit Debian/Ubuntu/Mint-Systempaketen erstellen

The current upstream REEF3D Makefile assumes HYPRE is installed under `/usr/local/hypre` and uses bundled Eigen from `ThirdParty/eigen-3.3.8`. Debian/Ubuntu/Mint packages install HYPRE elsewhere, so adjust the Makefile before compiling. Do **not** paste older Makefile snippets that set `CXXFLAGS` to `-std=c++11`; the current upstream Makefile uses `CXXFLAGS := -std=c++17 ...`.

Aus dem REEF3D Quellverzeichnis:

```bash
cd ~/src/REEF3D
cp Makefile Makefile.orig
```

Patchen Sie die HYPRE Pfade, während Sie die vorgeschaltete C++17-Einstellung beibehalten:

```bash
python3 - <<'PY'
from pathlib import Path

p = Path("Makefile")
s = p.read_text()

s = s.replace("HYPRE_DIR := /usr/local/hypre", "HYPRE_DIR := /usr")
s = s.replace(
    "LDFLAGS := -L ${HYPRE_DIR}/lib/ -lHYPRE",
    "LIBDIR := /usr/lib/$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)\nLDFLAGS := -L $(LIBDIR) -lHYPRE",
)
s = s.replace(
    "INCLUDE := -I ${HYPRE_DIR}/include -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY",
    "INCLUDE := -I /usr/include/hypre -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY",
)

p.write_text(s)
PY
```

Dann kompilieren:

```bash
make clean
make release -j"$(nproc)"
```

Die erwartete Ausführung ist:

```bash
ls -lh bin/REEF3D
```

Fügen Sie für eine User-Local-Installation beide ausführbaren Verzeichnisse zu Ihrem Shell-Pfad hinzu:

```bash
cat >> ~/.bashrc <<'EOF'

# REEF3D local build
export PATH="$HOME/src/REEF3D/bin:$HOME/src/DIVEMesh/bin:$PATH"
EOF

source ~/.bashrc
```

Dann überprüfen Sie:

```bash
which REEF3D
which DiveMESH
```

### Alternative: HYPRE manuell unter `/usr/local/hypre`

Die vorgeschaltete Dockerfile baut OpenMPI und HYPRE aus der Quelle und installiert HYPRE unter `/usr/local/hypre`. Das entspricht REEF3Ds Standard Makefile enger, aber es ist invasiver auf einer Workstation.

Verwenden Sie die manuelle `/usr/local/hypre`route nur, wenn Sie eine bestimmte HYPRE-Version benötigen oder wenn das Distributionspaket Lösungsprobleme verursacht. Für normale Debian-, Ubuntu- und Mint-Workstations bevorzugen Sie zunächst `libhypre-dev`.

### Prüfverfahren

Bevor Sie ein Projekt einrichten, führen Sie im REEF3D `Tutorials`-Verzeichnis einen kleinen Upstream-Tutorial- oder Beispielfall aus:

```bash
cd ~/src/REEF3D/Tutorials
find . -maxdepth 2 -type f | head
```

Folgen Sie den Anweisungen, die mit dem ausgewählten Tutorial ausgeliefert werden. Beginnen Sie nicht, Ihre eigene STL-Geometrie, Badymetrie, Turbulenzeinstellungen und Randbedingungen zu debuggen, bevor Sie bestätigen, dass die Binärfunktion auf einem kleinen vorgelagerten Fall funktioniert.

### MPI Laufnoten

Für parallele Laufzeiten verwenden Sie `mpirun` oder `mpiexec` nach dem Tutorial oder Fall-Setup:

```bash
mpirun -np 4 REEF3D
```

Führen Sie keine MPI-Jobs mit `sudo`. OpenMPI blockiert standardmäßig die Root-Ausführung aus einem Grund. Die vorgelagerten Dockerfile-Sets `OMPI_ALLOW_RUN_AS_ROOT` Variablen, weil Container oft als root ausgeführt werden; dass Workaround in Containern gehört, nicht an normalen Workstations.

## Fehlerbehebung

### `mpicxx: command not found`

Installiere OpenMPI-Entwicklungspakete:

```bash
sudo apt install libopenmpi-dev openmpi-bin
which mpicxx
```

### `fatal error: HYPRE.h: No such file or directory`

Die HYPRE beinhalten Pfad ist falsch oder `libhypre-dev` fehlt.

```bash
sudo apt install libhypre-dev
dpkg -L libhypre-dev | grep HYPRE.h
```

Stellen Sie sicher, dass die REEF3D Makefile enthält:

```make
INCLUDE := -I /usr/include/hypre -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY
```

### `/usr/bin/ld: cannot find -lHYPRE`

Der Linker sucht nicht das Debian/Ubuntu-Multi-Architektur-Bibliotheksverzeichnis.

```bash
dpkg -L libhypre-dev | grep libHYPRE.so
dpkg-architecture -qDEB_HOST_MULTIARCH
```

Stellen Sie sicher, dass die REEF3D Makefile etwas entspricht:

```make
LIBDIR := /usr/lib/$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
LDFLAGS := -L $(LIBDIR) -lHYPRE
```

### `fatal error: Eigen/Dense: No such file or directory`

REEF3D zeigt normalerweise auf gebündeltes Eigen:

```make
EIGEN_DIR := ThirdParty/eigen-3.3.8
```

Wenn dieser Ordner fehlt, verwenden Sie stattdessen den System Eigen-Pfad:

```make
EIGEN_DIR := /usr/include/eigen3
```

Dann wieder aufbauen:

```bash
make clean
make release -j"$(nproc)"
```

### Erstellen Sie Fehler nach Äste oder Tags ändern

Löschen Sie das Build-Verzeichnis:

```bash
make clean
make release -j"$(nproc)"
```

Wenn das immer noch scheitert, wiederherstellen Sie das Original Makefile und reapply nur das HYPRE Pfad-Patch:

```bash
cp Makefile.orig Makefile
```

### Binary stürzt auf einem anderen Computer

Das vorgelagerte `release`-Ziel verwendet `-march=native`. Das kann Binaries erzeugen, die für die CPU optimiert wurden, auf der sie kompiliert wurden. Wenn Sie auf einer Maschine kompilieren und auf einer anderen laufen, bauen Sie mit dem weniger aggressiven Ziel:

```bash
make clean
make all -j"$(nproc)"
```

Alternativ bearbeiten Sie das `release`-Ziel und entfernen Sie `-march=native`, bevor Sie einen Cluster mit gemischten CPU-Generationen erstellen.

## Versionskontrolle / Aufnahme

Für die Reproduzierbarkeit erfassen Sie den genauen Zustand/Version:

```bash
cd ~/src/REEF3D
git rev-parse --short HEAD
git status --short
mpicxx --version
mpirun --version
ldconfig -p | grep HYPRE || true
```

Speichern Sie das REEF3D-Tag/Kompass, Betriebssystemversion, Compilerversion, MPI-Version und Makefile-Patch mit der Simulationsfalldokumentation.

## REEF3 Quellen

- REEF3D GitHub Repository: <https://github.com/REEF3D/REEF3D>
- REEF3D veröffentlicht: <https://github.com/REEF3D/REEF3D/releases>
- REEF3D vor Ort und Tutorials: <https://reef3d.wordpress.com/>
- DIVEMesh GitHub Repository: <https://github.com/REEF3D/DIVEMesh>
- Debian-Paketsuche: <https://packages.debian.org/>
