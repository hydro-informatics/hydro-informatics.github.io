(chpt-telemac)=
# TELEMAC

The numerical simulation methods described on these pages use the freely available software *open TELEMAC-MASCARET* (in the following referred to as TELEMAC), which was started as a commercial code by the R&D group of Électricité de France (EDF). Since 2010, the TELEMAC-MASCARET Consortium took over the development (EDF R&D is still deeply involved) and freely provides the software and its source code under a [GPLv3 license](http://www.gnu.org/licenses/gpl-3.0.html). Visit their [website](http://www.opentelemac.org/) to learn more about TELEMAC.

Working on [Debian Linux](https://www.debian.org/) or one of its derivatives (see the chapter on {ref}`Virtual Machines (VMs) and Linux <chpt-vm-linux>`) facilitates handling TELEMAC, because most of its core algorithms were originally developed on Linux platforms. Using Linux follow the {ref}`TELEMAC installation <telemac-install>` chapter (account for approximately 2 hours for the installation).

(tm-tutorial-guide)=
## General Introduction and Tutorial Guide

The analysis of hydro-environments with TELEMAC involves pre-processing for abstracting the fluvial landscape, setting up control files, running a TELEMAC solver, and post-processing. The first-time user faces an overwhelming number of software options for pre- and post-processing. Moreover, TELEMAC comes with a wide range of modules for two-dimensional (2d) and three-dimensional (3d) modeling of hydro-morphodynamic processes of various water bodies, from mountain rivers to coastal deltas under the influence of tides. Also, multiple sediment transport phenomena can be modeled and coupled with steady or unsteady flow conditions. Consequently, TELEMAC's applications range is very wide and this eBook provides tutorials for a sound understanding of fundamental elements of river ecosystem modeling. To this end, this eBook features the following tutorials:

* Generate a Selafin `*.slf*` geometry mesh along with boundary conditions with QGIS, the BASEmesh plugin, and BlueKenue in the {ref}`pre-processing tutorial <slf-prepro-tm>`. **Recommended as first introductory tutorial for beginners.**
* Setup a purely hydrodynamic, steady Telemac2d simulation in the {ref}`steady 2d tutorial <telemac2d-steady>` (Selafin `*.slf*` geometry). **Recommended as a second tutorial for beginners.**
* Apply quasi-steady (near-census unsteady) flow conditions (e.g., important for modeling a flood hydrograph) in the {ref}`unsteady Telemac2d tutorial <chpt-unsteady>`. This tutorial builds on top of the steady Telemac2d tutorial.
* Setup a purely hydrodynamic 3d model in the {ref}`Telemac3d (Selafin) tutorial <chpt-telemac3d-slf>` with the standard Selafin (`*.slf`) format.
* Setup a purely hydrodynamic 3d model in the {ref}`Telemac3d (MED and Salome) tutorial <chpt-telemac3d-med>` with the MED geometry format using SALOME (***Outdated workflow***).
* Couple hydrodynamics (i.e., Telemac2d or Telemac3d) with morphodynamics (i.e., {term}`Sediment transport`) in the {ref}`Gaia tutorial <tm-gaia>`.


The tutorials build on the user manuals provided by the TELEMAC developers at [http://wiki.opentelemac.org](http://wiki.opentelemac.org/doku.php?id=documentation_v8p3r0).


### Pre-processing

Pre-processing involves abstracting the river landscape into a computational mesh (grid) with boundary conditions. Many software tools can be used for this purpose such as:

* {ref}`qgis-install` and the BASEmesh plugin, which are illustrated in the {ref}`QGIS pre-processing tutorial <slf-prepro-tm>` (**the Author's preferred choice**).
* The National Research Council Canada's {ref}`Blue Kenue <bluekenue>` GUI software (primarily for *Windows*).
* {ref}`SALOME <salome-install>` for generating computational meshes in the MED files format.

### Model Setup and Run

The centerpiece of any TELEMAC model is the control (steering or CAS) file, which can be set up with {ref}`Fudaa PrePro <fudaa>`. The model setup is explained in the above {ref}`tutorial guide <tm-tutorial-guide>` for TELEMAC.

### Post-processing

*Artelia Eau et Environnement* created the [PostTelemac](https://plugins.qgis.org/plugins/PostTelemac/) plugin for {ref}`qgis-install`, which is a powerful and convenient tool for visualizing and post-processing TELEMAC simulation results. The {ref}`Telemac2d (steady) Post-processing <tm-steady2d-postpro>` illustrates the usage of the PostTelemac QGIS plugin (read more in the {ref}`TELEMAC pre-processing tutorial <tm-qgis-plugins>`) to create {ref}`raster <raster>` maps and other useful data derivatives from TELEMAC output. In addition, the {ref}`Telemac3d (MED) <sh-postproc>` tutorial features the usage of the ParaVis module (a ParaView derivative) in {ref}`SALOME <salome-install>`.

(tm-files)=
## The TELEMAC File Structure

For any TELEMAC simulation, the following input files are **mandatory**:

* Steering file
  + File format: `*.cas`
  + Prepare either with {ref}`Fudaa PrePro <fudaa>` or use a text editor (e.g., {ref}`npp`).
* Geometry file
  + File formats: `*.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html) or `*.med` (MED file library from the [salome-platform](https://www.salome-platform.org)
  + Prepare `*.slf` geometries with {ref}`QGIS <qgis-tutorial>`or {ref}`Blue Kenue <bluekenue>` (read more in the {ref}`TELEMAC pre-processing tutorial <bk-create-slf>`).
  + Prepare `*.med` geometries with {ref}`SALOME <salome-install>`.
* Boundary conditions
  + File format: `*.cli` (with `*.slf`) or `*.bnd`/`*.bcd` (with `*.med`)
  + Prepare `*.cli` files with {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>` (read more in the {ref}`TELEMAC pre-processing tutorial <bk-bc>`).
  + Prepare `*.bnd`/`*.bcd` files either with {ref}`SALOME <salome-install>` or with a text editor (read more in the {ref}`Telemac3d (MED) tutorial <bnd-mod>`).

There are many more files that are not computationally mandatory for every TELEMAC simulation, but essential for particular scenarios (e.g., unsteady flows) and modules (e.g., sediment transport with Gaia). Such **optional** files include:

* Unsteady flow file (e.g., for water surface elevation or flow rates)
  + Requires a stage-discharge relationship file
  + File format: `*.qsl`
* Friction data file
  + File format: `*.tbl` or `*.txt` (`ASCII`)
* Restart / reference (for model validation) file
  + File format: `.slf` or `.med`
  + More information in the {{ tm2d }} (section 4.1.3) (see also {cite:t}`hervouet_user_2014`).
* Sections file to set control sections (e.g., verify flow rates, velocity, or water surface elevation)
* Sources (e.g., water or sediment) data file
* Stage-discharge relation file
  + File format: `*.tbl` or `*.txt` (`ASCII`)
* Zones files to describe reginal friction or other zonal properties

When hydraulic structures are integrated into a model, some of the following files are required (depending on the structure type):

* Culverts data file
* Weirs data file

In addition, a *FORTRAN* (`.f`) file can be created to specify special boundary conditions, custom algorithms, or the usage of either single or double precision.

```{admonition} Single and double precision
In hydro-morphodynamic modeling, single precision (i.e., 32-bit *floats*) rather than double precision (i.e., using 64-bit *floats*) is sufficient and much faster.
```

More input files can be defined to simulate oil spills, pollutant transport, wind, and tide effects.


## Detailed File Descriptions

### The Steering File (CAS)

The steering file is the main simulation file with information about mandatory files (e.g., the [*selafin*](https://gdal.org/drivers/vector/selafin.html) geometry or the boundary), optional files, and simulation parameters. The steering file can be created or edited with a basic text editor or advanced software such as {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>`.


### Geometry Files (SLF or MED)

The geometry file in [`*.slf` (*selafin* or *SERAFIN*)](https://gdal.org/drivers/vector/selafin.html) format contains binary data about the mesh with its nodes. The name format of the geometry file can be modified in the steering file with:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF / or MED with SALOME preferably for 3D
```

*MED* files are typically processed with either {ref}`SALOME <salome-install>`, which are featured in the {ref}`Telemac3d (MED) <chpt-telemac3d-med>` tutorial.


### Boundary Conditions (CLI or BND/BCD) and Liquid Boundary (QSL) Files

The boundary file in `*.cli` format contains information about inflow and outflow nodes (coordinates and IDs). The `*.cli` file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>` for generating and/or modifying `*.cli` files (read more in the {ref}`TELEMAC pre-processing tutorial <bk-bc>`). Here is an example (header only) for a `*.cli` boundary conditions file:

```
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    101     1
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    102     2
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    103     3
  ...
```


`*.bnd`/`*.bcd` files can be created and edited either with {ref}`SALOME <salome-install>` or a text editor (read more in the {ref}`Telemac3d (MED) tutorial <bnd-mod>`). The following block box shows how a `*.bnd` boundary file for a simple block geometry may look like.

```
4
5 4 4 4 downstream
4 5 5 4 upstream
2 0 0 2 leftwall
2 0 0 2 rightwall

```

Users can define a liquid boundary conditions file (`*.qsl`) to define time-dependent (unsteady) boundary conditions (e.g., discharge, water depth, flow velocity, or tracers). The following block shows an example for a liquid boundary conditions (`*.qsl`) file:
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

The boundary conditions and liquid boundary files can be added in the steering file with:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

### Stage-discharge (or WSE-Q) File (txt - ASCII)

Define a stage-discharge file to use a stage (water surface elevation *WSE*) - discharge relationship for boundary conditions. Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). The following block shows an example for a stage-discharge (`*.txt`) file:

```
# wse_Q.txt
#
Q(1)     Z(1)
m3/s     m
 50.     0.0
 60.     0.9
100.     1.5
```

To use a stage-discharge file, define the following keyword in the steering file:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```

### Friction Data File (tbl/txt - ASCII)

This optional file enables the definition of bottom friction regarding the roughness law to use and associated function coefficients.

To activate and use friction data, define the following keywords in the steering file:

```
/steering.cas
FRICTION DATA            : YES
FRICTION DATA FILE       : 'friction.tbl'
```

### The Results/Restart file (SLF or MED)


A restart file stems from a previous TELEMAC simulation and does not need to exist at the beginning. A good option for visualizing the results file is the {ref}`PostTelemac plugin <tm-qgis-plugins>` in QGIS.
Restart files in MED format are typically processed with the ParaVis module in {ref}`SALOME <salome-install>`, which is featured in the {ref}`Telemac3d (MED) <chpt-telemac3d-med>` tutorial.

The results/restart file can be define in the steering file as follows:
```
/steering.cas
RESULTS FILE             : 't2d_channel_output.slf'
```

The {{ tm2d }} (section 4.1.3) provide more explanations on the usage of results/restart files (e.g., for speeding up simulations).
