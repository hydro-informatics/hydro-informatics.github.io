(tm-gaia)=
# Hydro-Morphodynamic 2d Simulation (Gaia)
*This chapter is based on descriptions from {{ mouris }}*

```{figure} ../img/hydro-morphodynamics.png
:alt: hydrodynamics morphodynamics
:name: hydro-morphodynamics

A morphodynamically active tributary of Cache Creek (California, USA).
```

## Under construction. Expected release in the next 12 months.

Thank you for your patience.


```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials.

The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```


## About Morphodynamics

### Hydro-morphodynamics Terminology
A hydro-morphodynamic simulation implies modeling runoff-driven **{term}`Sediment transport`** processes. The previous sections in this eBook focus on hydrodynamics defined as *the study of liquids in motion* and this section focusses on **morphodynamics** defined as **the study of time-dependent changes in the forms of alluvial beds and their underlying processes**.

### What is Gaia?
TELEMAC has a dedicated module called Gaia for this purpose and Gaia enables modelling sediment transport and morphological evolution (i.e., {term}`Topographic change`) in rivers, lakes, and estuaries. Gaia comes with particular routines to consider spatio-temporal variation of grain sizes, grading curves, and sediment transport modes in the form of **{term}`Bedload` (coarse sediment)** and/or **{term}`Suspended load` (fine sediment)**. {term}`Bedload` is calculated by solving a semi-empiric equations, such as  the {cite:t}`meyer-peter_formulas_1948` formula (read more later in this tutorial). {term}`Suspended load` is modeled by solving the {term}`Advection`-{term}`Diffusion` equations and additionally requires closures for sediment erosion and deposition fluxes . Sediment is further distinguished between very fine, **cohesive** sediment and coarser, **non-cohesive** sediment. In addition, Gaia accounts for bed evolution through an iterative solution of the {cite:t}`exner_uber_1925` equation for mass conversation.

```{dropdown} The difference between Gaia and SISYPHE
To get specifications beyond the features presented here in the TELEMAC documentation and in the TELEMAC forum, it is useful to know that there has been a predecessor module of Gaia called SISYPHE. Most of the SISYPHE routines are still available in recent TELEMAC versions through Gaia, although with functional enhancements that require adjustments in some keywords.
```

### Coupling Hydro-morphodynamics

A hydro-morphodynamic numerical model can be either **fully coupled** or **decoupled**.

Fully coupled model
: A fully coupled model solves the hydrodynamic {term}`Navier-Stokes equations` simultaneously with sediment transport equations. Bed elevation (i.e., {term}`Topographic change`) is calculated for every timestep, which leads to very **long computation** times.
  *Application range:* Rapid morphodynamic processes, such as hyper-concentrated sediment-laden flows or debris flow.

Decoupled model
: A decoupled model solves morphodynamic equations not iteratively with and optionally not for every hydrodynamic timestep. Thus, a user-defined frequency calculation frequency for morphodynamics can be defined, such as every 2$^{nd}$ or 10$^{th}$ hydrodynamic timestep. Therefore, the active channel bottom is considered fixed when hydrodynamic variables are solved and bed elevation (or {term}`Topographic change`) is calculated at a user-defined frequency and separately (i.e., *decoupled*) from hydrodynamics.
  *Application range:* Most river models, and in particular lake or oceanic models.

## Coupling Gaia and TELEMAC
Gaia can be internally coupled with the hydrodynamic models Telemac2d or TELEMAC-
3D. The following keywords must be included in the Telemac2d or Telemac3d steering files:

`COUPLING WITH : 'GAIA'`

`GAIA STEERING FILE : '<name of the gaia steering file>'`

Since Gaia is not operated fully coupled, the first step is to compute the flow variables with a fixed bed.
Subsequently the discretized sediment equation is solved separately.
The suspended sediment transport processes are computed by the hydrodynamic modules (Telemac2d or Telemac3d), while near-bed, {term}`Bedload` and processes
in the bottom layer are handled by Gaia.

## Mandatory files
The following files are mandatory to simulate morphodynamics:

* the steering files for Gaia and the hydrodynamic module (e.g. [T2D](../numerics/telemac2d)
or [T3D](../numerics/telemac3d)
    - File format : *.cas

* the geometry file
    - File format : *.slf

* the boundary conditions file
    - File format : *.cli

Optional files such as Fortran file (*.f), the reference file (*.slf), but are not featured here.

## Setup of Gaia Steering file
This file contains the necessary information for running a morphodynamic simulation and must contain all parameter values that differ from the default value (as specified in the dictionary file `gaia.dico` and the {{ gaia_ref }}).

It is recommended to orientate on the following 3 categories to set up the Steering-file.

### Define input and output files
All files should be stored in the same folder.

Assign file names to at least the following keywords:

`GEOMETRY FILE : '*.slf'`

`BOUNDARY CONDITIONS FILE : '*.cli'`

`RESULTS FILE : '*.slf'`

`VARIABLES FOR GRAPHIC PRINTOUTS : ''`

### Physical Parameters
Define essential physical parameters such as sediment type, grain sizes, and decide which
transport mechanisms, and formulas to include in your calculation. Consider the following important keywords:

`TYPE OF SEDIMENT : CO; NCO`

`CLASSES SEDIMENT DIAMETERS : 0.0001; 0.1`

`BED LOAD FOR ALL SANDS : YES or NO`

`BED-LOAD TRANSPORT FORMULA FOR ALL SANDS`

`SUSPENSION FOR ALL SANDS : YES or NO`

Specific settling velocities or shields parameters can be defined or calculated directly by GAIA (default).

### Numerical options and parameters
Define which numerical schemes, solvers to use in your calculation. Consider the following important keywords:

`TIDAL FLATS : YES or NO`

`OPTION FOR THE TREATMENT OF TIDAL FLATS`

`SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS`

`FINITE VOLUMES : YES or NO`

`ADVECTION-DIFFUSION SCHEME WITH SETTLING VELOCITY`

`SOLVER FOR DIFFUSION OF SUSPENSION`


## Run Simulation
The simulation is started identically to a hydrodynamic simulation by calling the telemac2d.py script.
Please note that `*_tel.cas` is the hydrodynamic and not the GAIA steering file.

`cd /go/to/dir`

`telemac2d.py *_tel.cas`

However, in the steering file of the hydrodynamic model
the required keywords (see Coupling GAIA and TELEMAC) for the coupling must be present.
