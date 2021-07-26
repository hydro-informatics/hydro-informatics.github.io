(tm-gaia)=
#  Gaia (Morphodynamics)

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

### Sediment Transport and Gaia?
TELEMAC has a dedicated module called Gaia for this purpose and Gaia enables modelling sediment transport and morphological evolution (i.e., {term}`Topographic change`) in rivers, lakes, and estuaries. Gaia comes with particular routines to consider spatio-temporal variation of grain sizes, grading curves, and sediment transport modes in the form of **{term}`Bedload` (coarse sediment)** and/or **{term}`Suspended load` (fine sediment)**. {term}`Bedload` is calculated by solving a semi-empiric equations, such as  the {cite:t}`meyer-peter_formulas_1948` formula (read more later in this tutorial). {term}`Suspended load` is modeled by solving the {term}`Advection`-{term}`Diffusion` equations and additionally requires closures for sediment erosion and deposition fluxes . Sediment is further distinguished between very fine, **cohesive** sediment and coarser, **non-cohesive** sediment. In addition, Gaia accounts for bed evolution through an iterative solution of the {term}`Exner equation` {cite:p}`exner_uber_1925` for mass conversation.

```{dropdown} The difference between Gaia and SISYPHE
To get specifications beyond the features presented here in the TELEMAC documentation and in the TELEMAC forum, it is useful to know that there has been a predecessor module of Gaia called SISYPHE. Most of the SISYPHE routines are still available in recent TELEMAC versions through Gaia, although with functional enhancements that require adjustments in some keywords. Read more in the {{ gaia }} in Appendix 8.1.
```

(tm-coupling)=
## Gaia and TELEMAC

The morphodynamics module Gaia can be internally **coupled** with the hydrodynamic models Telemac2d (solving the {term}`Shallow water equations`) or Telemac3d (solving the Reynolds-averaged {term}`Navier-Stokes equations`). This section explains different types of coupling Telemac2d/Telemac3d (hydrodynamics) with Gaia (morphodynamics) and how coupling can be implement in the TELEMAC software suite.

### Coupling Hydro-morphodynamics

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

### Link Gaia in the Hydrodynamics Steering File

To programmatically implement the coupling of Gaia with a Telemac2d/Telemac3d simulation, at least five keywords should be defined in addition to the keywords presented in the {ref}`steady2d chapter <telemac2d-steady>`. The first additional keyword is the baseline for any coupling with Telemac2d or Telemac3d steering file:

```fortran
/ steady2d-gaia.cas
COUPLING WITH : 'GAIA'
```

```{admonition} steady2d-gaia.cas is the hydrodynamics (Telemac2d or Telemac3d) steering file
:class: note
In this tutorial the hydrodynamics (Telemac2d or Telemac3d) steering file is referred to as [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas) and the morphodynamics (Gaia) steering file is referred to as [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).
```

