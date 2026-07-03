---
title: "Native Compilation of Delft3D-FLOW on Ubuntu and Linux Mint"
subtitle: "A Jupyter Book Usage Note for `install-delft3d-flow-native.sh`"
author: "Prepared for hydraulic-engineering computational workflows"
date: "2026-07-02"
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: "0.13"
    jupytext_version: "1.16"
kernelspec:
  display_name: Bash
  language: bash
  name: bash
---

# Delft3D-FLOW

This section describes a native installation procedure for compiling the Delft3D 4 hydrodynamic kernel on Ubuntu- and Linux Mint-based systems without using Docker. The procedure is implemented in the shell script `install-delft3d-flow-native.sh`. The script clones the Deltares Delft3D source repository, installs a local Python/Conan build environment, installs and configures Intel oneAPI compilers, initializes the open-source Conan dependency workflow, builds the Delft3D 4 suite or the `flow2d3d` target, copies the resulting installation tree to a user-defined prefix, and runs a smoke test with the standard Delft3D 4 example. The procedure should be regarded as an experimental host build because the documented Linux build procedure for Delft3D is container-based. The intended use is reproducible local experimentation, code inspection, and command-line execution of Delft3D-FLOW test cases on non-containerized engineering workstations.

```{warning}
This document describes a native build attempt. It does not supersede Deltares' official Linux build guidance. Deltares documents Linux compilation primarily through containerized environments, whereas this script attempts to reproduce the required toolchain directly on an Ubuntu- or Linux Mint-based host. Review the script before running it: it adds the Intel oneAPI APT repository, installs system packages with `sudo`, downloads and compiles third-party source code, and writes files below `$HOME`. Use it at your own risk and do not run it on production, shared, or institutional systems without authorization and backups.
```

## Get Ready

The Delft3D repository contains source code for both Delft3D 4 and Delft3D FM. Delft3D-FLOW is part of the Delft3D 4 suite, for which the relevant build configuration is `d3d4-suite`. Within that suite, the principal Delft3D-FLOW binaries are `d_hydro` and `flow2d3d`. The build system also exposes `flow2d3d` as an individual configuration; however, the suite-level configuration is the more conservative target for a first installation because it preserves the expected Delft3D 4 runtime context.

The script is intended for the following operating conditions:

- the user requires command-line Delft3D-FLOW execution on Linux;
- Docker or another container runtime is undesired;
- local compilation time (roughly one to several hours) and disk use (roughly 25 GB for oneAPI, sources, and build trees) are acceptable;
- the host is an Ubuntu- or Linux Mint-derived system with `apt`;
- Intel oneAPI compilers can be installed under `/opt/intel/oneapi`;
- the user accepts that the procedure is outside the principal tested Linux pathway described by Deltares.

The procedure is not intended to install or run the Windows Delft3D graphical user interface. It installs command-line kernels and runtime files only.

To continue, [download the installer script `install-delft3d-flow-native.sh`](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/delft3d-installer/install-delft3d-flow-native.sh).

## Provenance of the Procedure

The script follows the repository-level build sequence used by Deltares' own helper tools. Third-party dependencies are managed with Conan 2, while `run_conan.py` performs one-time Conan configuration and `build.py` drives dependency installation, CMake configuration, compilation, and installation. For external users without access to the Deltares Nexus package server, the relevant initialization mode is:

```bash
python run_conan.py initialize external
```

The corresponding first-time build compiles all third-party dependencies locally:

```bash
python build.py --config d3d4-suite --build --build-type Release --build-dependencies
```

The native script automates these operations and adds the host-level preparation steps that would normally be supplied by the Deltares build container:

- It installs the Intel oneAPI toolchain pinned to the versions used by the Deltares container and Conan profile: C/C++ and Fortran compilers 2024.2, Intel MPI 2021.13, and MKL 2024.2. If these pinned packages disappear from the Intel repository, the script falls back to the latest versions and patches the Conan configuration to accept the detected compiler version.
- It creates a Python virtual environment inside the source tree with `conan ~= 2.29` and a current CMake, because the Delft3D build requires CMake 3.30 or newer, which Ubuntu 24.04 and Linux Mint 22 do not ship.
- It exports the compiler environment used inside the Deltares container (`CC=mpiicx`, `CXX=mpicxx`, `FC=mpiifx`) so that CMake configures Delft3D itself with the same toolchain as the Conan-built dependencies.

