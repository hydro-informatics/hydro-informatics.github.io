---
description: Installation guide for REEF3D open-source CFD software and DIVEMesh on Debian, Ubuntu, Linux Mint, and related Debian-based Linux systems.
---

# REEF3D (Installation)

REEF3D is an open-source hydrodynamics framework for free-surface CFD, wave modelling, non-hydrostatic flow, and shallow-flow applications. It is relevant for hydraulic and coastal engineering cases where local 3D flow, hydraulic structures, complex bathymetry, or sediment transport are important.

This page describes a practical source-build workflow for Debian-based Linux systems, including Debian, Ubuntu, Linux Mint, LMDE, Lubuntu, and similar distributions. The workflow below was checked against the current upstream GitHub layout and release information on **2026-06-26**. Upstream changes are frequent, so treat hard-coded version numbers as examples rather than permanent installation instructions.

```{note}
For Linux Mint 22.x, follow the Ubuntu 24.04-style package workflow. For LMDE, follow the Debian workflow. In both cases, the real issue is usually not the operating system but REEF3D's Makefile assumptions about the HYPRE installation path.
```

## Installation elements

A typical local setup needs two executables:

- `REEF3D`, the main hydrodynamics solver.
- `DiveMESH`, the mesh and geometry-preparation tool used with REEF3D.

REEF3D is parallelized with MPI and currently builds with `mpicxx`. DIVEMesh is a separate repository and builds with `g++`.


## Automatic installation with a helper script

For most Debian-based desktop or workstation installations, the easiest route is to use the REEF3D helper script instead of running the manual commands below. The script detects the Linux distribution, installs the required system packages, downloads the latest GitHub releases of DIVEMesh and REEF3D, patches the known Debian/Ubuntu/Mint Makefile path issues, compiles both programs, and optionally creates a desktop launcher.

### The short version

[Download the installer script `install_reef3d.sh`](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/main/extra-reef3d-installer/install_reef3d.sh), then run:

```bash
chmod +x install_reef3d.sh
./install_reef3d.sh
```

At the end of an interactive installation, the script asks whether to create a desktop/menu launcher. Answer `Y` to create it. On non-interactive systems, or if the answer should be fixed in advance, use:

```bash
REEF3D_CREATE_DESKTOP=1 ./install_reef3d.sh
```

By default, the script installs REEF3D and DIVEMesh under:

```bash
~/opt/reef3d
```

It also creates symbolic links in:

```bash
~/.local/bin
```

After the installation, check that the executables are visible:

```bash
which REEF3D
which DiveMESH
REEF3D || true
DiveMESH || true
```

If `which REEF3D` or `which DiveMESH` returns nothing, open a new terminal or add `~/.local/bin` to the shell `PATH`:

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

To force a clean rebuild, use:

```bash
./install_reef3d.sh --force
```

To explicitly skip the desktop launcher, use:

```bash
REEF3D_CREATE_DESKTOP=0 ./install_reef3d.sh
```

```{note}
The autoinstaller intentionally targets apt-based Debian systems only, including Debian, Ubuntu, Linux Mint, LMDE, and close derivatives. Other Linux distributions can still run REEF3D, but the package-installation part of the script must be adapted.
```

```{warning}
The script downloads the latest upstream GitHub releases. That is convenient for a first installation, but not ideal for reproducible applications. So for case studies, record the installed REEF3D and DIVEMesh release tags, compiler versions, OpenMPI version, and operating-system version in the project documentation.
```

The following sections describe what the script does internally and are useful for troubleshooting failed builds.



## Step-by-step installation

### Install system packages

Update the package index and install the build toolchain, MPI, HYPRE, and Eigen:

```bash
sudo apt update
sudo apt install \
  build-essential gfortran git wget ca-certificates pkg-config dpkg-dev \
  libopenmpi-dev openmpi-bin \
  libhypre-dev libeigen3-dev
```

Optional but useful packages:

```bash
sudo apt install paraview htop tree
```

Check that the important tools are visible:

```bash
g++ --version
mpicxx --version
which mpicxx
mpirun --version
```

Check where Debian/Ubuntu installed HYPRE and Eigen:

```bash
dpkg -L libhypre-dev | grep -E 'HYPRE\.h|libHYPRE\.so'
dpkg -L libeigen3-dev | grep 'Eigen/Dense' | head
```

On Debian/Ubuntu/Mint systems, HYPRE headers are usually under `/usr/include/hypre`, while the library is normally under a multi-arch path such as `/usr/lib/x86_64-linux-gnu/`. This is why the upstream REEF3D Makefile often needs a local path adjustment.

### Get the source code

Use Git rather than a random source archive when possible. The current REEF3D Makefile inserts Git branch and commit metadata into the build, so a Git checkout avoids confusing version strings.

```bash
mkdir -p ~/src
cd ~/src

git clone https://github.com/REEF3D/REEF3D.git
git clone https://github.com/REEF3D/DIVEMesh.git
```

List available REEF3D versions:

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

### Build DIVEMesh

DIVEMesh is separate from REEF3D and should be built first:

```bash
cd ~/src/DIVEMesh
make clean
make -j"$(nproc)"
```

The expected executable is:

```bash
ls -lh bin/DiveMESH
```

If you want the executable available system-wide:

```bash
sudo install -m 755 bin/DiveMESH /usr/local/bin/DiveMESH
```

