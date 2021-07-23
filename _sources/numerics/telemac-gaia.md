(tm-gaia)=
# Morphodynamics 2d with Gaia

```{figure} ../img/hydro-morphodynamics.png
:alt: hydrodynamics morphodynamics
:name: hydro-morphodynamics

A morphodynamically active tributary of Cache Creek (California, USA).
```

This chapter guides through modelling {term}`Sediment transport` and related phenomena in rivers (morphodynamics) with Telemac2d and the Gaia module. Notably, a simple steady2d example demonstrates how {term}`Sediment transport` in the form of bedload can be modeled with the TELEMAC software suite.

## Under construction. Expected release in the next 12 months.

Thank you for your patience.


```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to **complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials**.

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
To get specifications beyond the features presented here in the TELEMAC documentation and in the TELEMAC forum, it is useful to know that there has been a predecessor module of Gaia called SISYPHE. Most of the SISYPHE routines are still available in recent TELEMAC versions through Gaia, although with functional enhancements that require adjustments in some keywords. Read more in the {{ gaia }} in Appendix 8.1.
```

### Coupling Hydro-morphodynamics

A hydro-morphodynamic numerical model can be either **fully coupled** or **decoupled**.

Fully coupled model
: A fully coupled model solves the hydrodynamic {term}`Navier-Stokes equations` simultaneously with sediment transport equations. Bed elevation (i.e., {term}`Topographic change`) is calculated for every timestep, which leads to very **long computation** times. In addition to coupling of gravity-driven hydrodynamics (i.e., bulk flow along valley slopes), {term}`Sediment transport`, and {term}`Topographic change`, a model can also be coupled with (surface) wave hydrodynamics.

  *Application range:* Rapid morphodynamic processes, such as hyper-concentrated sediment-laden flows or debris flow.

Decoupled model
: A decoupled model solves morphodynamic equations not iteratively with and optionally not for every hydrodynamic timestep. Thus, a user-defined frequency calculation frequency for morphodynamics can be defined, such as every 2$^{nd}$ or 10$^{th}$ hydrodynamic timestep. Therefore, the active channel bottom is considered fixed when hydrodynamic variables are solved and bed elevation (or {term}`Topographic change`) is calculated at a user-defined frequency and separately (i.e., *decoupled*) from hydrodynamics.

  *Application range:* Most river models, and in particular lake or oceanic models.

## Coupling Gaia and TELEMAC

*This section is partially based on descriptions from {{ mouris }}.*

### Activate Gaia

Gaia can be internally coupled with the hydrodynamic models Telemac2d (solving the {term}`Shallow water equations`) or Telemac3d (solving the Reynolds-averaged {term}`Navier-Stokes equations`). To this end, the following keyword must be added to a Telemac2d or Telemac3d steering file:

```fortran
COUPLING WITH : 'GAIA'
```

This tutorial builds on the results of the {ref}`dry-initialized steady2d model <tm2d-dry>` to significantly speed up calculations. This type of model initialization is called **hotstart** and in the case of Telemac requires a results file from a previous simulation. For this purpose, place the dry-initialized steady2d results file in the simulation folder (download [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf)) and setup the hotstart in the Telemac2d steering file for this tutorial with the following keywords:

```fortran
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

The `INITIAL TIME SET TO ZERO` keyword resets the simulation time to `0`.

### Gaia File Requirements and Steering

Gaia requires an own steering (`*.cas`) file that needs to be referenced in the main steering file of the simulation. Thus, in addition to the standard Telemac2d steering, boundaries and geometry mesh file, **create a new steering file in the modeling folder** and call it, for example, **gaia4bedload.cas**. The following files should now be living in the modeling folder for this tutorial (e.g., called `/gaia2d-tutorial/`):

* The computational mesh in the form of [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* The boundary definitions in the form of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* The results of the dry-initialized steady 2d model run for 35 m$^3$/s in the form of [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) (result of the {ref}`dry bonus run <tm2d-dry>` ending at `T=15000`).
* A Telemac2d steering file for this tutorial, building on the dry-initialized steady2d steering file, and called [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* The new [gaia4bedload.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia4bedload.cas) steering file.


```{admonition} Unsteady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/).
```

`GAIA STEERING FILE : gaia4bedload.cas`

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


```{admonition} Get inspired by the TELEMAC examples
The installation of TELEMAC comes with examples for Gaia applied to Telemac2d and Telemac3d models, which can be found in:

`/telemac/v8p2/examples/gaia/`

Because Gaia is the successor of SISYPHE, also the SISYPHE examples are useful, in particular with regards to multi-grain size modeling:

`/telemac/v8p2/examples/sisyphe/`

```