```{important}
The script deliberately keeps the Deltares Conan profile close to its upstream form and patches only the local Intel compiler paths and, if necessary, the compiler version. The upstream Linux profile is named for an AlmaLinux 8 and Intel oneAPI 2024 environment. Changing the distribution identity in the profile may alter Conan package identities and can reduce reproducibility.
```

## Installation

### File Placement

Place the script in a working directory where shell execution is permitted. The following layout is recommended:

```bash
mkdir -p "$HOME/src/delft3d-native-installer"
cd "$HOME/src/delft3d-native-installer"

# copy or move the script here
ls -l install-delft3d-flow-native.sh
```

Make the script executable:

```bash
chmod +x install-delft3d-flow-native.sh
```

### Default Installation

The default invocation builds the Delft3D 4 suite in release mode, copies the resulting installation tree to `$HOME/opt/delft3d-flow`, and runs the standard example as a smoke test:

```bash
./install-delft3d-flow-native.sh
```

The script asks for the `sudo` password when it installs system packages. The default values are summarized in {numref}`default-options`.

```{list-table} Default script options
:name: default-options
:header-rows: 1
:widths: 25 35 40

* - Option
  - Default
  - Function
* - `--src-dir`
  - `$HOME/src/delft3d`
  - Location of the cloned Delft3D source repository.
* - `--prefix`
  - `$HOME/opt/delft3d-flow`
  - Final installation/copy destination.
* - `--config`
  - `d3d4-suite`
  - Delft3D 4 suite build, including Delft3D-FLOW.
* - `--build-type`
  - `Release`
  - Optimized CMake build type.
* - `--jobs`
  - `nproc`
  - Parallel build level (`CMAKE_BUILD_PARALLEL_LEVEL` and `MAKEFLAGS`).
* - `--tag`
  - not set
  - Uses the default branch unless a branch, tag, or commit is specified.
* - `--no-test`
  - not set
  - Skips the smoke test with the standard example.
```

### Reproducible Installation

For hydraulic-engineering studies, the source revision should be fixed. A branch tip is not a reproducible model dependency. Use a release tag or commit hash where possible.

```bash
./install-delft3d-flow-native.sh \
  --tag <Delft3D-tag-or-commit> \
  --config d3d4-suite \
  --build-type Release \
  --prefix "$HOME/opt/delft3d-flow"
```

```{note}
Replace `<Delft3D-tag-or-commit>` with a tag or commit selected from the Deltares repository. The script does not prescribe a specific release because the appropriate revision depends on the user's model archive, validation case, or project requirements.
```

### Minimal FLOW-Oriented Build

If the objective is only to evaluate the `flow2d3d` build target, the script may be invoked as follows:

```bash
./install-delft3d-flow-native.sh --config flow2d3d
```

For first-time users, `d3d4-suite` remains the preferred trial because it is the suite-level target associated with Delft3D 4. The smaller `flow2d3d` target is more suitable after the host toolchain has already been shown to work.

### Skipping Package Installation

On managed university or institute workstations, the user may not want the script to change system packages. Two reduced modes are provided.

Skip only the Intel oneAPI installation step:

```bash
./install-delft3d-flow-native.sh --skip-oneapi-install
```

Skip all `apt` activity:

```bash
./install-delft3d-flow-native.sh --no-apt
```

These modes assume that the required compilers and build tools are already installed. In particular, the following commands must resolve after oneAPI initialization:

```bash
source /opt/intel/oneapi/setvars.sh --force
which icx icpx ifx mpiicx mpiifx mpicxx
```

If the preinstalled oneAPI version differs from 2024.2, the script patches the Conan profile and the allowed compiler versions automatically, but such a deviation moves the build further away from the Deltares baseline.

```{warning}
A reduced invocation is not a portable solution by itself. It merely prevents package-manager actions. If `git`, Python, the Intel C/C++ and Fortran compilers, or the Intel MPI wrappers are absent or not discoverable, the build will fail at the corresponding diagnostic check.
```

## Launch and Test Delft3D-FLOW

### Runtime Environment

