# Introduction and Coupling

```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to **complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials**.

The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`) - earlier versions will not recognize some of the keywords used in this eBook.
* {ref}`QGIS <qgis-install>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Terminology
A hydro-morphodynamic simulation implies modeling runoff-driven **{term}`Sediment transport`** processes. The previous sections in this eBook focus on hydrodynamics defined as *the study of liquids in motion* and this section focuses on **morphodynamics** defined as **the study of time-dependent changes in the forms of alluvial beds and their underlying processes**.

(gaia-seditrans)=
## Sediment Transport, Gaia, and Sisyphe

TELEMAC has a dedicated module called Gaia for modeling morphodynamics. Gaia enables modeling sediment transport and morphological evolution (i.e., {term}`Topographic change`) in rivers, lakes, and estuaries. It comes with particular routines to consider a spatio-temporal variation of grain sizes, grading curves, and riverbed layering for simulating sediment transport in the form of **{term}`Bedload` (coarse sediment)** and/or **{term}`Suspended load` (fine sediment)**. {term}`Bedload` is calculated by solving semi-empiric equations, such as the {cite:t}`meyer-peter_formulas_1948` formula (read more later in this tutorial). {term}`Suspended load` is modeled by solving the {term}`Advection`-{term}`Diffusion` equations, require closures for sediment erosion and deposition fluxes. {numref}`Figure %s <bl-vs-sl>` qualitatively illustrates the two basic modes of sediment transport in the form of suspended load and bedload.

```{figure} https://github.com/Ecohydraulics/media/raw/master/png/sediment-transport.png
:alt: sediment transport bedload suspended load
:name: bl-vs-sl

