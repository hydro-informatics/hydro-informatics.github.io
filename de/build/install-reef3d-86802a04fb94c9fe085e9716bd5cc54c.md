---
description: Installationsanleitung für REEF3D Open-Source-CFD-Software auf Debian-basierten Linux-Systemen, die gcc-Compiler, OpenMPI, HYPRE, Eigene Abhängigkeiten und den DIVEMesh-Generator abdecken.
---

# REEF3D (Installation)

REEF3D steht im Vordergrund der Innovation in der Wasserressourcenforschung und Hydrauliktechnik und bietet fortschrittliche 3D-Modellierungsfunktionen, die es Ingenieuren ermöglichen, komplexe Wasserflüsse und sogar Sedimentdynamiken mit hoher Genauigkeit zu simulieren. Seine ausgeklügelten numerischen Algorithmen geben Einblicke in Küsten-, Fluss- und Estuarinenprozesse, insbesondere dort, wo Strömungs-Struktur-Interaktionen wichtig sind. REEF3D unterscheidet sich von ähnlichen proprietären Software wie FLOW-3D in seiner Open Source-Politik.

Below is an installation workflow for Debian-based Linux systems (incl. Ubuntu, Mint, Lubuntu, etc.) is adapted from section 4 of the official REEF3D documentation, available on GitHub at [https://github.com/REEF3D/REEF3D/](https://github.com/REEF3D/REEF3D/). The REEF3D mesh generator, DIVEMesh, can be installed following an analogous process. While the hydro-informatics.com eBook does not include REEF3D tutorials, the developers have produced a wide range of detailed and engaging tutorials, which can be explored on their website at [https://reef3d.wordpress.com](https://reef3d.wordpress.com/).

## Installieren Sie die Anforderungen

REEF3D hängt von gcc Compilern, OpenMPI, HYPRE und Eigen ab.

* gcc und g++ Compiler:

```
sudo apt install build-essential
```

* OpenMPI:

```
sudo apt install libopenmpi-dev openmpi-bin
```

* Eigen:

```
sudo apt install libeigen3-dev
```

* HYPRE:

```
sudo apt install libhypre-dev
```

## Installation von REEF3D auf Debian-basierten Linux-Systemen

### Erhalten Sie die neueste Version

Download the latest release from [https://github.com/REEF3D/REEF3D/releases/](https://github.com/REEF3D/REEF3D/releases/), unpack it, and `cd` into the folder (e.g., `REEF3D-25.02`).

### Stellen Sie die Makefile fest

Mit Eigen und HYPRE als Systempakete installiert, erfordert der Header der Makefile Anpassungen ab Linie 9:

```
# Point to the system installation paths, not /usr/local/hypre
HYPRE_DIR := /usr
EIGEN_DIR := ThirdParty/eigen-3.3.8 
CXXFLAGS  := -w -std=c++11 -O3 -DVERSION=\"$(GIT_VERSION)\" -DBRANCH=\"$(GIT_BRANCH)\"
# Use the system library location
LDFLAGS   := -L /usr/lib/x86_64-linux-gnu/ -lHYPRE
# Point INCLUDE to /usr/include/hypre
INCLUDE   := -I /usr/include/hypre -I $(EIGEN_DIR) -DEIGEN_MPL2_ONLY
SRC       := $(wildcard src/*.cpp)
OBJECTS   := $(SRC:%.cpp=$(OBJ_DIR)/%.o)
DEPENDENCIES := $(OBJECTS:.o=.d)
```

### Zusammenstellung

Um zu kompilieren eingeben:

```
make -j n
```

wobei n mindestens die Anzahl der verfügbaren Kerne ist.

