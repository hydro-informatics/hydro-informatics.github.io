---
description: Installationsanleitung für REEF3D Open Source CFD Software und DIVEMesh auf Debian, Ubuntu, Linux Mint und verwandten Debian-basierten Linux Systemen.
---

# REEF3D (Installation)

REEF3D ist ein Open-Source-Hydrodynamik-Framework für CFD, Wellenmodellierung, nicht-hydrostatische Strömung und Flachströmungsanwendungen. Es ist relevant für hydraulische und küstentechnische Fälle, in denen lokale 3D-Flüsse, hydraulische Strukturen, komplexe Bathymetrie oder Sedimenttransport wichtig sind.

Diese Seite beschreibt einen praktischen Source-Build-Workflow für Debian-basierte Linux-Systeme, einschließlich Debian, Ubuntu, Linux Mint, LMDE, Lubuntu und ähnlichen Distributionen. Der folgende Workflow wurde mit dem aktuellen Upstream-GitHub-Layout und den Release-Informationen unter **2026-06-26** verglichen. Upstream-Änderungen sind häufig, also behandeln Sie fest codierte Versionsnummern als Beispiele und nicht als permanente Installationsanweisungen.

```{note}
Folgen Sie für Linux Mint 22.x dem Paket-Workflow im Ubuntu 24.04-Stil. Folgen Sie für LMDE dem Debian-Workflow. In beiden Fällen ist das eigentliche Problem normalerweise nicht das Betriebssystem, sondern die Makefile-Annahmen von REEF3D über den HYPRE-Installationspfad.
```

## Einbauelemente

Ein typisches lokales Setup benötigt zwei ausführbare Dateien:

- `REEF3D`, der wichtigste Hydrodynamik-Löser.
- `DiveMESH`, das Mesh- und Geometrie-Vorbereitungswerkzeug, das mit REEF3D verwendet wird.

REEF3D is parallelized with MPI and currently builds with `mpicxx`. DIVEMesh is a separate repository and builds with `g++`.


## Automatische Installation mit einem Helferskript

Für die meisten Debian-basierten Desktop- oder Workstation-Installationen besteht der einfachste Weg darin, das REEF3D-Helferskript zu verwenden, anstatt die folgenden manuellen Befehle auszuführen. Das Skript erkennt die Linux-Distribution, installiert die erforderlichen Systempakete, lädt die neuesten GitHub-Versionen von DIVEMesh und REEF3D herunter, patcht die bekannten Debian/Ubuntu/Mint Makefile-Pfadprobleme, kompiliert beide Programme und erstellt optional einen Desktop-Launcher.

### Die Kurzfassung

[Download the installer script `install_reef3d.sh`](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/reef3d-installer/install_reef3d.sh), then run:

```bash
chmod +x install_reef3d.sh
./install_reef3d.sh
```

At the end of an interactive installation, the script asks whether to create a desktop/menu launcher. Answer `Y` to create it. On non-interactive systems, or if the answer should be fixed in advance, use:

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

Überprüfen Sie nach der Installation, ob die ausführbaren Dateien sichtbar sind:

```bash
which REEF3D
which DiveMESH
REEF3D || true
DiveMESH || true
```

Wenn `which REEF3D` oder `which DiveMESH` nichts zurückgibt, öffnen Sie ein neues Terminal oder fügen Sie `~/.local/bin` zur Shell `PATH` hinzu:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Customization

A custom installation directory can be selected with `--prefix`:

```bash
./install_reef3d.sh --prefix "$HOME/software/reef3d"
```

To control the number of parallel compiler jobs, use `-j` or `--jobs`:

```bash
./install_reef3d.sh -j 8
```

Um einen sauberen Wiederaufbau zu erzwingen, verwenden Sie:

```bash
./install_reef3d.sh --force
```

Um den Desktop Launcher explizit zu überspringen, verwenden Sie:

```bash
REEF3D_CREATE_DESKTOP=0 ./install_reef3d.sh
```

```{note}
Der Autoinstaller zielt absichtlich nur auf apt-basierte Debian-Systeme ab, einschließlich Debian, Ubuntu, Linux Mint, LMDE und Close-Derivate. Andere Linux-Distributionen können immer noch REEF3D ausführen, aber der Teil der Paketinstallation des Skripts muss angepasst werden.
```

```{warning}
Das Skript lädt die neuesten Upstream-Versionen von GitHub herunter. Das ist bequem für eine erste Installation, aber nicht ideal für reproduzierbare Anwendungen. Für Fallstudien notieren Sie die installierten REEF3D- und DIVEMesh-Release-Tags, Compiler-Versionen, OpenMPI-Version und Betriebssystemversion in der Projektdokumentation.
```