This tutorial builds on the results of the {ref}`dry-initialized steady2d model <tm2d-dry>` because Gaia is design as a decoupled model (see the {ref}`above definitions <tm-coupling>). Using a former calculations result for model initialization is called **hotstart** for which TELEMAC requires a results file from a previous simulation. For this purpose, place the dry-initialized steady2d results file in the simulation folder ([download r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf)) and setup the hotstart in the Telemac2d steering file for this tutorial with the following keywords:

```fortran
/ steady2d-gaia.cas
/ ...
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

The `INITIAL TIME SET TO ZERO` keyword resets the simulation time to `0`.

Ultimately, the **GAIA STEERING FILE** keyword links the above-created `gaia-morphodynamics.cas` in the Telemac2d (or Telemac3d) hydrodynamics steering file:

```fortran
/ steady2d-gaia.cas
/ ...
GAIA STEERING FILE : gaia-morphodynamics.cas
```

## Gaia Steering

*This section is partially based on descriptions from {{ mouris }}.*

The following instructions refer to the setup of the above-created Gaia steering file (`gaia-morphodynamics.cas`), which requires some mandatory parameters and enables many more optional keywords settings. An overview of all keywords can be found in the {{ gaia_ref }} and the dictionary file `/telemac/v8p2/sources/gaia/gaia.dico`. Similar to the Telemac2d or Telemac3d hydrodynamics steering file, the Gaia steering file requires definitions of general (file-related), physical, and numerical parameters.

### General Parameters

The general parameters defining mandatory input and output files resemble the hydrodynamic steering file. Input files can also be the same as used in the hydrodynamics steering file. Therefore, **define** the **[qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf)** from the {ref}`pre-processing <slf-prepro-tm>` **as geometry file** and **[boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)** as **boundary conditions file**. However, the Gaia `RESULTS FILE` keyword should differ from the `RESULTS FILE` keyword in the hydrodynamic steering file.

```fortran
/ gaia-morphodynamics.cas
/
/ COMPUTATION ENVIRONMENT
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE : qgismesh.slf
RESULTS FILE : rGaia-steady2d.slf
MASS-BALANCE : YES
```

Graphical output variables related to sediment transport can be defined with the `VARIABLES FOR GRAPHIC PRINTOUTS` keyword for {term}`Bedload` and/or {term}`Suspended load` with the following list-options:

* `E` for bottom evolution in (m)
* `M` for the magnitude (length) of the bi-directional (i.e., $x$ and $y$ directions) unit solid transport (bedload, suspended load, and dissolved tracers) $\boldsymbol{q_s}$ (read more in the definition of the {term}`Exner equation`) in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `N` for unit solid transport (bedload, suspended load, and dissolved tracers) in $x$-direction $\boldsymbol{q_s}\cdot\cos\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$) where  $\alpha$ is the angle between the longitudinal channel ($x$) axis and the solid transport vector $\boldsymbol{q_s}$.
* `P` for unit solid transport (bedload, suspended load, and dissolved tracers) in $y$-direction $\boldsymbol{q_s}\cdot\sin\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `QSBL` `M` for the magnitude (length) of the bi-directional (i.e., $x$ and $y$ directions) unit **bedload (only)** transport $\boldsymbol{q_b}$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `TOB` for bed shear stress in (N$\cdot$m$^{-2}$)

The parameters `M` and `QSBL` will result in the same output if no suspended load is simulated. To output multiple parameters, set the graphical printouts keyword as follows:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : E,M,N,P,QSBL,TOB,U,V
```

(gaia-bc)=
### Boundary Conditions

The boundary conditions in Gaia work similarly as for hydrodynamics and can be added to the existing boundaries file through modification of the **LITBOR** definition. For this purpose, open the boundary conditions file [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) in a {ref}`text editor <npp>` and modify the eighth entry of all open liquid boundary lines. Counting line entries sounds like a tedious task, but is fairly straightforward in practice:

* The first three entries of the upstream and downstream boundaries are **LIHBOR** (water depth), **LIUBOR** (flow velocity in $x$-direction), and **LIVBOR** (flow velocity in $y$-direction). These three values were set to `5` in the {ref}`dry-initialized steady2d simulation<tm2d-dry>`, which defines the upstream and downstream boundaries with **prescribed H and Q**.
* The following four entries are `0.000` (for HBOR, UBOR, VBOR, and AUBOR) and would prescribe (assign) float values directly in the boundary file (deactivated through the `0.000` setting).
* The eighth entry is the **LITBOR** type, which currently set to `2` (closed wall) and has to be modified for use with Gaia:
  * Open the upstream and downstream boundary for sediment transport by **setting LITBOR to `4`** (prescribed flowrate). This setting is useful for prescribing sold flowrates either in the steering file or with a liquid boundaries file as described in the {ref}`unsteady (quasi-steady) tutorial <tm2d-liq-file>`.
  * Alternatively, a value of `5` can be assigned for prescribing equilibrium solid flowrates, which also requires that EBOR is set to `0.0` (no change of bottom elevation).



### Physical Parameters
Define essential physical parameters such as sediment type, grain sizes, and decide which
transport mechanisms, and formulas to include in your calculation. Consider the following important keywords:

TYPE OF SEDIMENT :
BED LOAD FOR ALL SANDS :
SUSPENSION FOR ALL SANDS :
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS :

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
