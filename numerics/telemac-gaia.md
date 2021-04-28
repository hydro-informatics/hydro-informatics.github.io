# Gaia Workflow

## Introduction

GAIA is the new open-source, sediment transport and bed evolution module of the TELEMAC-MASCARET modelling system.

GAIA is able to model complex sediment and morphodynamic processes in coastal areas, rivers, lakes and estuaries,
accounting for spatial and temporal variability of sediment size classes (uniform, graded or mixed), properties (cohesive and
non-cohesive) and transport modes (suspended, bedload and both simultaneously).
The generalized framework used for bed layering enables any combination of multiple size classes
for both non-cohesive and cohesive sediment to be modelled simultaneously. Compatibility
is ensured between an active layer model (an approach traditionally adopted for non-cohesive
sediment) and the presence of different classes of fine sediment and consolidation.

## Coupling GAIA and TELEMAC
GAIA can be internally coupled with the hydrodynamic models TELEMAC-2D or TELEMAC-
3D. The following keywords must be included in the TELEMAC-2D or TELEMAC-3D steering files:

`COUPLING WITH = ’GAIA’`

`GAIA STEERING FILE = ’<name of the gaia steering file>’`

Since GAIA is not operated fully coupled, the first step is to compute the flow variables with a fixed bed.
Subsequently the discretized sediment equation is solved separately.
The suspended sediment transport processes are computed by the hydrodynamic modules (TELEMAC-2D or TELEMAC-3D), while near-bed, bedload and processes
in the bottom layer are handled by GAIA.

## Mandatory files
The following files are mandatory to simulate morphodynamics:

* the steering files for GAIA and the hydrodynamic module (e.g. [T2D](../numerics/telemac2d)
or [T3D](../numerics/telemac3d)
    - File format = *.cas

* the geometry file
    - File format = *.slf

* the boundary conditions file
    - File format = *.cli

Optional files such as Fortran file (*.f), the reference file (*.slf), but are not featured here.

## Setup of GAIA Steering file
This file contains the necessary information for running a morphodynamic simulation and must contain all parameter values
that differ from the default value (as specified in the dictionary file `gaia.dico` and the `GAIA Reference Manual`).

It is recommended to orientate on the following 3 categories to set up the Steering-file.
### Define input and output files
All files should be stored in the same folder.

Assign file names to at least the following keywords:

`GEOMETRY FILE = '*.slf'`

`BOUNDARY CONDITIONS FILE = '*.cli'`

`RESULTS FILE = '*.slf'`

`VARIABLES FOR GRAPHIC PRINTOUTS = ''`

### Physical Parameters
Define essential physical parameters such as sediment type, grain sizes, and decide which
transport mechanisms, and formulas to include in your calculation. Consider the following important keywords:

`TYPE OF SEDIMENT = CO; NCO`

`CLASSES SEDIMENT DIAMETERS = 0.0001; 0.1`

`BED LOAD FOR ALL SANDS = YES or NO`

`BED-LOAD TRANSPORT FORMULA FOR ALL SANDS`

`SUSPENSION FOR ALL SANDS = YES or NO`

Specific settling velocities or shields parameters can be defined or calculated directly by GAIA (default).

### Numerical options and parameters
Define which numerical schemes, solvers to use in your calculation. Consider the following important keywords:

`TIDAL FLATS = YES or NO`

`OPTION FOR THE TREATMENT OF TIDAL FLATS`

`SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS`

`FINITE VOLUMES = YES or NO`

`ADVECTION-DIFFUSION SCHEME WITH SETTLING VELOCITY`

`SOLVER FOR DIFFUSION OF SUSPENSION`


## Run Simulation
The simulation is started identically to a hydrodynamic simulation by calling the telemac2d.py script.
Please note that `*_tel.cas` is the hydrodynamic and not the GAIA steering file.

`cd /go/to/dir`

`telemac2d.py *_tel.cas`

However, in the steering file of the hydrodynamic model
the required keywords (see Coupling GAIA and TELEMAC) for the coupling must be present.
