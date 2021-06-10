(telemac2d-steady)=
# Steady 2d Simulation

```{admonition} Requirements
The case featured in this tutorial was established with:
* {ref}`Fudaa PrePro v1.4 <fudaa>`
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* Optional: {ref}`Blue Kenue <bluekenue>`
```

## Input files

See the section on {ref}`TELEMAC files <tm-files>`

## Build geometry and computational mesh

## Geometry File Option 1: BlueKenue

### File description and reference to CAS
The geometry file in [*slf* (*selafin*)](https://gdal.org/drivers/vector/selafin.html) format contains binary data about the mesh with its nodes. The name format of the geometry file can be modified in the steering file with:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF  / or MED with SALOME verify usage
```



(slf-qgis)=
## Serafin Geometry with QGIS & BASEMESH


Then...


(prepro-fudaa)=
## Model setup with Fudaa Prepro

*Fudaa PrePro* facilitates the definition of boundaries, initial conditions, and setting up a steering file. To start *Fudaa*, open *Terminal* (*Linux*) or *Command Prompt* (*Windows*) and:

* `cd` to the installation directory of *Fudaa*
* start the GUI:
    + *Linux*: tap `sh supervisor.sh`
    + *Windows*: tap `supervisor.bat`


## Boundary Conditions

The boundary file in *cli* format contains information about inflow and outflow nodes (coordinates and IDs). The *cli* file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use [*Fudaa-PrePro*](../get-started/install-telemac.html#fudaa) or [*BlueKenue*](../get-started/install-telemac.html#bluekenue) for generating and/or modifying *cli* files.

In addition, users can define a liquid boundary conditions file (*qsl*) to define time-dependent boundary conditions (e.g., discharge, water depth, flow velocity or tracers).

### Stage-discharge (or WSE-Q) Relationship

Define a stage-discharge file (*ASCII* format) to use a stage (water surface elevation *WSE*) - discharge relationship for boundary conditions. Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). To use a stage-discharge file, define the following keyword in the steering file:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```


### Define steady flow boundaries {#prepro-steady}

Qconst

### Define unsteady flow boundaries {#prepro-unsteady}

The name format of the boundary conditions file can be modified in the steering file with:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
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

### Activate morphodynamics (sediment transport with Gaia) {#prepro-gaia}

Qs



## Run Telemac2d

### Load environment and files

Load the TELEMAC *Python* variables:

```
cd ~/telemac/v8p1/configs
source pysource.openmpi.sh
config.py
```



### Start a 2D hydrodynamic simulation (steady) {#steadyrun}

To start a simulation, `cd` to the directory where the simulation files live (see previous page) and launch the steering file (*cas*) with *telemac2d.py*:

```
cd /go/to/dir
telemac2d.py run_2dhydrodynamic.cas
```
