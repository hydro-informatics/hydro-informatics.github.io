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

## Gaia Setup

*This section is partially based on descriptions from {{ mouris }}.*

The following instructions refer to the setup of the above-created Gaia steering file (`gaia-morphodynamics.cas`), which requires some mandatory parameters and enables many more optional keywords settings. An overview of all keywords can be found in the {{ gaia_ref }} and the dictionary file `/telemac/v8p2/sources/gaia/gaia.dico`. Similar to the Telemac2d or Telemac3d hydrodynamics steering file, the Gaia steering file requires definitions of general (file-related), physical, and numerical parameters.

### General Parameters

The general parameters defining mandatory input and output files resemble the hydrodynamic steering file. Input files can also be the same as used in the hydrodynamics steering file. Therefore, **define** the **[qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf)** from the {ref}`pre-processing <slf-prepro-tm>` **as geometry file** and **boundaries-gaia.cli** as **boundary conditions file**. The boundary conditions file will be created based on the hydrodynamics [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) in the section on {ref}`boundary conditions for Gaia <gaia-bc>`. The Gaia **RESULTS FILE** keyword should also differ from the RESULTS FILE keyword in the hydrodynamic steering file.

```fortran
/ gaia-morphodynamics.cas
/
/ COMPUTATION ENVIRONMENT
/
BOUNDARY CONDITIONS FILE : boundaries-gaia.cli
GEOMETRY FILE : qgismesh.slf
RESULTS FILE : rGaia-steady2d.slf
MASS-BALANCE : YES
```

Graphical output variables related to sediment transport can be defined with the **VARIABLES FOR GRAPHIC PRINTOUTS** keyword for {term}`Bedload` and/or {term}`Suspended load` with the following list-options:

* `B` for bottom elevation in (m a.s.l.)
* `E` for bottom evolution in (m)
* `F` for {term}`Froude number` (-)
* `M` for the magnitude (length) of the bi-directional (i.e., $x$ and $y$ directions) unit solid transport (bedload, suspended load, and dissolved tracers) $\boldsymbol{q_s}$ (read more in the definition of the {term}`Exner equation`) in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `MU` for the skin friction coefficient (depends on the {ref}`friction law <tm2d-friction>` in the hydrodynamic steering file)
* `N` for unit solid transport (bedload, suspended load, and dissolved tracers) in $x$-direction $\boldsymbol{q_s}\cdot\cos\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$) where  $\alpha$ is the angle between the longitudinal channel ($x$) axis and the solid transport vector $\boldsymbol{q_s}$.
* `P` for unit solid transport (bedload, suspended load, and dissolved tracers) in $y$-direction $\boldsymbol{q_s}\cdot\sin\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `QSBL` `M` for the magnitude (length) of the bi-directional (i.e., $x$ and $y$ directions) unit **bedload (only)** transport $\boldsymbol{q_b}$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `R` for the non-erodible bottom (?)
* `S` for water surface elevation in (m a.s.l.)
* `TOB` for bed shear stress in (N$\cdot$m$^{-2}$)

The parameters `M` and `QSBL` will result in the same output if no suspended load is simulated. In addition, also Sisyphe printout parameters may be used according to the definitions in section 1.2.4 in the {{ sis }}. To output multiple parameters, set the graphical printouts keyword as follows:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : E,M,N,P,QSBL,TOB,U,V
```

(gaia-bc)=
### Boundary Conditions

The boundary conditions in Gaia work similarly as for hydrodynamics and can be derived from the hydrodynamics [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) file.

````{admonition} Recall the structure of the hydrodynamics boundaries.cli file
:class: tip, dropdown
The [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) file has 13 variables per line, which are separated with a `space` and this is how the file head looks like:

```
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000         138           1   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9836           2   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9838           3   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9194           4   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9827           5   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9828           6   #
...
```
````

{numref}`Table %s <tab-gaia-bc>` shows the variables of a Gaia boundary conditions files compared with the hydrodynamic Telemac2d/3d [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) file.

````{dropdown} View the Cross-comparison Table of Boundary variables and types in Telemac2d/3d and Gaia
```{list-table} Boundary variables and types in Telemac2d/3d and Gaia.
:header-rows: 1
:name: tab-gaia-bc

* - Variable no.<br>
  - Flag<br>
  - Telemac2d/3d<br>
    <small>*parameter*</small>
  - Gaia<br>
    <small>*parameter*</small>

