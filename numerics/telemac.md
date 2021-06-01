(chpt-telemac)=
# TELEMAC

  The numerical simulation methods described on these pages use the freely available software *open TELEMAC-MASCARET* (in the following referred to as TELEMAC), which was started as a commercial code by the R&D group of Électricité de France (EDF). Since 2010, the TELEMAC-MASCARET Consortium took over the development (EDF R&D is still deeply involved) and freely provides the software and its source code under a [*GPLv3* license](http://www.gnu.org/licenses/gpl-3.0.html). Visit their [website](http://www.opentelemac.org/) to learn more about TELEMAC.


## Get Started

It is strongly recommended to install [*Debian Linux*](https://www.debian.org/) or one of its derivatives for working with TELEMAC (see the chapter on {ref}`Virtual Machines (VMs) and Linux <chpt-vm-linux>`). Then, proceed with the {ref}`installation of TELEMAC <telemac-install>`. Account for approximately 2 hours to get ready with TELEMAC.


## General Introduction and Tutorial Guide

The analysis of hydro-environments with TELEMAC involves pre-processing for abstracting the fluvial landscape, setting up control files, running a TELEMAC solver, and post-processing. The first-time user faces an overwhelming number of software options for pre- and post-processing. Moreover, TELEMAC comes with a wide range of modules for two-dimensional (2d) and three-dimensional (3d) modeling of hydro-morphodynamic processes of various water bodies, from mountain rivers to coastal deltas under the influence of tides. Also, multiple sediment transport phenomena can be modeled and coupled with steady or unsteady flow conditions.

The tutorials in this eBook feature:

* the usage of TELEMAC with the computational mesh created in the {ref}`pre-processing with QGIS tutorial <qgis-prepro>` (refer to the section describing the {ref}`export of the mesh to SLF <qgis4tm>`);
* a purely hydrodynamic 2d model with steady discharge boundary conditions in the {ref}`chpt-telemac2d` section with the standard SLF geometry format;
* a purely hydrodynamic 3d model with steady discharge boundary conditions in the {ref}`chpt-telemac3d` section with the MED geometry format.
* Future tutorials (under development) will also feature:
  * the implementation of unsteady boundary conditions (replace steady flow boundaries);
  * the activation of sediment transport (morphodynamic) modeling with TELEMAC's Gaia module.

The tutorials build on the user manuals provided by the TELEMAC developers at [http://wiki.opentelemac.org](http://wiki.opentelemac.org/doku.php?id=documentation_v8p2r0).


### Pre-processing

Pre-processing involves abstracting the river landscape into a computational mesh (grid) with boundary conditions. Many software tools can be used for this purpose such as:

* {ref}`qgis-install` and the BASEmesh plugin, which are illustrated in the {ref}`QGIS pre-processing tutorial <qgis-prepro`.
* The National Research Council Canada's {ref}`Blue Kenue <bluekenue>` GUI software (primarily for *Windows*).
* {ref}`SALOME-HYDRO <salome-hydro>` for generating computational meshes in the MED files format (here illustrated in the {ref}`chpt-telemac3d` tutorial).

### Model setup and run

The centerpiece of any TELEMAC model is the control (steering or *CAS*) file, which can be comfortably set up with [Fudaa PrePro](../get-started/install-telemac.html#fudaa). The basic setup of a [steady](../numerics/telemac2d.html#steady) and a [unsteady](../numerics/telemac2d.html#unsteady) model are explained on the [Model Setup page](../numerics/telemac2d). In addition, explanations are provided on the use of the [Gaia module for modeling morphodynamic (sediment transport) processes](../numerics/telemac2d.html#prepro-gaia).

### Post-processing

*Artelia Eau et Environnement* created the [PostTelemac](https://plugins.qgis.org/plugins/PostTelemac/) plugin for *QGIS*, which is a powerful and convenient tool visualizing and post-processing TELEMAC simulation results. The [*Telemac2d*](../numerics/telemac2d) and [*Telemac3d*](../numerics/telemac3d) tutorials provide guidance on the usage of the *PostTelemac* plugin and [*SALOME*](../get-started/install-openfoam.html#salome) for post-processing *SLF* and *MED* results files, respectively.

## The TELEMAC file structure

For any TELEMAC 2D simulation, the following input files are **mandatory**:

* Steering file
    + File format: `cas`
    + Prepare either with [Fudaa PrePro](../numerics/telemac2d.html#prepro-fudaa).
* Geometry file
    + File format: `.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html) or `.med` (*MED* file library from the [salome-platform](https://www.salome-platform.org)
    + Prepare either with [*BlueKenue<sup>TM</sup>*](../get-started/install-telemac.html#bluekenue) or [Fudaa PrePro](../numerics/telemac2d.html#prepro-fudaa).
* Boundary conditions
    + File format: `.cli` (with `slf`) or `.bnd`/`.bcd` (with `.med`)
    + Prepare `.cli` files with [*BlueKenue<sup>TM</sup>*](../get-started/install-telemac.html#bluekenue) and [Fudaa PrePro](../numerics/telemac2d.html#prepro-fudaa).
    + Prepare  `.bnd`/`.bcd` files either with *SALOME-HYDRO* or with a text editor (read more in the [Telemac3d tutorial](../numerics/telemac3d.html#bnd-mod)

There are many more file formats, which are not computationally mandatory for running a simulation with TELEMAC, but essential in practice to yield reasonable results with a hydro-morphodynamic model (i.e., coupled hydrodynamic-sediment transport solver). Such **optional** files are:

* Liquid boundaries file (e.g., for water surface elevation or flow rates)
    + Requires a stage-discharge relationship file
    + File format: `.qsl`
* Friction data file
    + File format: `tbl` (`ASCII`)
* Reference file to enable model validation (restart)
    + File format: `.slf` or `.med`
    + Check the TELEMAC docs
* Restart file for setting initial conditions (`.slf` or `.med`)
* Sections file to set control sections (e.g., verify flow rates, velocity, or water surface elevation)
* Sources (e.g., water or sediment) data file
* Zones file
    + Describes friction or other zonal properties

When hydraulic structures are integrated into a model, some of the following files are required (depending on the structure type):

* Culverts data file
* Weirs data file

In addition, a *FORTRAN* (`.f`) file can be created to specify special boundary conditions or the usage of either single or double precision

```{tip}
In hydro-morphodynamic modeling, single precision (i.e., 32-bit *floats*) rather than double precision (i.e., using 64-bit *floats*) is sufficient and much faster.
```

More input files can be defined to simulate oil spills, pollutant transport, wind, and tide effects.

***

Continue with setting up a mesh (*2dm* file) and a geometry file (*SLF*) with either

* [> *QGIS* >](pre-qgis), or
* [> *Blue Kenue<sup>TM</sup>* >](../numerics/telemac2d)

***

## Detailed file descriptions

### The steering file (CAS)

The steering file is the main simulation file with information about mandatory files (e.g., the [*selafin*](https://gdal.org/drivers/vector/selafin.html) geometry or the *cli* boundary), optional files, and simulation parameters. The steering file can be created or edited either with a basic text editor or advanced software such as [*Fudaa-PrePro*](../get-started/install-telemac.html#fudaa) or [*BlueKenue*](../get-started/install-telemac.html#bluekenue). In this example, we will use *BlueKenue*.


### The geometry file (SLF or MED)

The geometry file in [*slf* (*selafin* or *SERAFIN*)](https://gdal.org/drivers/vector/selafin.html) format contains binary data about the mesh with its nodes. The name format of the geometry file can be modified in the steering file with:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF  / or MED with SALOME preferably for 3D
```

*MED* files are typically processed with either [*SALOME*](../get-started/install-openfoam.html#salome) or [*SALOME-HYDRO*](../get-started/install-telemac.html#salome-hydro), which are featured in the [*Telemac3d*](../numerics/telemac3d) tutorial.

### The boundary conditions (CLI or BND/BCD) and liquid boundary (QSL) files

The boundary file in *cli* format contains information about inflow and outflow nodes (coordinates and IDs). The *cli* file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use [*Fudaa-PrePro*](../get-started/install-telemac.html#fudaa) or [*BlueKenue*](../get-started/install-telemac.html#bluekenue) for generating and/or modifying *cli* files.

In addition, users can define a liquid boundary conditions file (*qsl*) to define time-dependent boundary conditions (e.g., discharge, water depth, flow velocity or tracers).

The name format of the boundary conditions file can be modified in the steering file with:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

Example (header only) for a boundary conditions file (*cli*):
```
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    101     1
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    102     2
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    103     3
  ...
```

Example for a liquid boundary conditions file:
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

### The stage-discharge (or WSE-Q) file (txt - ASCII)

Define a stage-discharge file to use a stage (water surface elevation *WSE*) - discharge relationship for boundary conditions. Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). To use a stage-discharge file, define the following keyword in the steering file:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```

Example for a stage-discharge file:
```
# wse_Q.txt
#
Q(1)     Z(1)
m3/s     m
 50.     0.0
 60.     0.9
100.     1.5
```

### The friction data file (tbl - ASCII)

This optional file enables the definition of bottom friction regarding the roughness law to use and associated function coefficients. To activate and use friction data, define the following keywords in the steering file:

```
/steering.cas
FRICTION DATA            : YES
FRICTION DATA FILE       : 'friction.tbl'
```


### The results file (SLF or MED)

The name format of the results file can be modified in the steering file with:

```
/steering.cas
RESULTS FILE             : 't2d_channel_output.slf'
```

Because this file is generated by TELEMAC when the simulation is running, it does not need to exist for starting the simulation. A good option for visualizing the results file is the [*PostTelemac* Plugin in *QGIS*](../get-started/install-telemac.html#qgis)

*MED* results files are typically processed with either [*SALOME*](../get-started/install-openfoam.html#salome) or [*SALOME-HYDRO*](../get-started/install-telemac.html#salome-hydro), which are featured in the [*Telemac3d*](../numerics/telemac3d) tutorial.