Qualitative representation of two modes of sediment transport. On the left: suspended load in the form of fine particles moving with the bulk flow; on the right: bedload in the form of particles rolling, jumping, or sliding on the riverbed.
```

Sediment is further distinguished between very fine, **cohesive** sediment and coarser, **non-cohesive** sediment. In addition, Gaia accounts for bed evolution through an iterative solution of the {term}`Exner equation` {cite:p}`exner_uber_1925` for mass conversation.

The recruitment of sediment for both suspended load and bedload transport requires a detailed look at the riverbed, which will be provided later in the section on the definition of {ref}`the riverbed composition and the active layer <gaia-active-lyr>`.

```{dropdown} The difference between Gaia and SISYPHE
To get specifications beyond the features presented here in the TELEMAC documentation and the TELEMAC forum, it is useful to know that there has been a predecessor module of Gaia called SISYPHE. SISYPHE and its routines are still available in recent TELEMAC versions in addition to and through Gaia. Although the use of SISYPHE routines through Gaia with functional enhancements require adjustments of some keywords. Read more in the {{ gaia }} in Appendix 8.1 and in the [gaia.dico](http://svn.opentelemac.org/svn/opentelemac/tags/v8p2r1/sources/gaia/gaia.dico) file (lives in the TELEMAC installation directory: `telemac/v8p2/sources/gaia/gaia.dico`).
```

(tm-coupling)=
## Coupling TELEMAC and Gaia

The morphodynamics module Gaia can be internally **coupled** with the hydrodynamic models Telemac2d (solving the {term}`Shallow water equations`) or Telemac3d (solving the Reynolds-averaged {term}`Navier-Stokes (RANS) equations <Navier-Stokes equations>`). This section explains types of coupling Telemac2d/Telemac3d (hydrodynamics) with Gaia (morphodynamics).

### Coupling Hydrodynamics (Telemac2d/3d) and Morphodynamics (Gaia)

A hydro-morphodynamic numerical model can be either **fully coupled** or **decoupled**.

Fully coupled model
: A fully coupled model solves the hydrodynamic {term}`Navier-Stokes equations` simultaneously with sediment transport equations (i.e., erosion and deposition fluxes from and to the riverbed through the {term}`Exner equation`). Bed elevation (i.e., {term}`Topographic change`) is calculated for every timestep, which leads to **long computation** times. In addition to the coupling of gravity-driven hydrodynamics (i.e., bulk flow along valley slopes), {term}`Sediment transport`, and {term}`Topographic change`, a model can also be coupled with (surface) wave hydrodynamics.

  *Application range:* Rapid morphodynamic processes, such as hyper-concentrated sediment-laden flows or debris flow.

Decoupled model
: A decoupled model solves morphodynamic (i.e., the {term}`Exner equation`) not iteratively with, and optionally, not for every hydrodynamic timestep. Thus, a user-defined frequency calculation frequency for morphodynamics can be set, such as every 2$^{nd}$ or 10$^{th}$ hydrodynamic timestep. Therefore, the active channel bottom is considered fixed when hydrodynamic variables are solved and bed elevation (or {term}`Topographic change`) is calculated at a user-defined frequency and separately (i.e., *decoupled* or *asynchronous*) from hydrodynamics.

  *Application range:* Most river models, and in particular, lake or oceanic models.

Gaia is designed as a de-coupled model where the morphodynamic calculation frequency is a function of a *coupling period* parameter (read more in section 5.1.2 in the {{ gaia }}). Note that the {{ gaia }} (section 1.1.3) says that Gaia is decoupled, though it successively solves hydrodynamics and morphodynamics for every timestep. Moreover, the coupling period is currently only a user-defined parameter with reference to SISYPHE, which can be modified in the hydrodynamic steering file with:

```fortran
/steady2d-gaia.cas
/...
COUPLING PERIOD FOR SISYPHE : 1 / integer
```

To get updates on the coupling period and modes of Gaia, follow the [discussion in the TELEMAC Forum](http://www.opentelemac.org/index.php/kunena/17-sisyphe/13413-coupling-period-for-gaia#38974).

### File Requirements for Coupling Gaia

In addition to the standard Telemac2d steering, boundaries, and geometry mesh files, coupling hydrodynamics with Gaia requires a new steering (`*.cas`) file that needs to be referenced in the main steering file of the simulation. To this end, **create a new folder for the Gaia tutorial** (e.g., called `/gaia2d-tutorial/`), copy the {ref}`dry-initialized steady2d simulation and results files <tm2d-dry>` (or clone the [gaia2d-tutorial repository](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/)), and **create a new Gaia steering file** (e.g., called `gaia-morphodynamics.cas`). Thus, the following files should live in the modeling folder for this tutorial:

* The computational mesh in the form of [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* The boundary definitions in the form of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* The results of the dry-initialized steady 2d model run for 35 m$^3$/s in the form of [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) ({ref}`dry steady run <tm2d-dry>` ending at `T=15000`).
* A Telemac2d steering file for this tutorial, building on the dry-initialized steady2d steering file and called [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* The new [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas) steering file.

```{admonition} Gaia simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/).
```

### Couple Gaia in the Hydrodynamics Steering File

To programmatically implement the coupling of Gaia with a Telemac2d/Telemac3d simulation, a couple of new keywords need to be defined in addition to the keywords explained in the {ref}`steady2d chapter <telemac2d-steady>`. The first additional keyword is the baseline for any coupling with Telemac2d or Telemac3d steering file:

```fortran
/ steady2d-gaia.cas
COUPLING WITH : 'GAIA'
```

```{admonition} steady2d-gaia.cas is the hydrodynamics (Telemac2d or Telemac3d) steering file
:class: note
In this tutorial the hydrodynamics (Telemac2d or Telemac3d) steering file is referred to as [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas) and the morphodynamics (Gaia) steering file is referred to as [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).
```

In addition, the **GAIA STEERING FILE** keyword links the above-created `gaia-morphodynamics.cas` in the Telemac2d (or Telemac3d) hydrodynamics steering file:

```fortran
/ steady2d-gaia.cas
/ ...
GAIA STEERING FILE : gaia-morphodynamics.cas
```

(gaia-hotstart)=
### Hotstart

This tutorial builds on the results of the {ref}`dry-initialized steady2d model <tm2d-dry>` because Gaia is designed as a decoupled model (see the {ref}`above definitions <tm-coupling>). Using a former simulation result for model initialization is called **hotstart** for which TELEMAC requires, of course, a results file from a previous simulation. For this purpose, make sure that the dry-initialized steady2d results file in the simulation folder ([download r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf)). Then **define the hotstart in the Telemac2d steering file** with the following keywords:

