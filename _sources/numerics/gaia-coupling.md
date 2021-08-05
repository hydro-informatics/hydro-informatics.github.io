# Introduction and Coupling

```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to **complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials**.

The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Terminology
A hydro-morphodynamic simulation implies modeling runoff-driven **{term}`Sediment transport`** processes. The previous sections in this eBook focus on hydrodynamics defined as *the study of liquids in motion* and this section focusses on **morphodynamics** defined as **the study of time-dependent changes in the forms of alluvial beds and their underlying processes**.

## Sediment Transport, Gaia, and Sisyphe

TELEMAC has a dedicated module called Gaia for this purpose and Gaia enables modelling sediment transport and morphological evolution (i.e., {term}`Topographic change`) in rivers, lakes, and estuaries. Gaia comes with particular routines to consider spatio-temporal variation of grain sizes, grading curves, and sediment transport modes in the form of **{term}`Bedload` (coarse sediment)** and/or **{term}`Suspended load` (fine sediment)**. {term}`Bedload` is calculated by solving semi-empiric equations, such as the {cite:t}`meyer-peter_formulas_1948` formula (read more later in this tutorial). {term}`Suspended load` is modeled by solving the {term}`Advection`-{term}`Diffusion` equations and additionally requires closures for sediment erosion and deposition fluxes. Sediment is further distinguished between very fine, **cohesive** sediment and coarser, **non-cohesive** sediment. In addition, Gaia accounts for bed evolution through an iterative solution of the {term}`Exner equation` {cite:p}`exner_uber_1925` for mass conversation. {numref}`Figure %s <bl-vs-sl>` qualitatively illustrates the two basic modes of sediment transport in the form of suspended load and bedload.

```{figure} https://github.com/Ecohydraulics/media/raw/master/png/sediment-transport.png
:alt: sediment transport bedload suspended load
:name: bl-vs-sl