After a successful build, the installation tree resides in the selected prefix (default `$HOME/opt/delft3d-flow`) and contains, among others, `bin/run_dflow2d3d.sh`, `bin/d_hydro`, and the `flow2d3d` shared libraries. The script writes an environment file to the prefix. Source this file in every new shell before running Delft3D-FLOW:

```bash
source "$HOME/opt/delft3d-flow/env.sh"
```

This command reinitializes the Intel oneAPI runtime, sets `DELFT3D_HOME`, and puts the Delft3D binaries and libraries on `PATH` and `LD_LIBRARY_PATH`.

### Test with the Standard Example

The installer already runs this test at the end of the build unless `--no-test` was given. To repeat it manually, use the standard Delft3D 4 example distributed with the repository (a tidal test case on the `f34` curvilinear grid):

```bash
source "$HOME/opt/delft3d-flow/env.sh"

cd "$HOME/src/delft3d/examples/delft3d4/01_standard"
run_dflow2d3d.sh
```

`run_dflow2d3d.sh` locates the installation relative to its own path and reads the model configuration file `config_d_hydro.xml` from the current working directory. The run takes seconds. Consider the test successful when all of the following hold:

1. The console output ends without error messages and the script returns exit code 0.
2. The history and map result files `trih-f34.dat`, `trih-f34.def`, `trim-f34.dat`, and `trim-f34.def` were written to the example directory.
3. The diagnostic file `tri-diag.f34` contains no lines with `*** ERROR`.

A quick check:

```bash
ls -l trih-f34.* trim-f34.*
grep -i error tri-diag.f34 || echo "no errors in tri-diag.f34"
```

A successful execution indicates that the binary, runtime libraries, and command-line launch script are mutually consistent on the host. It does not establish scientific validity for a project model. Hydrodynamic model validation remains case-specific and should include grid, bathymetry, boundary condition, roughness, process coupling, and calibration checks.

### Run Your Own Model

To run a project model, place the Delft3D-FLOW input files (for example `*.mdf`, grid, bathymetry, and boundary files) together with a `config_d_hydro.xml` configuration file in a working directory, then launch:

```bash
source "$HOME/opt/delft3d-flow/env.sh"

cd /path/to/my-model
run_dflow2d3d.sh                 # uses config_d_hydro.xml
run_dflow2d3d.sh my_config.xml   # or an explicit configuration file
```

The `config_d_hydro.xml` file from `examples/delft3d4/01_standard` serves as a template; adapt the `<mdfFile>` entry to the name of the project `.mdf` file. For parallel runs with Intel MPI, the installation also provides `run_dflow2d3d_parallel.sh`, which accepts the number of processes and otherwise follows the same conventions.

## Log Files

Each installer run writes a timestamped log file under:

```bash
$HOME/.cache/delft3d-native-build
```

If the build fails, inspect the final portion of the log:

```bash
tail -n 120 "$HOME/.cache/delft3d-native-build"/build-*.log
```

For a deterministic diagnostic record, copy the log into the model or software provenance folder:

```bash
mkdir -p provenance/software
cp "$HOME/.cache/delft3d-native-build"/build-*.log provenance/software/
```

## Common Failure Modes

```{list-table} Diagnostic interpretation
:name: diagnostics
:header-rows: 1
:widths: 25 35 40

* - Symptom
  - Probable cause
  - Corrective action
* - `ifx not found` or `mpiifx not found`
  - Intel oneAPI compiler or MPI packages are absent, or `setvars.sh` was not sourced.
  - Reinstall the oneAPI compiler and `intel-oneapi-mpi-devel` packages, or verify `/opt/intel/oneapi/setvars.sh`.
* - `CMake 3.30 or higher is required`
  - The system CMake shadows the virtual-environment CMake.
  - Rerun the script; it installs CMake into `$HOME/src/delft3d/.venv` and activates that environment itself.
* - Conan reports `Invalid setting` for `compiler.version`.
  - The installed oneAPI version is not whitelisted in `conan/config/settings_user.yml`.
  - Let the script patch the profile and settings, or install the pinned oneAPI 2024.2 packages.
* - Missing third-party package during Conan install.
  - External users must build dependencies locally.
  - Ensure the build command includes `--build-dependencies`; this is the script default.
* - CMake configure fails after dependency installation.
  - Host libraries or compiler configuration differ from the Deltares Linux container baseline.
  - Review the first CMake error, not only the final build summary.
* - `run_dflow2d3d.sh` starts but cannot load a shared library.
  - Runtime library path is incomplete.
  - Source `<prefix>/env.sh` and confirm `LD_LIBRARY_PATH` contains `<prefix>/lib`.
* - Build succeeds, but results differ from another workstation.
  - Source revision, compiler version, dependency build, or runtime configuration differs.
  - Record the Git revision, script log, oneAPI version, and model input files.
```