* - 1
  - boundary type
  - LIHBOR<br>
    <small>*water depth*</small>
  - LIHBOR<br>
    <small>*water depth*</small>

* - 2
  - boundary type
  - LIUBOR<br>
    <small>*$x$-flowrate or $u$*</small>
  - LIQBOR<br>
    <small>*sediment load*</small>

* - 3
  - boundary type
  - LIVBOR<br>
    <small>*$y$-flowrate or $v$*</small>
  - LIVBOR<br>
    <small>*velocity*</small>

* - 4
  - Prescription
  - HBOR<br>
    <small>*water depth*</small>
  - Q2BOR<br>
    <small>*sediment load*</small>

* - 5
  - Prescription
  - UBOR<br>
    <small>*$x$-flowrate or $u$*</small>
  - UBOR<br>
    <small>*$x$-flowrate or $u$*</small>

* - 6
  - Prescription
  - VBOR<br>
    <small>*$y$-flowrate or $v$*</small>
  - VBOR<br>
    <small>*$y$-flowrate or $v$*</small>

* - 7
  - Prescription
  - AUBOR<br>
    <small>*wall friction*</small>
  - AUBOR<br>
    <small>*wall friction*</small>

* - 8
  - boundary type
  - LITBOR<br>
    <small>*tracer*</small>
  - LIEBOR (LICBOR)<br>
    <small>*bottom elevation*</small>

* - 9
  - Prescription
  - TBOR<br>
    <small>*tracer*</small>
  - EBOR (CBOR)<br>
    <small>*bottom elevation*</small>

* - 10
  - Prescription
  - ATBOR<br>
    <small>*heat fluxes*</small>
  - ATBOR<br>
    <small>*heat fluxes*</small>

* - 11
  - Prescription
  - BTBOR<br>
    <small>*heat fluxes*</small>
  - BTBOR<br>
    <small>*heat fluxes*</small>

* - 12
  - Global Node ID
  - N<br>
    <small>*Selafin mesh*</small>
  - N<br>
    <small>*Selafin mesh*</small>

* - 13
  - Local Node ID
  - K <br><small>*boundary file*</small>
  - K <br><small>*boundary file*</small>

```
````

The boundary type variables (no. 1, 2, 3, and 8) listed in {numref}`Tab. %s <tab-gaia-bc>` can take the integer values `2` (closed wall), `4` (free Neumann-type boundary), `5` (Dirichlet-type prescribed boundary), or `6` (Dirichlet-type velocity).

To define sediment transport boundaries for Gaia, **create a copy of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)** and call it **boundaries-gaia.cli**. In the context of Gaia, most hydrodynamic boundary types can be kept and only the **LIEBOR** entry requires some adaptations. For this purpose, open the new **boundaries-gaia.cli** file with a {ref}`text editor <npp>` and modify the eighth entry (cf. {numref}`Tab. %s <tab-gaia-bc>`) of all open liquid boundary lines. Counting line entries sounds like a tedious task, but is fairly straightforward in practice:

* The first three entries (cf. {numref}`Tab. %s <tab-gaia-bc>`) of the upstream and downstream boundaries are:
  * **LIHBOR** for water depth,
  * **LIQBOR** for sediment transport, and **LIVBOR** (flow velocity). These three values were set to `5` in the corresponding hydrodynamics boundary file ({ref}`dry-initialized steady2d simulation<tm2d-dry>`) and can be kept to use **prescribed H and Q** upstream and downstream boundaries.
* The following four entries (4-7 in {numref}`Tab. %s <tab-gaia-bc>`) are `0.000` (for Q2BOR, UBOR, VBOR, and AUBOR) and would prescribe (assign) float values directly in the boundary file (deactivated through the `0.000` setting).
* The eighth entry is the **LIEBOR** type, which currently set to `2` (closed wall) and has to be modified for use with Gaia:
  * Open the upstream and downstream boundary for sediment transport by **setting LIEBOR to `4`** (prescribed flowrate). This setting is useful for prescribing sold flowrates either in the steering file or with a liquid boundaries file as described in the {ref}`unsteady (quasi-steady) tutorial <tm2d-liq-file>`.
  * Alternatively, a value of `5` can be assigned for prescribing equilibrium solid flowrates, which also requires that EBOR is set to `0.0` (no change of bottom elevation).

The boxes below indicate how the required adaptations in the `boundaries-gaia.cli` file where the importance lies in the second entry (**LIQBOR**) being set to `5` and the eighth entry (**LIEBOR**) being set to `4`.

````{tabbed} Upstream boundary
```
[go to line 7]
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         144           7   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        9824           8   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        9831           9   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          89          10   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        9817          11   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        9818          12   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         109          13   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000       10011          14   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        9820          15   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         105          16   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        7936          17   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          93          18   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        7940          19   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        7555          20   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000       11484          21   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          73          22   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000       11481          23   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          77          24   # upstream (144 - 32)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          32          25   # upstream (144 - 32)
```
````

````{tabbed} Downstream boundary
```
[go to line 312]
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          34         312   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         113         313   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         765         314   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         116         315   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000       11242         316   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          81         317   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         769         318   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          85         319   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          97         320   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        5293         321   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         101         322   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        5294         323   # downstream (34 - 5)
5 5 5  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000           5         324   # downstream (34 - 5)
```
````

To prescribe a sediment flowrate of **10 kg$^3\cdot$s$^{-1}$** across the upstream and downstream boundaries through the `LIQBOR = 5`, **add the PRESCRIBED SOLID DISCHARGES keyword to the Gaia steering file (gaia-morphodynamics.cas)**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
PRESCRIBED SOLID DISCHARGES : 10.0;10.0
```