Die folgenden Abschnitte beschreiben, was das Skript intern macht und sind nützlich für die Fehlerbehebung fehlgeschlagener Builds.



## Schrittweise Installation

### Systempakete installieren

Aktualisieren Sie den Paketindex und installieren Sie die Build-Toolchain, MPI, HYPRE und Eigen:

```bash
sudo apt update
sudo apt install \
  build-essential gfortran git wget ca-certificates pkg-config dpkg-dev \
  libopenmpi-dev openmpi-bin \
  libhypre-dev libeigen3-dev
```

Optionale, aber nützliche Pakete:

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

On Debian/Ubuntu/Mint systems, HYPRE headers are usually under `/usr/include/hypre`, while the library is normally under a multi-arch path such as `/usr/lib/x86_64-linux-gnu/`. This is why the upstream REEF3D Makefile often needs a local path adjustment.

### Holen Sie sich den Quellcode

Verwenden Sie Git anstelle eines zufälligen Quellarchivs, wenn möglich. Das aktuelle REEF3D Makefile fügt Git Branch ein und überträgt Metadaten in den Build, sodass ein Git Checkout verwirrende Versionszeichenfolgen vermeidet.

```bash
mkdir -p ~/src
cd ~/src

git clone https://github.com/REEF3D/REEF3D.git
git clone https://github.com/REEF3D/DIVEMesh.git
```

Liste der verfügbaren REEF3D-Versionen:

```bash
cd ~/src/REEF3D
git tag --sort=-v:refname | head
```

For a reproducible installation, check out a specific release tag instead of building whatever happens to be on `master`:

```bash
# Example only. Replace with the release tag you want to use.
git checkout 26.05
```

```{warning}
Do not keep old installation notes that say, for example, `cd REEF3D-25.02` as if that were the latest version. Use the GitHub release page or `git tag --sort=-v:refname | head` and pin the version explicitly in your project notes.
```

### Bauen Sie DIVEMesh

DIVEMesh ist getrennt von REEF3D und sollte zuerst gebaut werden:

```bash
cd ~/src/DIVEMesh
make clean
make -j"$(nproc)"
```

Die erwartete ausführbare Datei ist:

```bash
ls -lh bin/DiveMESH
```

Wenn Sie die ausführbare systemweit verfügbar:

```bash
sudo install -m 755 bin/DiveMESH /usr/local/bin/DiveMESH
```

**DIVEMesh Compilerline Fix**

Zum Zeitpunkt der Überprüfung enthielt das vorgelagerte DIVEMesh Makefile:

```make
CXX := -g++
```

That is not a valid compiler command on a normal Debian/Ubuntu/Mint shell. If your build fails with a message such as `-g++: command not found`, patch the line:

```bash
cd ~/src/DIVEMesh
sed -i 's/^CXX := -g++/CXX := g++/' Makefile
make clean
make -j"$(nproc)"
```

### REEF3D mit Debian/Ubuntu/Mint-Systempaketen erstellen

The current upstream REEF3D Makefile assumes HYPRE is installed under `/usr/local/hypre` and uses bundled Eigen from `ThirdParty/eigen-3.3.8`. Debian/Ubuntu/Mint packages install HYPRE elsewhere, so adjust the Makefile before compiling. Do **not** paste older Makefile snippets that set `CXXFLAGS` to `-std=c++11`; the current upstream Makefile uses `CXXFLAGS := -std=c++17 ...`.

Aus dem Quellenverzeichnis REEF3D:

```bash
cd ~/src/REEF3D
cp Makefile Makefile.orig
```

Patchen Sie die HYPRE-Pfade, während Sie die vorgelagerte C++17-Einstellung beibehalten:

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

Die erwartete ausführbare Datei ist:

```bash
ls -lh bin/REEF3D
```

Fügen Sie für eine benutzerseitige Installation beide ausführbaren Verzeichnisse zu Ihrem Shell-Pfad hinzu:

```bash
cat >> ~/.bashrc <<'EOF'

# REEF3D local build
export PATH="$HOME/src/REEF3D/bin:$HOME/src/DIVEMesh/bin:$PATH"
EOF

source ~/.bashrc
```

Dann überprüfen:

```bash
which REEF3D
which DiveMESH
```

### Alternative: build HYPRE manually under `/usr/local/hypre`

Die vorgelagerte Dockerfile baut OpenMPI und HYPRE von der Quelle und installiert HYPRE unter `/usr/local/hypre`. Das entspricht dem Standard-Makefile von REEF3D genauer, ist aber auf einer Workstation invasiver.