**DIVEMesh compiler-line fix**

At the time of checking, the upstream DIVEMesh Makefile contained:

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

### Build REEF3D with Debian/Ubuntu/Mint system packages

The current upstream REEF3D Makefile assumes HYPRE is installed under `/usr/local/hypre` and uses bundled Eigen from `ThirdParty/eigen-3.3.8`. Debian/Ubuntu/Mint packages install HYPRE elsewhere, so adjust the Makefile before compiling. Do **not** paste older Makefile snippets that set `CXXFLAGS` to `-std=c++11`; the current upstream Makefile uses `CXXFLAGS := -std=c++17 ...`.

From the REEF3D source directory:

```bash
cd ~/src/REEF3D
cp Makefile Makefile.orig
```

Patch the HYPRE paths while keeping the upstream C++17 setting:

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

Then compile:

```bash
make clean
make release -j"$(nproc)"
```

The expected executable is:

```bash
ls -lh bin/REEF3D
```

For a user-local installation, add both executable directories to your shell path:

```bash
cat >> ~/.bashrc <<'EOF'

# REEF3D local build
export PATH="$HOME/src/REEF3D/bin:$HOME/src/DIVEMesh/bin:$PATH"
EOF

source ~/.bashrc
```

Then check:

```bash
which REEF3D
which DiveMESH
```

### Alternative: build HYPRE manually under `/usr/local/hypre`

The upstream Dockerfile builds OpenMPI and HYPRE from source and installs HYPRE under `/usr/local/hypre`. That matches REEF3D's default Makefile more closely, but it is more invasive on a workstation.

Use the manual `/usr/local/hypre` route only when you need a specific HYPRE version or when the distribution package causes solver/linker problems. For normal Debian, Ubuntu, and Mint workstations, prefer `libhypre-dev` first.

### Test

Before setting up any project, run a small upstream tutorial or example case from the REEF3D `Tutorials` directory:

```bash
cd ~/src/REEF3D/Tutorials
find . -maxdepth 2 -type f | head
```

Follow the instructions shipped with the selected tutorial. Do not start debugging your own STL geometry, bathymetry, turbulence settings, and boundary conditions before confirming that the binary works on a small upstream case.

### MPI run notes

For parallel runs, use `mpirun` or `mpiexec` according to the tutorial or case setup:

```bash
mpirun -np 4 REEF3D
```

Do not run MPI jobs with `sudo`. OpenMPI blocks root execution by default for a reason. The upstream Dockerfile sets `OMPI_ALLOW_RUN_AS_ROOT` variables because containers often run as root; that workaround belongs in containers, not on normal workstations.

## Troubleshooting

### `mpicxx: command not found`

Install OpenMPI development packages:

```bash
sudo apt install libopenmpi-dev openmpi-bin
which mpicxx
```

### `fatal error: HYPRE.h: No such file or directory`

The HYPRE include path is wrong or `libhypre-dev` is missing.

```bash
sudo apt install libhypre-dev
dpkg -L libhypre-dev | grep HYPRE.h
```

Make sure the REEF3D Makefile contains:

```make
INCLUDE := -I /usr/include/hypre -I ${EIGEN_DIR} -DEIGEN_MPL2_ONLY
```

### `/usr/bin/ld: cannot find -lHYPRE`

The linker is not searching the Debian/Ubuntu multi-arch library directory.

```bash
dpkg -L libhypre-dev | grep libHYPRE.so
dpkg-architecture -qDEB_HOST_MULTIARCH
```

Make sure the REEF3D Makefile contains something equivalent to:

```make
LIBDIR := /usr/lib/$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
LDFLAGS := -L $(LIBDIR) -lHYPRE
```

### `fatal error: Eigen/Dense: No such file or directory`

REEF3D normally points to bundled Eigen:

```make
EIGEN_DIR := ThirdParty/eigen-3.3.8
```

If that folder is missing, use the system Eigen path instead:

```make
EIGEN_DIR := /usr/include/eigen3
```

Then rebuild:

```bash
make clean
make release -j"$(nproc)"
```

### Build fails after changing branches or tags

Clean the build directory:

```bash
make clean
make release -j"$(nproc)"
```

If that still fails, restore the original Makefile and reapply only the HYPRE path patch:

```bash
cp Makefile.orig Makefile
```

### Binary crashes on another computer

The upstream `release` target uses `-march=native`. That can create binaries optimized for the CPU on which they were compiled. If you compile on one machine and run on another, build with the less aggressive target:

```bash
make clean
make all -j"$(nproc)"
```

Alternatively, edit the `release` target and remove `-march=native` before compiling for a cluster with mixed CPU generations.

## Version check / recording

For reproducibility, record the exact state/version:

```bash
cd ~/src/REEF3D
git rev-parse --short HEAD
git status --short
mpicxx --version
mpirun --version
ldconfig -p | grep HYPRE || true
```

Store the REEF3D tag/commit, operating system version, compiler version, MPI version, and Makefile patch with the simulation case documentation.

## REEF3D sources

- REEF3D GitHub repository: <https://github.com/REEF3D/REEF3D>
- REEF3D releases: <https://github.com/REEF3D/REEF3D/releases>
- REEF3D upstream site and tutorials: <https://reef3d.wordpress.com/>
- DIVEMesh GitHub repository: <https://github.com/REEF3D/DIVEMesh>
- Debian package search: <https://packages.debian.org/>