```fortran
/ steady2d-gaia.cas
/ ...
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

The **INITIAL TIME SET TO ZERO** keyword resets the simulation time to `0`. Next, make sure that all **INITIAL CONDITIONS** keywords are commented out with a **/** (alternatively delete these lines from steady2d-gaia.cas):

```fortran
/ steady2d-gaia.cas
/ ...
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
```

```{admonition} Bottom elevation must be available in the hotstart geometry (SLF)
:class: warning
The bottom elevation must be printed out in the results file of the simulation used for the hotstart. To this end, make sure that the list of values for the **VARIABLES FOR GRAPHIC PRINTOUTS** keyword contains `B` as indicated in the {ref}`explanations for the setup of the dry-initialized model <tm2d-dry>`.
```

The dry-initialized steering file prescribes flowrates and elevations, which requires **modifications in steady2d-gaia.cas** to **prescribed Q only**. The reason for the Q-only prescription is that with Gaia, we want to model-predict changes in water depths and riverbed elevation, which means that the water surface elevation must not be constrained (i.e., not prescribed) as a boundary condition. Thus, the setup of boundary conditions for Gaia also requires slight modifications of the boundary (`*.cli`) file(s), which will be explained in the next section on the {ref}`Basic Setup of Gaia <gaia-bc>`. To this end, make sure that in the hydrodynamics steering file **only the flowrate prescription keyword is activated** and the elevation prescription is deactivated (comment out with `/`):

```fortran
/ steady2d-gaia.cas
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;371.33
```

### Control Sections

Control sections are sequences of node numbers (or node coordinates) at which TELEMAC sums up fluxes, for instance, to verify inflow and outflow mass balances. The unsteady simulation section provides detailed instructions for {ref}`defining control sections <tm-control-sections>` and this tutorial re-uses the control sections file from the unsteady simulation (**[download control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/control-sections.txt)**).

````{dropdown} Expand to view the file *control-sections.txt*
```
# control sections steady2d
2 -1
Inflow_boundary
144 32
Outflow_boundary
34 5
```
````

To use the control sections for the Gaia simulation add the following to the **hydrodynamics** steering file:

```
/ steady2d-gaia.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

Thus, re-running the simulation will write the fluxes across the two defined control sections to a file called *r-control-flows.txt*.

### Hydrodynamic Steering Summary

With the above adaptions and using a simulation length of `30000` timesteps (to observed morphodynamic evolution) with a graphical printout period of every `5000` timesteps (to reduce the output file size), the final hydrodynamic steering file should look like this:

```fortran
/ steady2d-gaia.cas
/
TITLE : 'gaia2d steady'
/
COMPUTATION CONTINUED : YES / build on top of a steady flow initialization
PREVIOUS COMPUTATION FILE : r2dsteady.slf / here - 35 CMS initialization after t 15000
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
/
COUPLING WITH : 'GAIA'
GAIA STEERING FILE : gaia-morphodynamics.cas
/
/ DEFAULTS FROM STEADY2D
/
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady-gaia.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
/
/ CONTROL SECTIONS
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
/
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
TIME STEP : 1.
NUMBER OF TIME STEPS : 30000
GRAPHIC PRINTOUT PERIOD : 5000
LISTING PRINTOUT PERIOD : 5000
/
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/ General solver parameters from section 7.1
DISCRETIZATIONS IN SPACE : 11;11
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
ADVECTION : YES
/
/ FINITE ELEMENT SCHEME PARAMETERS - section 7.2.1 in the manual
/------------------------------------------------------------------
TREATMENT OF THE LINEAR SYSTEM : 2 / default is 2 - use 1 to avoid smoothened results
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION OF VELOCITY : 1. / v8p2 default
IMPLICITATION COEFFICIENT OF TRACERS : 0.6 / v8p2 default
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
/ MASS-LUMPING FOR WEAK CHARACTERISTICS : 1. / enabling leads to weak characteristics
SUPG OPTION : 0;0;2;2  / classic supg for U and V
/
/ SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
/
/ TIDAL FLATS  - see section 7.5
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats - default is 1
/
/ MATRIX HANDLING - see section 7.6
MATRIX STORAGE : 3 / default is 3
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;0.
/
/ Type of velocity profile can be 1-constant normal profile (default) and (cli) 4-vector is proportional to root (water depth, only for Q)
VELOCITY PROFILES : 4;1
/
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
/
/ STABILITY CONTROLS
/ ------------------------------------------------------------------
PRINTING CUMULATED FLOWRATES : YES
/
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/
DIFFUSION OF VELOCITY : YES / default is YES
TURBULENCE MODEL : 3
/
&ETA
```