Qualitative representation of two modes of sediment transport. On the left: suspended load in the form of fine particles moving with the bulk flow; on the right: bedload in the form of particles rolling, jumping, or sliding on the riverbed.
```

The recruitment of sediment for both suspended load and bedload transport requires a detailed look at the riverbed, which will be provided later in the section on the definition of {ref}`the riverbed composition and the active layer <gaia-active-lyr>`.


```{dropdown} The difference between Gaia and SISYPHE
To get specifications beyond the features presented here in the TELEMAC documentation and in the TELEMAC forum, it is useful to know that there has been a predecessor module of Gaia called SISYPHE. Most of the SISYPHE routines are still available in recent TELEMAC versions through Gaia, although with functional enhancements that require adjustments in some keywords. Read more in the {{ gaia }} in Appendix 8.1 and in the [gaia.dico](http://svn.opentelemac.org/svn/opentelemac/tags/v8p2r1/sources/gaia/gaia.dico) file (lives in the TELEMAC installation directory: `telemac/v8px/sources/gaia/gaia.dico`).
```


(tm-coupling)=
## Coupling TELEMAC and Gaia

The morphodynamics module Gaia can be internally **coupled** with the hydrodynamic models Telemac2d (solving the {term}`Shallow water equations`) or Telemac3d (solving the Reynolds-averaged {term}`Navier-Stokes equations`). This section explains different types of coupling Telemac2d/Telemac3d (hydrodynamics) with Gaia (morphodynamics) and how coupling can be implement in the TELEMAC software suite.

### Coupling Hydrodynamics (Telemac2d/3d) and Morphodynamics (Gaia)

A hydro-morphodynamic numerical model can be either **fully coupled** or **decoupled**.

Fully coupled model
: A fully coupled model solves the hydrodynamic {term}`Navier-Stokes equations` simultaneously with sediment transport equations. Bed elevation (i.e., {term}`Topographic change`) is calculated for every timestep, which leads to very **long computation** times. In addition to coupling of gravity-driven hydrodynamics (i.e., bulk flow along valley slopes), {term}`Sediment transport`, and {term}`Topographic change`, a model can also be coupled with (surface) wave hydrodynamics.

  *Application range:* Rapid morphodynamic processes, such as hyper-concentrated sediment-laden flows or debris flow.

Decoupled model
: A decoupled model solves morphodynamic equations not iteratively with and optionally not for every hydrodynamic timestep. Thus, a user-defined frequency calculation frequency for morphodynamics can be defined, such as every 2$^{nd}$ or 10$^{th}$ hydrodynamic timestep. Therefore, the active channel bottom is considered fixed when hydrodynamic variables are solved and bed elevation (or {term}`Topographic change`) is calculated at a user-defined frequency and separately (i.e., *decoupled*) from hydrodynamics.

  *Application range:* Most river models, and in particular lake or oceanic models.


### File Requirements for Coupling Gaia

In addition to the standard Telemac2d steering, boundaries and geometry mesh file, coupling Gaia requires an own steering (`*.cas`) file that needs to be referenced in the main steering file of the simulation. To this end, **create a new folder for the Gaia tutorial** (e.g., called `/gaia2d-tutorial/`), copy the dry-initialized steady2d simulation and results files, and **create a new Gaia steering file** (e.g., called `gaia-morphodynamics.cas`). Thus, the following files should live in the modeling folder for this tutorial :

* The computational mesh in the form of [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* The boundary definitions in the form of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* The results of the dry-initialized steady 2d model run for 35 m$^3$/s in the form of [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) (result of the {ref}`dry bonus run <tm2d-dry>` ending at `T=15000`).
* A Telemac2d steering file for this tutorial, building on the dry-initialized steady2d steering file, and called [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* The new [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas) steering file.

```{admonition} Gaia simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/).
```

### Couple Gaia in the Hydrodynamics Steering File

To programmatically implement the coupling of Gaia with a Telemac2d/Telemac3d simulation, at least five keywords should be defined in addition to the keywords presented in the {ref}`steady2d chapter <telemac2d-steady>`. The first additional keyword is the baseline for any coupling with Telemac2d or Telemac3d steering file:

```fortran
/ steady2d-gaia.cas
COUPLING WITH : 'GAIA'
```

```{admonition} steady2d-gaia.cas is the hydrodynamics (Telemac2d or Telemac3d) steering file
:class: note
In this tutorial the hydrodynamics (Telemac2d or Telemac3d) steering file is referred to as [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas) and the morphodynamics (Gaia) steering file is referred to as [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).
```


Ultimately, the **GAIA STEERING FILE** keyword links the above-created `gaia-morphodynamics.cas` in the Telemac2d (or Telemac3d) hydrodynamics steering file:

```fortran
/ steady2d-gaia.cas
/ ...
GAIA STEERING FILE : gaia-morphodynamics.cas
```

### Hotstart

This tutorial builds on the results of the {ref}`dry-initialized steady2d model <tm2d-dry>` because Gaia is design as a decoupled model (see the {ref}`above definitions <tm-coupling>). Using a former calculations result for model initialization is called **hotstart** for which TELEMAC requires a results file from a previous simulation. For this purpose, place the dry-initialized steady2d results file in the simulation folder ([download r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf)) and setup the hotstart in the Telemac2d steering file for this tutorial with the following keywords:

```fortran
/ steady2d-gaia.cas
/ ...
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

The **INITIAL TIME SET TO ZERO** keyword resets the simulation time to `0`. In addition, make sure that all **INITIAL CONDITIONS** keywords are commented out with a **/** (alternatively delete these lines from steady2d-gaia.cas):

```fortran
/ steady2d-gaia.cas
/ ...
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
```

The dry-initialized steering file also prescribes flowrates and elevations, that need to be **kept in steady2d-gaia.cas**. Therefore, make sure that the flowrate and elevation prescription keywords are activated:

```fortran
/ steady2d-gaia.cas
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
PRESCRIBED ELEVATIONS : 374.805626;371.33
```
