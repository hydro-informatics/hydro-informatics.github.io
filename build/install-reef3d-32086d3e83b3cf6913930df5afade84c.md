---
description: Installation guide for REEF3D open-source CFD software on Debian-based Linux systems, covering gcc compilers, OpenMPI, HYPRE, Eigen dependencies, and the DIVEMesh generator.
---

# REEF3D (Installation)

REEF3D is at the forefront of innovation in water resources research and hydraulic engineering, offering advanced 3d modeling capabilities that enable engineers to simulate complex water flows and even sediment dynamics with high accuracy. Its sophisticated numerical algorithms provide insight into coastal, riverine, and estuarine processes, especially where flow-structure interactions are important to consider. REEF3D differs from similar proprietary software such as FLOW-3D in its open source policy.

Below is an installation workflow for Debian-based Linux systems (incl. Ubuntu, Mint, Lubuntu, etc.) is adapted from section 4 of the official REEF3D documentation, available on GitHub at [https://github.com/REEF3D/REEF3D/](https://github.com/REEF3D/REEF3D/). The REEF3D mesh generator, DIVEMesh, can be installed following an analogous process. While the hydro-informatics.com eBook does not include REEF3D tutorials, the developers have produced a wide range of detailed and engaging tutorials, which can be explored on their website at [https://reef3d.wordpress.com](https://reef3d.wordpress.com/).

## Install the requirements

REEF3D depends on gcc compilers, OpenMPI, HYPRE and Eigen.

* gcc and g++ compilers:

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

## Installation of REEF3D on Debian-based Linux systems

### Get the latest version

Download the latest release from [https://github.com/REEF3D/REEF3D/releases/](https://github.com/REEF3D/REEF3D/releases/), unpack it, and `cd` into the folder (e.g., `REEF3D-25.02`).

### Fix the Makefile

With Eigen and HYPRE installed as system packages, the header of the Makefile requires adaptions starting from line 9:

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

### Compiling

To compile enter:

```
make -j n
```

where n is at least the number of available cores.