## Interpretation of Success

The installation should be considered successful when all of the following conditions are met:

1. `run_conan.py initialize external` completes without remote-credential errors.
2. `build.py` completes the CMake build and install stages.
3. The selected prefix contains `bin/run_dflow2d3d.sh`.
4. The standard Delft3D 4 example runs from a clean shell after `env.sh` is sourced and writes the `trih-f34.*` and `trim-f34.*` result files without errors in `tri-diag.f34`.
5. The build log, Git revision, and compiler versions are archived.

For computational hydraulics, binary availability is not equivalent to model validation. A defensible Delft3D-FLOW study should report the software revision, compiler environment, grid schematization, physical-process switches, boundary forcing, calibration data, and acceptance metrics.

## Uninstallation

The script installs files in user-space by default. To remove the resulting installation and build cache:

```bash
rm -rf "$HOME/opt/delft3d-flow"
rm -rf "$HOME/src/delft3d/build_d3d4-suite_release"
rm -rf "$HOME/src/delft3d/.venv"
rm -rf "$HOME/.conan2"
```

To remove the cloned source tree entirely:

```bash
rm -rf "$HOME/src/delft3d"
```

System packages installed by `apt`, including the Intel oneAPI packages and the Intel APT repository entry in `/etc/apt/sources.list.d/oneAPI.list`, are not removed automatically. This is intentional because compilers, CMake, Python, Git, and oneAPI components may be shared by other numerical models.

## Recommended Citation Record for Reports

A concise reproducibility statement may be included in project documentation:

> Delft3D-FLOW was compiled natively on an Ubuntu/Linux Mint host using `install-delft3d-flow-native.sh`. The script initialized the Delft3D external Conan workflow with Intel oneAPI 2024.2 compilers and Intel MPI 2021.13, built the `d3d4-suite` configuration in `Release` mode, and installed the command-line runtime under a user-space prefix. The Delft3D Git revision, Intel oneAPI compiler version, and build log were archived with the model provenance files.

## References

Deltares. 2026. "Compiling Delft3D on Linux." Delft3D GitHub repository documentation. https://github.com/Deltares/Delft3D/blob/main/doc/compiling_Linux.md

Deltares. 2026. "Getting started with code compilation and development." Delft3D GitHub repository documentation. https://github.com/Deltares/Delft3D/blob/main/doc/development.md

Deltares. 2026. "`build.py`." Delft3D GitHub repository. https://github.com/Deltares/Delft3D/blob/main/build.py

Deltares. 2026. "`delft3d_alma8_intel_2024` Conan profile." Delft3D GitHub repository. https://github.com/Deltares/Delft3D/blob/main/conan/config/profiles/delft3d_alma8_intel_2024

Deltares. 2026. "`buildtools.Dockerfile`." Delft3D GitHub repository. https://github.com/Deltares/Delft3D/blob/main/ci/dockerfiles/linux/buildtools.Dockerfile

Intel. 2026. "Install with APT." Intel oneAPI Toolkit Installation Guide for Linux. https://www.intel.com/content/www/us/en/docs/oneapi-toolkit/installation-guide-linux/latest/install-oneapi-toolkit-with-apt.html

Intel. 2024. "Use the setvars and oneapi-vars Scripts with Linux." Intel oneAPI Programming Guide. https://www.intel.com/content/www/us/en/docs/oneapi/programming-guide/2024-2/use-the-setvars-and-oneapi-vars-scripts-with-linux.html

MyST Markdown. 2026. "Callouts & Admonitions." https://mystmd.org/guide/admonitions

Jupyter Book. 2026. "MyST Markdown overview." https://jupyterbook.org/v1/content/myst.html