Use the manual `/usr/local/hypre` route only when you need a specific HYPRE version or when the distribution package causes solver/linker problems. For normal Debian, Ubuntu, and Mint workstations, prefer `libhypre-dev` first.

### Test

Before setting up any project, run a small upstream tutorial or example case from the REEF3D `Tutorials` directory:

```bash
cd ~/src/REEF3D/Tutorials
find . -maxdepth 2 -type f | head
```

Befolgen Sie die Anweisungen, die mit dem ausgewählten Tutorial gesendet wurden. Beginnen Sie nicht mit dem Debuggen Ihrer eigenen STL-Geometrie, Bathymetrie, Turbulenzeinstellungen und Randbedingungen, bevor Sie bestätigen, dass die Binärdatei in einem kleinen Upstream-Fall funktioniert.

### Laufende MPI-Anleihen

Verwenden Sie für parallele Läufe `mpirun` oder `mpiexec` entsprechend dem Tutorial oder dem Fall-Setup:

```bash
mpirun -np 4 REEF3D
```

Do not run MPI jobs with `sudo`. OpenMPI blocks root execution by default for a reason. The upstream Dockerfile sets `OMPI_ALLOW_RUN_AS_ROOT` variables because containers often run as root; that workaround belongs in containers, not on normal workstations.

## Fehlerbehebung

### `mpicxx: command not found`

Installieren Sie OpenMPI-Entwicklungspakete:

```bash
sudo apt install libopenmpi-dev openmpi-bin
which mpicxx
```

### `fatal error: HYPRE.h: No such file or directory`

Der HYPRE-Include-Pfad ist falsch oder `libhypre-dev` fehlt.

```bash
sudo apt install libhypre-dev
dpkg -L libhypre-dev | grep HYPRE.h
```

Stellen Sie sicher, dass das REEF3D Makefile enthält:

```make
INCLUDE := -I /usr/include/hypre -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY
```

### `/usr/bin/ld: cannot find -lHYPRE`

Der Linker durchsucht nicht das Debian/Ubuntu Multi-Bogen-Bibliotheksverzeichnis.

```bash
dpkg -L libhypre-dev | grep libHYPRE.so
dpkg-architecture -qDEB_HOST_MULTIARCH
```

Stellen Sie sicher, dass das REEF3D Makefile etwas Entspricht:

```make
LIBDIR := /usr/lib/$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
LDFLAGS := -L $(LIBDIR) -lHYPRE
```

### `fatal error: Eigen/Dense: No such file or directory`

REEF3D weist normalerweise auf gebündeltes Eigen hin:

```make
EIGEN_DIR := ThirdParty/eigen-3.3.8
```

Wenn dieser Ordner fehlt, verwenden Sie stattdessen den systemeigenen Pfad:

```make
EIGEN_DIR := /usr/include/eigen3
```

Dann wieder aufbauen:

```bash
make clean
make release -j"$(nproc)"
```

### Build schlägt fehl, nachdem Branchs oder Tags geändert wurden

Reinigen Sie das Build-Verzeichnis:

```bash
make clean
make release -j"$(nproc)"
```

Wenn das immer noch fehlschlägt, stellen Sie das ursprüngliche Makefile wieder her und wenden Sie nur den HYPRE-Pfad-Patch erneut an:

```bash
cp Makefile.orig Makefile
```

### Binäre Abstürze auf einem anderen Computer

The upstream `release` target uses `-march=native`. That can create binaries optimized for the CPU on which they were compiled. If you compile on one machine and run on another, build with the less aggressive target:

```bash
make clean
make all -j"$(nproc)"
```

Alternatively, edit the `release` target and remove `-march=native` before compiling for a cluster with mixed CPU generations.

## Versionsprüfung/Aufzeichnung

Zur Reproduzierbarkeit notieren Sie den genauen Zustand/Version:

```bash
cd ~/src/REEF3D
git rev-parse --short HEAD
git status --short
mpicxx --version
mpirun --version
ldconfig -p | grep HYPRE || true
```

Speichern Sie den REEF3D-Tag/Commit, die Betriebssystemversion, die Compilerversion, die MPI-Version und den Makefile-Patch mit der Simulationsfalldokumentation.

## REEF3D-Quellen

- REEF3D GitHub Repository: <https://github.com/REEF3D/REEF3D>
- REEF3D Releases: <https://github.com/REEF3D/REEF3D/releases>
- REEF3D Upstream-Site und Tutorials: <https://reef3d.wordpress.com/>
- DIVEMesh GitHub Repository: <https://github.com/REEF3D/DIVEMesh>
- Debian-Paketsuche: <https://packages.debian.org/>
