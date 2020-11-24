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

The steering file is the main simulation file with information about mandatory files (e.g., the *selafin* geometry or the *cli* boundary), optional files, and simulation parameters. The steering file can be created or edited either with a basic text editor or an advanced software such as [*Fudaa-PrePro*](install-telemac.html#fudaa) or *BlueKenue*](install-telemac.html#bluekenue).

***

Next: [> Start the simulation >](tm-main.html)
