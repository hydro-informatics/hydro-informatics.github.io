---
description: Installation of OpenCFD OpenFOAM v2406, Olsen sediment solvers, BAW outlet boundary conditions, ParaView, and VisIt on Debian, Ubuntu, and Windows through WSL2.
---

(openfoam-install)=
# OpenFOAM (Installation)

This section explains the installation of [OpenCFD OpenFOAM v2406](https://dl.openfoam.com/source/v2406/) with a cross-platform auto-installer script that compiles the program alongside sediment-transport and outlet-boundary components as well as ParaView and VisIt-DAV for post-processing.

| Component | Function |
| :--- | :--- |
| `sediDriftFoam` | Olsen et al. (2023) fixed-mesh suspended-sediment solver. |
| `sediDriftFoam2` | Olsen (2025) sediment solver with bed-elevation and free-surface adjustment. |
| `sediDriftFoam2Rating` | New experimental extension of `sediDriftFoam2` for a stage–discharge relation. |
| BAW `HydBCsForOF` | Boundary-condition library, including a stage–discharge outlet for water–air simulations with `interFoam`. |

The original solvers are documented by [Nils Reidar Olsen](https://www.pvv.ntnu.no/~nilsol/sediDriftFoam2/); the native outlet boundary condition is documented in [BAW's repository](https://github.com/baw-de/HydBCsForOF).

```{admonition} OpenFOAM Distribution
:class: important

These instructions target the OpenCFD release v2406, not OpenFOAM Foundation releases (e.g., v9 or v13). The default installation compiles the June 2024 source release and matching ThirdParty sources in a separate user directory. Existing OpenFOAM installations and shell startup files are retained. Do not combine libraries compiled against different OpenFOAM distributions or versions.
```

## Requirements and Installer Files

The installer supports x86-64 systems running Debian 12, Ubuntu 22.04, or Ubuntu 24.04. Derivatives must use a corresponding supported base distribution. Windows builds run in Windows Subsystem for Linux 2 (WSL2), not as native Windows executables.

Installation requires a good and stable Internet connection, Python 3.10 or later, and a user account with `sudo` access for system packages. Allow approximately 20 GiB of free disk space and at least 8 GiB of RAM; the source-build check requires at least 15 GiB free. Compiling may take several hours. Graphical post-processing requires a Linux desktop or WSLg.

The installer is maintained in the [`OpenFOAM-installer` subfolder](https://github.com/Ecohydraulics/numerical-software-installers/tree/main/OpenFOAM-installer) of the `Ecohydraulics/numerical-software-installers` repository. With Git installed, clone the repository and enter that subfolder:

```bash
git clone --depth 1 https://github.com/Ecohydraulics/numerical-software-installers.git
cd numerical-software-installers/OpenFOAM-installer
```

These commands also work in PowerShell. For an existing checkout, enter its `OpenFOAM-installer` directory instead of cloning again. Alternatively, use **Code → Download ZIP** on the [repository page](https://github.com/Ecohydraulics/numerical-software-installers), extract the archive, and enter `numerical-software-installers-main/OpenFOAM-installer`.

Retain the complete installer subfolder; `install.py` alone is insufficient. The repository contains installer files, not the software distributions; these are downloaded during installation. Run the commands below from `OpenFOAM-installer`, which contains `install.py` and `install.ps1`.

(openfoam-debian)=
## Debian and Ubuntu

### Compile and Install

If Python is absent, install it first:

```bash
sudo apt update
sudo apt install python3
```

Preview the installation, then compile and install:

```bash
python3 install.py --dry-run
python3 install.py --install-system-packages --examples --smoke-test
```

Run the installer as the normal user, without prefixing it with `sudo`. The `--install-system-packages` option authorizes installation of build dependencies, graphical runtime dependencies, and ParaView through `sudo apt-get`. VisIt-DAV 3.5.0 is downloaded as a checksum-verified binary matched to the operating system. ParaView follows the version available from the configured distribution repositories.

```{admonition} APT Commands
:class: note

The installer uses `apt-get`, the backward-compatible interface recommended for scripts. The `apt` commands above are intended for interactive use. Neither interface is obsolete; see the [Debian APT manual](https://manpages.debian.org/bookworm/apt/apt.8.en.html#SCRIPT_USAGE_AND_DIFFERENCES_FROM_OTHER_APT_TOOLS).
```

The `--examples` option downloads Nils Reidar Olsen's coarse Case A. The `--smoke-test` option runs a short serial `interFoam` case to check the BAW library. A dry run prints the plan without checking prerequisites or compiling code.

```{admonition} Distribution Derivatives
:class: note

If a derivative is not recognized, verify its Debian or Ubuntu base before selecting `--visit-platform debian12`, `--visit-platform ubuntu22`, or `--visit-platform ubuntu24`. The override selects the VisIt binary; it does not establish compatibility with an unsupported operating system.
```

### Reuse an Existing OpenCFD v2406 Installation

Instead of compiling the OpenFOAM core, specify the existing v2406 activation file. For the Debian package installation at `/usr/lib/openfoam/openfoam2406`, use:

```bash
python3 install.py --install-system-packages \
  --reuse-openfoam /usr/lib/openfoam/openfoam2406/etc/bashrc \
  --examples --smoke-test
```

This is an alternative to the preceding source-build command. The sediment solvers and BAW library are still compiled into the new user directory. The existing installation must include development headers, `wmake`, and a working compiler. Its API must be 2406; its patch level may differ from the default source release.

## Windows through WSL2

In an administrator PowerShell, install Ubuntu 24.04 for WSL:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart Windows if requested. Launch Ubuntu once and create a normal Linux user account. Confirm that the distribution uses WSL2:

```powershell
wsl --list --verbose
```

If its version is 1, run `wsl --set-version Ubuntu-24.04 2`. WSLg supports graphical applications on Windows 11 and Windows 10 build 19044 or later; see the [Microsoft installation requirements](https://learn.microsoft.com/windows/wsl/tutorials/gui-apps).

From the repository's `OpenFOAM-installer` directory, use an ordinary PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -InstallSystemPackages -Examples -SmokeTest
```

The launcher invokes the same Python installer inside WSL2. The installer files may remain on the Windows filesystem, but compiling and cases should reside on the Linux filesystem, not under `/mnt/c`. ParaView and VisIt run as Linux applications displayed through WSLg.

For an initialized WSL distribution named `Debian` that runs Debian 12, add `-Distro Debian`. Check its release before installation; a newly downloaded Debian distribution need not be Debian 12. To reuse OpenCFD v2406, add `-ReuseOpenfoam` followed by its Linux `etc/bashrc` path.

## Installation Directory and Verification

The default installation directory is `~/.local/openfoam-sediment-v2406` in the Linux user's home directory. Specify another dedicated Linux path with `--prefix /home/USER/path` or Windows `-Prefix /home/USER/path`; the path must not contain whitespace. Limit compilation concurrency with `--jobs 4` or `-Jobs 4`, if required. The default is no more than eight compilation processes, reduced according to system RAM.

In a Linux or WSL terminal, enter the installed environment:

```bash
source ~/.local/openfoam-sediment-v2406/activate.sh
```

This command opens a new, isolated interactive shell. It does not modify `.bashrc` or merge an earlier OpenFOAM environment. Only project-level OpenFOAM preferences are loaded; existing user/group preferences are excluded. Enter `exit` to return to the previous shell. For a custom installation directory, use its `activate.sh` instead.

Check the installation in this new shell:

```bash
foamEtcFile -show-api
foamEtcFile -show-patch
printf '%s\n' "$WM_PROJECT_DIR" "$WM_OPTIONS"
command -v sediDriftFoam sediDriftFoam2 sediDriftFoam2Rating
sediDriftFoam -help
sediDriftFoam2 -help
sediDriftFoam2Rating -help
```

The API output must be `2406`. Solver help must load without missing-library errors. The installation directory contains compilation logs and `environment-probe.log` in `logs/`, build details in `build-environment.txt`, and source and installation records in `receipt.json`. The BAW runtime-test output is stored in `runs/baw-smoke/`.

```{admonition} Scope of Verification
:class: warning

Successful compilation and the BAW runtime test establish neither the validity of a sediment simulation nor the accuracy of the experimental rating-curve extension. The installer does not run Olsen's Case A. Before scientific use, verify mesh quality, conservation, hydraulic boundary conditions, and agreement with suitable reference results. Retain the build records with the simulation inputs.
```

If installation fails, inspect `logs/` before rerunning. Interrupted builds retain downloads and logs. Do not remove an existing OpenFOAM installation to resolve a version conflict. When changing source pins, installer code, or the compiler environment, select a new installation directory rather than mixing old and new binaries.

```{admonition} Archive Verification
:class: warning

A checksum mismatch indicates that the received bytes do not match the pinned archive; it does not, by itself, establish that the release changed. The downloader rejects partial and HTML responses and reports the expected and received SHA256 values, byte count, content type, and mirror path. Retain the complete error output if verification fails. Do not change the checksum or disable verification. Rejected temporary downloads are removed; verified archives are retained.
```

If the installation directory or its log is unexpectedly absent, locate the directory before rebuilding. A tree found in desktop Trash must be restored to its recorded original path, with no build active and no existing destination overwritten. Finding the tree in Trash does not establish when or why it moved. The supplied recovery instructions describe log inspection and restoration; do not compile within Trash.

````{admonition} Recovery from a Failed Installation
:class: note

Earlier installers rejected the valid Linux filename `jouleHeatingSource:V` or failed during environment loading with `/bin/bash: cannot execute binary file` or `pop_var_context`. The corrected loader isolates command arguments and suspends strict shell modes during OpenFOAM initialization, then checks the selected project, API, and ABI before compilation. Preserve the failed directory and select a new installation prefix; do not bypass its ownership marker. Retry without requiring a previous cache:

```bash
python3 install.py --install-system-packages \
  --prefix "$HOME/.local/openfoam-sediment-v2406-initfix" \
  --examples --smoke-test
```

The installer downloads and verifies archives in the new prefix. Cache reuse is optional: use `--source-cache` only with a verified existing directory. An `Archive cache directory not found` error precedes changes to the target prefix or system packages; omit that option and retry with the same prefix. On Windows, use `-Prefix` with a Linux path. After success, activate the new prefix's `activate.sh`. Moving a user installation does not reverse APT package changes. The [recovery instructions](https://github.com/Ecohydraulics/numerical-software-installers/blob/main/OpenFOAM-installer/docs/RECOVERY.md) describe recoverable rollback and package-transaction review.
````

## Sediment Cases and Stage–Discharge Outlets

With `--examples`, the Olsen input files are stored in `cases/olsen-upstream/cylinder9_case_A/` under the installation directory. Work on a writable copy. Inspect the mesh before running the selected solver:

```bash
cd /path/to/case-copy
checkMesh -constant -allTopology -allGeometry
```

Resolve mesh errors before simulation. For the supplied Case A, invoke `sediDriftFoam2` explicitly from the case directory; the published `controlDict` may still name `simpleFoam`. The fixed-mesh `sediDriftFoam` requires a separately prepared compatible case because its sediment-dictionary entries differ. Run the Olsen solvers serially. The moving-bed mesh and output algorithms are not suitable for MPI decomposition. Both `sediDriftFoam2` and `sediDriftFoam2Rating` overwrite `scour.txt` on launch; archive it before restarting.

### BAW Outlet for interFoam

The installer prepares `cases/baw-interFoam/` and compiles the shared library `lib_BAW_public_BCs_v2412_20260813.so` against the selected v2406 installation. The `v2412` text is part of the upstream filename, not the build's OpenFOAM version. This library is loaded by the case through the `libs` entry in `system/controlDict`; it does not require recompiling `interFoam`.

For a site-specific rating curve, configure the paired `waterLevel_alpha_prgh` outlet entries in `p_rgh` and `alpha.water`, using the `ratingCurveTable` mode described in [BAW's documentation](https://github.com/baw-de/HydBCsForOF). Use the prepared case as a configuration example, not as calibrated hydraulic data.

### Experimental Outlet for Olsen's Moving-Bed Solver

In a disposable case copy, place the supplied `examples/ratingCurveProperties` file in `constant/ratingCurveProperties`. Replace the illustrative table with site-specific outward discharge in m³/s and water-surface elevation in m, expressed in the mesh's vertical datum. Discharge values must increase strictly, and elevations must not decrease. Set `outletPatch` to the actual outlet, check the depth and elevation limits, and change `enabled false` to `enabled true`. Run `sediDriftFoam2Rating` explicitly. Without this configuration, the extension is inactive.

```{admonition} Distinct Boundary-Condition Formulations
:class: warning

BAW's native condition uses the water–air fields `alpha.water` and hydrostatically reduced pressure `p_rgh` in Pa. It cannot be assigned directly to the Olsen single-phase kinematic pressure `p` in m²/s². The separate rating extension adjusts the geometric free surface in a serial, quasi-steady calculation; it is not a validated transient or conservative arbitrary Lagrangian–Eulerian formulation. It retains the Olsen hexahedral, that is vertically ordered mesh restrictions. The fixed-mesh `sediDriftFoam` has no movable free surface.
```

Complete the tests in the supplied [rating-curve validation instructions](https://github.com/Ecohydraulics/numerical-software-installers/blob/main/OpenFOAM-installer/docs/RATING_CURVE.md) before using the extension for research or design.

## Utilities (Pre- and Post-Processors)

### ParaView

Activate the installed environment, then open the simulation case with ParaView's built-in OpenFOAM reader:

```bash
cd /path/to/case-copy
touch case.foam
paraview case.foam
```

Select `internalMesh` and the relevant boundary patches, including `bedWall` and `freeSurface` where present. Enable `Conc`, `U`, and `p`, then select **Apply**. Choose the displayed field and use the animation controls to inspect the time series. For BAW water–air cases, inspect `alpha.water` and `p_rgh`. No OpenFOAM-linked ParaView reader plugin is required; see the [OpenFOAM reader documentation](https://www.paraview.org/paraview-docs/v5.12.0/python/paraview.simple.OpenFOAMReader.html).

### VisIt-DAV

Export the case to legacy VTK and generate time-series manifests in the activated shell:

```bash
python3 ~/.local/openfoam-sediment-v2406/postprocess.py /path/to/case-copy
visit
```

For a custom installation directory, adjust the script path. In VisIt, open one of the printed `.visit` files, add a **Pseudocolor** plot of `Conc` or another available scalar, select **Draw**, and use the animation controls. Open volume, bed, and free-surface manifests separately. The exporter retains time-dependent mesh coordinates and records OpenFOAM time values from metadata rather than inferring time from filenames; see the [VisIt file-series documentation](https://visit-sphinx-github-user-manual.readthedocs.io/en/v3.5.0/using_visit/WorkingWithFiles/Supported_File_Types.html#creating-visit-files).

Retain all exported timestep files. OpenFOAM time values need not equal the accelerated morphodynamic time recorded by Olsen's solver. Reconstruct parallel `interFoam` fields and meshes before serial export. To regenerate manifests after additional timesteps, move earlier `.visit` files aside; differing existing manifests are not overwritten.

```{admonition} Remote or Headless Computers
:class: note

On a server without a graphical desktop, transfer the case or its VTK export to a visualization workstation. The options `--skip-visualization` and Windows `-SkipVisualization` omit both viewers when a build-only installation is required. Use the installer's `paraview` and `visit` launchers to avoid conflicts between OpenFOAM libraries and viewer libraries.
```

### SALOME

SALOME is not installed by this script. Its installation is described in the TELEMAC instructions: {ref}`salome-install`.

(freecad-install)=
### FreeCAD

FreeCAD is not installed by this script. Windows, Linux, and macOS packages and installation instructions are available from the [FreeCAD project](https://www.freecad.org/).
