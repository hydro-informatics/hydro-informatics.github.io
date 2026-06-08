---
description: Guide d'installation du logiciel CFD open-source REEF3D sur les systèmes Linux basés sur Debian, couvrant les compilateurs gcc, OpenMPI, HYPRE, les dépendances Eigen et le générateur DIVEMesh.
---

# REEF3D (Installation)

REEF3D est à l'avant-garde de l'innovation en recherche sur les ressources en eau et en génie hydraulique, offrant des capacités de modélisation 3d avancées qui permettent aux ingénieurs de simuler des débits d'eau complexes et même la dynamique des sédiments avec une grande précision. Ses algorithmes numériques sophistiqués donnent un aperçu des processus côtiers, fluviaux et estuariens, en particulier lorsque les interactions écoulement-structure sont importantes à considérer. REEF3D diffère de logiciels propriétaires similaires tels que FLOW-3D dans sa politique open source.

Below is an installation workflow for Debian-based Linux systems (incl. Ubuntu, Mint, Lubuntu, etc.) is adapted from section 4 of the official REEF3D documentation, available on GitHub at [https://github.com/REEF3D/REEF3D/](https://github.com/REEF3D/REEF3D/). The REEF3D mesh generator, DIVEMesh, can be installed following an analogous process. While the hydro-informatics.com eBook does not include REEF3D tutorials, the developers have produced a wide range of detailed and engaging tutorials, which can be explored on their website at [https://reef3d.wordpress.com](https://reef3d.wordpress.com/).

## Installer les exigences

REEF3D dépend des compilateurs gcc, OpenMPI, HYPRE et Eigen.

* compilateurs gcc et g++:

```
sudo apt install build-essential
```

* OpenMPI:

```
sudo apt install libopenmpi-dev openmpi-bin
```

* Eigen :

```
sudo apt install libeigen3-dev
```

* HYPRE:

```
sudo apt install libhypre-dev
```

## Installation de REEF3D sur les systèmes Linux basés sur Debian

### Obtenez la dernière version

Download the latest release from [https://github.com/REEF3D/REEF3D/releases/](https://github.com/REEF3D/REEF3D/releases/), unpack it, and `cd` into the folder (e.g., `REEF3D-25.02`).

### Correction du fichier Makefile

Avec Eigen et HYPRE installés comme paquets système, l'en-tête du Makefile nécessite des adaptations à partir de la ligne 9:

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

### Compilation

Pour compiler entrez :

```
make -j n
```

où n est au moins le nombre de cœurs disponibles.