Recall that the first and second values in the list of prescribed solid discharges refer to the first (beginning at line 1) and second open boundary listed in the `boundaries-gaia.cas` (i.e., upstream and downstream in that order).

### Physical Parameters (General)

The essential physical parameters embrace sediment type, grain sizes, and definitions of
transport mechanisms that apply to the simulation. This tutorial deals with non-cohesive sediment only, which is defined through the keywords setting `TYPE OF SEDIMENT : NCO`.

```{admonition} Cohesive sediment transport
Gaia considers sediment with grain diameters of less than 60$\cdot$10$^{-6}$m being cohesive. To model such fine sediment, where capillary forces may have a significant impact, adaptations in the boundary conditions file and types are required. In the cohesive sediment case, the `TYPE OF SEDIMENT` keyword is `CO`. Read more about modelling cohesive sediment in section 3.3.3 of the {{ gaia }}.
```

Gaia enables the differentiation between classes of sediment diameters with the **CLASSES SEDIMENT DIAMETERS** keyword. This tutorial features the implementation of three sediment classes in the form of sand (0.0005 m), gravel (0.02 m), and cobble (0.1 m) and assign a grain density of 2680 kg m$^{-3}$ to the three classes.

```fortran
/ continued: gaia-morphodynamics.cas
/
/ PHYSICAL PARAMETERS
/
TYPE OF SEDIMENT : CO
CLASSES SEDIMENT DIAMETERS : 0.0005;0.02;0.1 / in m
CLASSES SEDIMENT DENSITY : 2680;2680;2680 / in kg per m3
```

The particle size classes can also be assigned specific shield energy values or settling velocities.




Particular sediment transport formulae are related to the phenomena under consideration and their implementation in the Gaia steering file is explained in the next sections.


Specific settling velocities or shields parameters can be defined or calculated directly by GAIA (default).

(gaia-bl)=
### Bedload

{term}`Bedload` transport that is supplied by channel-internal and external sources, mostly during floods. The calculation of {term}`Bedload` requires a differentiation between two limiting factors {cite:p}`church_morphodynamics_2015`:

1. The flow-driven transport capacity and
2. The sediment supply.

The hydraulic transport capacity (1) results from and evaluation of {term}`Dimensionless bed shear stress`$\tau_x$ and its critical value, often referred to as the `Shields parameter` $\tau_{x,cr}$ .


$\tau_{* cr}$ is also a function of channel roughness and slope, relative submergence and bedload transport intensity {cite:p}`wilcock_critical_1993,gregoretti_inception_2008,lamb_is_2008,recking_bed-load_2008,ferguson_river_2012`.



`BED LOAD FOR ALL SANDS : YES or NO`
`BED-LOAD TRANSPORT FORMULA FOR ALL SANDS`

(gaia-sl)=
### Suspended Load

`SUSPENSION FOR ALL SANDS : YES or NO`

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
