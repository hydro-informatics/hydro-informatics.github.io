---
title: The structure of TELEMAC models
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, raster, shapefile, qgis, hydraulics, tin]
keywords: numerics
sidebar: mydoc_sidebar
permalink: tm-about.html
folder: numerics
---


This page builds on descriptions provided in the [telemac2d_user_v8p1](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac2d/user/telemac2d_user_v8p1.pdf) manual.

{% include tip.html content="**New to TELEMAC?** Then just read through the general introduction and tutorial guide section. Ignore the detailed file description for the moment and come back there after running your first TELEMAC model." %}

## General Introduction and Tutorial Guide

Analysis of a hydro-environment with TELEMAC involves pre-processing for abstracting the fluvial landscape, setting up control files, running a TELEMAC solver, and post-processing. The first-time user faces an overwhelming number of software options for pre- and post-processing. In addition, TELEMAC comes with a wide range of modules for 2D and 3D calculations of hydro-morphodynamic processes of various water bodies, from mountain rivers to coastal deltas under the influence of tides. Also various sediment transport processes can be considered coupled with steady or unsteady flow conditions.

The tutorials on this website show how to 
 - create a pure hydrodynamic model with steady-state runoff boundary conditions;
 - implement unsteady boundary conditions (replace steady flow boundaries);
 - activate modelling of sediment transport processes (morphodynamics) with TELEMAC's Gaia module.
 
Thus, the focus on this website is on modeling small to medium-sized rivers without the influence of tides.

### Pre-processing

Pre-processing involves abstracting the river landscape into a computational grid (mesh) with boundary conditions. Many software tools can be used for this purpose and this website features two options for mesh generation and defining geometry boundary conditions:

1. Use [*QGIS*](geo_software.html#qgis) and the [*BASEmesh* plugin](bm-pre.html#get-ready-with-qgis). The [*QGIS* Prepro option](pre-qgis.html) is convenient for creating geo-referenced 2D meshes and uses the pre-processing routines of [BASEMENT](basement.html). So this is not an officially recommended version by the TELEMAC developers, but rather a home-brewed option on this website.
1. Use the National Research Council Canada's [*Blue Kenue<sup>TM</sup>*](install-telemac.html#bluekenue) GUI software. The [*Blue Kenue<sup>TM</sup>* Prepro option](tm2d-pre-bk.html) is preferably for *Windows* users and is somewhat cumbersome for creating geo-referenced point and line datasets to delineate the mesh.

In addition, the [next chapter](tm3d-pre.html#prepro-salome) introduces [SALOME](install-telemac.html#salome) for pre-processing of 3D models.

### Model setup and run

The centerpiece of any TELEMAC model is the control (steering or *CAS*) file, which can be comfortably set up with [Fudaa PrePro](install-telemac.html#fudaa). The basic setup of a [steady](tm-run.html#steady) and a [unsteady](tm-run.html#unsteady) model are explained on the [Model Setup page](tm-run.html). In addition, explanations are provided on the use of the [Gaia module for modeling morphodynamic (sediment transport) processes](tm-run.html#prepro-gaia).

### Post-processing

*Artelia Eau et Environnement* created the [PostTelemac](https://plugins.qgis.org/plugins/PostTelemac/) plugin for *QGIS*, which is a powerful and convenient tool visualizing and post-processing TELEMAC simulation results. The TELEMAC [post-processing page](tm2d-post.html) provides guidance on the usage of the *PostTelemac* plugin. Thus, simulation results can be visualized on a georeferenced basemap or exported to other formats (e.g., GeoTIFF rasters or shapefiles).

## The TELEMAC file structure

For any TELEMAC 2D simulation, the following input files are **mandatory**:

* Steering file 
    + File format: `cas`
    + Prepare either with [Fudaa PrePro](tm-run.html#prepro-fudaa). 
* Geometry file
    + File format: `.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html))
    + Prepare either with [*BlueKenue<sup>TM</sup>*](install-telemac.html#bluekenue) or [Fudaa PrePro](tm-run.html#prepro-fudaa).
* Boundary conditions
    + File format: `.cli`
    + Prepare either with [Fudaa PrePro](tm-run.html#prepro-fudaa).

There are many more file formats, which are not computationally mandatory for running a simulation with TELEMAC, but essential inpractice to yield reasonable results with a hydro-morphodynamic model (i.e., coupled hydrodynamic-sediment transport solver). such **optional** files are:

* Liquid boundaries file (e.g., for water surface elevation or flow rates)
    + Requires a stage-discharge relationship file 
* Friction data file 
    + File format: `tbl` (`ASCII`)
* Reference file to enable model validation (restart)
    + File format: `.slf`
    + Check the TELEMAC docs
* Restart file for setting initial conditions (`SLF`)
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

***

Continue with setting up a mesh (*2dm* file) and a geometry file (*SLF*) with either 

* [> *QGIS* >](pre-qgis.html), or
* [> *Blue Kenue<sup>TM</sup>* >](tm2d-pre-bk.html) 

***

## Detailed file descriptions

*** 

### The steering file (CAS)

The steering file is the main simulation file with information about mandatory files (e.g., the [*selafin*](https://gdal.org/drivers/vector/selafin.html) geometry or the *cli* boundary), optional files, and simulation parameters. The steering file can be created or edited either with a basic text editor or an advanced software such as [*Fudaa-PrePro*](install-telemac.html#fudaa) or [*BlueKenue*](install-telemac.html#bluekenue). In this example, we will use *BlueKenue*.



### The geometry file (SLF or MED)

The geometry file in [*slf* (*selafin* or *SERAFIN*)](https://gdal.org/drivers/vector/selafin.html) format contains binary data about the mesh with its nodes. The name format of the geometry file can be modified in the steering file with:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF  / or MED with SALOME preferably for 3D
```


### The boundary conditions (CLI) and liquid boundary (QSL) files

The boundary file in *cli* format contains information about inflow and outflow nodes (coordinates and IDs). The *cli* file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use [*Fudaa-PrePro*](install-telemac.html#fudaa) or [*BlueKenue*](install-telemac.html#bluekenue) for generating and/or modifying *cli* files.

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
# Time-dependent inflow (discharge Q(2)) and outflow (depth SL(1))
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


### The results file (SLF)

The name format of the results file can be modified in the steering file with:

```
/steering.cas
RESULTS FILE             : 't2d_channel_output.slf'
```

Because this file is generated by TELEMAC when the simulation is running, it does not need to exist for starting the simulation. A good option for visualizing the results file is the [*PostTelemac* Plugin in *QGIS*](install-telemac.html#qgis)

