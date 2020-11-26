---
title: Pre-Processing for TELEMAC-MASCARET models
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, raster, shapefile, qgis, hydraulics, tin]
keywords: numerics
summary: "Produce a numerical mesh with QGIS/Blue Kenue."
sidebar: mydoc_sidebar
permalink: tm-pre.html
folder: numerics
---

## Under construction. Expected release of this tutorial: Spring 2021.

Thank you for your patience.

{% include requirements.html content="This tutorial refers to TELEMAC-MASCARET v8p1 (parallel with *Open MPI*) installed on Debian Linux. For the best learning experience follow the installation guides for [Debian Linux on a Virtual Machine (VM)](#vm.html) and [TELEMAC-MASCARET](install-telemac.html)." %}

This tutorial uses descriptions provided in the [telemac2d_user_v8p1](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac2d/user/telemac2d_user_v8p1.pdf) manual.

## Input files

### Overview

For any TELEMAC 2D simulation, the following files are mandatory:

* Steering file 
    + File format: `cas`
    + Prepare either with [Fudaa PrePro](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/253165587/How+to+launch+Fudaa-Prepro) or [*BlueKenue<sup>TM</sup>*](install-telemac.html#bluekenue).
* Geometry file
    + File format: `.slf` (selafin)
    + Prepare either with
* Boundary conditions
    + File format: `.cli`
    + Prepare either with

The basic setup of the files is explained below.

### Optional

The below listed files are not computationally mandatory for running a simulation with TELEMAC, but essential to yield reasonable results with a hydro-morphodynamic model (i.e., coupled hydrodynamic-sediment transport solver).

* Liquid boundaries file (e.g., for water surface elevation or flow rates)
    + Requires a stage-discharge relationship file 

* Friction data file 
* Reference file to enable model validation (restart)
    + File format: `.slf`
    + Check the TELEMAC docs
* Restart file for setting initial conditions
* Sections file to set control sections (e.g., verify flow rates, velocity or water surface elevation)
* Sources (e.g., water or sediment) data file
* Zones file
    + Describes friction or other zonal properties

When hydraulic structures are integrated in a model, some of the following files are required (depending on the structure type):

* Culverts data file
* Weirs data file

In addition, a *FORTRAN* (`.f`) file can be created to specify special boundary conditions or the usage of either single or double precision

{% include tip.html content="In hydro-morphodynamic modelling, single precision (i.e., 32-bit *floats*) rather than double precision (i.e., using 64-bit *floats*) is sufficient and much faster." %}

More input files can be defined to simulate oil spill, pollutant transport, wind, and tide effects.

### The steering file (CAS)

The steering file is the main simulation file with information about mandatory files (e.g., the *selafin* geometry or the *cli* boundary), optional files, and simulation parameters. The steering file can be created or edited either with a basic text editor or an advanced software such as [*SALOME*](install-telemac.html#salome), [*Fudaa-PrePro*](install-telemac.html#fudaa), or [*BlueKenue*](install-telemac.html#bluekenue). In this examples, we will use *SALOME*.

### The geometry file (SLF or MED)

The geometry file in *slf* (*selafin*) format contains binary data about the mesh with its nodes. The name format of the geometry file can be modified in the steering file with:

```
/steering.cas
GEOMETRY FILE            : t2d_channel.slf 
GEOMETRY FILE FORMAT     : SLF  / or MED with SALOME verify usage
```

### The boundary conditions file (CLI) and liquid boudnaries (QSL)

The boundary file in *cli* format contains information about inflow and outflow nodes (coordinates and IDs). The *cli* file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use [*Fudaa-PrePro*](install-telemac.html#fudaa) or [*BlueKenue*](install-telemac.html#bluekenue) for generating and/or modifying *cli* files.

In addition, users can define a liquid boundary conditions file (*qsl*) to define time-dependent boundary conditions (e.g., discharge, water depth, flow velocity or tracers). 

The name format of the boundary conditions file can be modified in the steering file with:

```
/steering.cas
BOUNDARY CONDITIONS FILE : bc_channel.cli 
LIQUID BOUNDARIES FILE   : bc_unsteady.qsl
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
# Time-dependent inflow (discharge Q(2)) and outflow (depth SL(1))
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

### The stage-discharge (or WSE-Q) file

Define a stage-discharge file to use a stage (water surface elevation *WSE*) - discharge relationship for boundary conditions. Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). To use a stage-discharge file, define the following keyword in the steering file:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```

### The friction data file

This optional file enables the definition of bottom friction regarding the roughness law to use and associated function coefficients. To activate and use friction data, define the following keywords in the steering file:

```
/steering.cas
FRICTION DATA            : YES
FRICTION DATA FILE       : friction.ROUGH / verify
```


### The results file (SLF)

The name format of the results file can be modified in the steering file with:

```
/steering.cas
RESULTS FILE             : t2d_channel_output.slf 
```

Because this file is generated by TELEMAC when the simulation is running, it does not need to exist for starting the simulation. A good option for visualizing the results file is the [*PostTelemac* Plugin in *QGIS*](install-telemac.html#qgis)

## Start SALOME

Make sure to have *SALOME* installed ([see instructions](install-telemac.html#salome)) and launch *SALOME* (on *Debian*):

```
cd SALOME-9.5.0-DB10-SRC
./sat environ SALOME-9.5.0
./sat launcher SALOME-9.5.0
./salome
```


***

Next: [> Start the simulation >](tm-main.html)
