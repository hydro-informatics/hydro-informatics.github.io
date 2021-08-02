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
## TELEMAC Setup

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

(gaia-sed)=
## Define Sediment

The essential physical parameters embrace sediment type, grain sizes, and definitions of
transport mechanisms that apply to the simulation. This tutorial deals with non-cohesive sediment only, which is defined through the keywords setting `TYPE OF SEDIMENT : NCO`.

```{admonition} Cohesive sediment transport
Gaia considers sediment with grain diameters of less than 60$\cdot$10$^{-6}$m being cohesive. To model such fine sediment, where capillary forces may have a significant impact, adaptations in the boundary conditions file and types are required. In the cohesive sediment case, the `TYPE OF SEDIMENT` keyword is `CO`. Read more about modelling cohesive sediment in section 3.3.3 of the {{ gaia }}.
```

Gaia enables the differentiation between classes of sediment diameters with the **CLASSES SEDIMENT DIAMETERS** keyword. This tutorial features the implementation of three sediment classes in the form of sand (0.0005 m), gravel (0.02 m), and cobble (0.1 m) and assign a grain density of 2680 kg m$^{-3}$ to the three classes. The grain sizes correspond to representative mean (average) diameters for every class.

```fortran
/ continued: gaia-morphodynamics.cas
/
/ PHYSICAL PARAMETERS FOR SEDIMENT
/
CLASSES TYPE OF SEDIMENT : NCO
CLASSES SEDIMENT DIAMETERS : 0.0005;0.02;0.1 / in m
CLASSES SEDIMENT DENSITY : 2680;2680;2680 / in kg per m3
```

The particle size classes can also be assigned specific {term}`Shields parameter` values (`CLASSES CRITICAL SHEAR STRESS`) or settling velocities (`CLASSES SETTLING VELOCITIES `) (e.g., to impose no-erosion or no-deposition conditions).

Particular sediment transport formulae are related to the phenomena under consideration and their implementation in the Gaia steering file is explained in the next sections.


(gaia-bl)=
## Bedload

```{admonition} Bedload basics
:class: important
For a better reading experience of this section, the {ref}`glossary` helps with explanations of the terms {term}`Sediment transport`, (dimensionless) {term}`Bedload` transport $\Phi_b$, {term}`Dimensionless bed shear stress` $\tau_{x}$, and the {term}`Shields parameter` $\tau_{x,cr}$ (in that order).
```

(bl-principles)=
### Principles

The calculation of {term}`Bedload` transport requires expert knowledge about the modeled ecosystem for judging whether the system is sediment supply-limited or transport capacity-limited {cite:p}`church_morphodynamics_2015`.

Sediment supply-limited rivers
: A sediment supply-limited river is characterized by clearly visible incision trends indicating that the river's runoff could potentially transport more sediment than is available in the river. Sediment-supply limited river sections typically occur downstream of dams, which represent an unsurmountable barrier for sediment.

Transport capacity-limited (alluvial) rivers
: A transport capacity-limited river is characterized by sediment abundance where the river's runoff is too small to transport all available sediment during a flood. Sediment accumulations (i.e., the alluvium) are present and the channel has the tendency to braiding into {term}`anabranches <Anabranch>`.

The following figures feature sediment supply-limited river sections and a transport capacity-limited river section.

````{tabbed} Artificially sediment supply-limited
```{figure} ../img/nature/doubs-capacity-2015.JPG
:height: 350px
:alt: channel doubs france sediment supply transport limited
:name: doubs-2015

The Doubs in the Franche-Comté (France) during a small flood. The sediment supply is interrupted by a cascade of dams upstream with the consequence of a straight monotonous channel with significant plant growth along the banks. The riverbed primarily consists of boulders that are immobile most of the time. Thus, the river section can be characterized as artificially sediment supply-limited (picture: Sebastian Schwindt 2015).
```
````

````{tabbed} Naturally sediment supply-limited
```{figure} ../img/nature/krimmler-ache-2010.jpg
:height: 350px
:alt: naturally channel krimmler ache austria sediment supply transport limited
:name: krimml-2010
:class: with-shadow

The Krimmler Ache in Austria during a small flood event. Even though the watershed has a high {term}`Sediment yield`, the transport capacity of the water in this river section is so high, that the riverbed only consists of large boulders. Thus, the river section can be characterized as naturally sediment supply-limited (picture: Sebastian Schwindt 2010).
```
````

````{tabbed} Capacity-limited
```{figure} ../img/nature/jenbach-alluvial-2020.jpg
:height: 350px
:alt: alluvial channel jenbach sediment supply transport limited
:name: jenbach-2020

The Jenbach in the Bavarian Alps (Germany) after an intense natural sediment supply in an upstream reach in the form of a landslide. Thus, the river section can be characterized as transport capacity-limited (picture: Sebastian Schwindt 2020).
```
````

**Why is the differentiation between sediment supply and transport capacity-limited rivers important for numerical modeling?**

Gaia provides different formulae for calculating bedload, which are mostly either derived from lab experiments with infinite sediment supply (e.g., the {cite:t}`meyer-peter_formulas_1948` formula and its derivates or from field measurements in partially transport capacity-limited rivers (e.g., {cite:t}`wilcock_critical_1993`). Formulae that account for limited sediment supply often involve a correction factor for the {term}`Shields parameter`.


### Calculous and Parameters

{term}`Bedload` is typically designated with $q_b$ (in kg$\cdot$s$^{-1}\cdot$m$^{-1}$) and accounts for particulate transport in the form of the displacement of rolling, sliding, and/or jumping coarse particles. In river hydraulics, the so-called {term}`Dimensionless bed shear stress` or also referred to as {term}`Shields parameter` {cite:p}`shields_anwendung_1936` is often used as the threshold value for the mobilization of sediment from the riverbed. TELEMAC and Gaia output a dimensionless expression of bedload transport according to {cite:t}`einstein_bed-load_1950`:

$$
\Phi_b = \frac{q_b}{\rho_{w} \sqrt{(s - 1) g D_{pq}}}
$$ (eq-phi-gaia)

where $\rho_{w}$ is the density of water; $s$ is the ratio of sediment grain and water density (typically 2.68) {cite:p}`schwindt_hydro-morphological_2017`; $g$ is gravitational acceleration; and $D_{pq}$ is the characteristic grain diameter of the sediment class (cf. {ref}`gaia-sed`). Note that the dimensionless expression $\Phi$ and the dimensional expression $q_b$ represent unit bedload (i.e., bedload normalized by a unit of width). In Gaia, the unit of width corresponds to a side of a numerical mesh cell over which the mass fluxes are calculated.

Equation {eq}`eq-phi-gaia` expresses only the dimensional conversion for bedload transport (i.e., the way how dimensions are removed or added to sediment transport). In fact, this is only the first step to solve the other side of a bedload equation by means of a (semi-) empirical formula. To calculate $\Phi_b$, Gaia currently provides a set of (semi-) empirical formulae, which can be modified with user Fortran files and defined in the Gaia steering file with the `BED-LOAD TRANSPORT FORMULA FOR ALL SANDS` `integer` keyword. {numref}`Table %s <tab-gaia-bl-formulae>` lists possible integers for the keyword for currently available bedload transport formulae, including references to original publications, formula application ranges, and the names of the Fortran files for modifications.

```{csv-table} *Bedload transport formulae implemented in Gaia with application limits with regards to the grain diameter $D$, and **cross section-averaged** Froude number $Fr$, slope $S$, water depth $h$, and flow velocity $u$. The Fortran files live in TELEMAC sources-directory.*
:header: Gaia, Author(s), $D$, "*{term}`Fr <Froude number>`*; $S$; $h$; and $u$", User Fortran
:header-rows: 1
:widths: 10, 50, 30, 35, 15
:name: tab-gaia-bl-formulae
"(no.)", "(ref.)", "(10$^{-3}$m)", "(-); (-); (m); (m/s)", "(file name)"
{ref}`1 <gaia-mpm>`, "{cite:t}`meyer-peter_formulas_1948`", 0.4 $<$D_{50}$<$28.6, "10$^{-4}<Fr<$639<br> 0.0004$<S<$0.02<br>0.01$<h<$1.2<br>0.2$<u$", [bedload_meyer_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__meyer__gaia_8f.html)
{ref}`2 <gaia-einstein>`, "{cite:t}`einstein_bed-load_1950, brown1949`", 0.25$<D_{35}<$32, "", [bedload_einst.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__einst__gaia_8f.html)
 `3`, {cite:t}`engelund_monograph_1967`, 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", [bedload_engel_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__engel__gaia_8f.html)
 `30`, "{cite:t}`engelund_monograph_1967,chollet1979`", 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", [bedload_engel_cc_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__engel__cc__gaia_8f.html)
 `7`, {cite:t}`van_rijn_sediment_1984`, 0.6$<D_{50}<$2.0, "0.5$<h$<br>0.2$<u$", [bedload_vanrijn_gaia.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__vanrijn__gaia_8f.html)
```

To use the {cite:t}`meyer-peter_formulas_1948` formula (`1` according to  {numref}`Tab. %s <tab-gaia-bl-formulae>`) in this tutorial, **add the following line to the gaia-morphdynamics.cas steering file:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
/
BED LOAD FOR ALL SANDS : YES / deactivate with NO
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1
```

The following sections provide more details on how $\Phi_b$ is calculated with the pre-defined formulae listed in {numref}`Tab. %s <tab-gaia-bl-formulae>`.

```{admonition} User Fortran Files
:class: note, dropdown
To implement a user Fortran file, copy the original TELEMAC Fortran file from the `/telemac/v8pX/sources/` directory (e.g., `/telemac/v8pX/sources/gaia/bedload_einst_gaia.f`) to the project directory (e.g., `/telemac/v8pX/simulations/gaia-tutorial/user_fortran/bedload_einst_gaia.f`). Finally, tell TELEMAC where to look for user fortran files by defining the following keyword in a steering file (e.g., in `gaia-morphodynamics.cas`):

`FORTRAN FILE : 'user_fortran'`
```

(gaia-mpm)=
### Meyer-Peter and Müller (1948)

```{admonition} Recall the validity range for the MPM formula (1)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

The {cite:t}`meyer-peter_formulas_1948` formula was published in 1948 by Swiss researchers Eugen Meyer-Peter, professor at [ETH Zurich](https://ethz.ch/en.html) and founder of the school's hydraulics laboratory (Zurich's famous [VAW](https://vaw.ethz.ch/)), and Professor Robert Müller. Their empirical formula is the result of more than a decade of collaboration and the elaboration began one year after the VAW was founded in 1931, when Robert Müller was appointed assistant to Eugen Meyer-Peter. The two scientists also worked with Henry Favre and Hans-Albert Einstein who came up with another approach for calculating bedload. An early version of the {cite:t}`meyer-peter_formulas_1948` formula was published in 1934 and it is the basis for many formulas that refer to a critical {term}`Dimensionless bed shear stress` (i.e., {term}`Shields parameter`). It is important to remember that the formula is based on data from lab flume experiments with quasi unlimited sediment supply. This is why bedload transport calculated with the {cite:t}`meyer-peter_formulas_1948` formula corresponds to the {ref}`hydraulic transport capacity <bl-principles>` of an alluvial channel. Thus, **the {cite:t}`meyer-peter_formulas_1948` formula tends to overestimate bedload transport** and it is inherently designed for estimating bedload **based on simplified 1d cross section-averaged hydraulics** (see also the {ref}`Python sediment transport exercise <ex-py-sediment>`).

Ultimately, the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) can be calculated with the {cite:t}`meyer-peter_formulas_1948` formula as follows:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x,cr} > \tau_{x} \\ f_{mpm} \cdot (\tau_{x} - \tau_{x,cr})^{3/2} & \mbox{ if } \tau_{x,cr} \leq \tau_{x}\end{cases}
$$ (eq-mpm)

where $f_{mpm}$ is the MPM coefficient (default is 8), $\tau_{x,cr}$ denotes the {term}`Shields parameter` ($\approx$ 0.047 and up to 0.07 in mountain rivers), and $\tau_{x}$ is the {term}`Dimensionless bed shear stress`. When using the {cite:t}`meyer-peter_formulas_1948` formula with Gaia, consistency with original publications is **ensured by defining $\tau_{x,cr}$ and $f_{mpm}$ in the steering file**:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / see above
SHIELDS PARAMETERS : 0.047
MPM COEFFICIENT : 8
```

````{admonition} Wong-Parker correction of the MPM formula
The Wong-Parker correction {cite:p}`wong_reanalysis_2006` for the {cite:t}`meyer-peter_formulas_1948` formula refers to a statistical re-analysis of the original experimental datasets and applies to {term}`Plane bed` river sections. To this end, the Wong-Parker correction yields lower bedload transport values and it excludes the form drag correction of the original formula with the following expression: $\Phi_{b} \approx 3.97 \cdot (\tau_{x} - 0.0495)^{3/2}$. Thus, to implement the Wong-Parker correction in Gaia use:

```fortran
SHIELDS PARAMETERS : 0.0495
MPM COEFFICIENT : 3.97
```
````

(gaia-einstein)=
### Einstein-Brown (1942/49)

```{admonition} Recall the validity range for the Einstein-Brown formula (2)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

Hans Albert Einstein, son of the famous Albert Einstein, was a pioneer of probability-based analyses of sediment transport. In particular, he hypothesized that the beginning and the end of sediment motion can be expressed in terms of probabilities. Furthermore, Einstein assumed  that the sediment motion is a series of step-wise displacements followed by rest periods and that the average distance of a displacement is approximately hundred times the particle (grain) diameter. Aiming to account for his observations in lab flume experiments, Einstein introduced hiding and lifting correction coefficients {cite:p}`einstein1942`.

The Einstein formula differs from any {cite:t}`meyer-peter_formulas_1948`-based formula in that it does not imply a threshold for incipient motion of sediment. However, despite or because Einstein's sediment transport theory is significantly more complex than many other bedload transport formulae, it did not become very popular in engineering applications. Today, Gaia enables user-friendly applications of Einstein's formula, which was similarly presented by {cite:t}`brown1949` at an engineering hydraulic conference in 1949.

According to {cite:t}`einstein1942`-{cite:t}`brown1949`, the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) is calculated as follows:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x} < 0.0025
F_{eb} 2.15 \cdot \exp{-0.391/\tau_{x}} & \mbox{ if } 0.0025 \geq \tau_{x} \leq 0.2\\ F_{eb} \cdot  40 \cdot \tau_{x}^{3} & \mbox{ if } \tau_{x} > 0.2  \tau_{x}\end{cases}
$$ (eq-einstein-brown)

where

$$
F_{eb} = \left(\frac{2}{3} + \frac{36}{D_x}\right)^{0.5} - \left(\frac{36}{D_x}\right)^{0.5}
$$ (eq-f-eb)

$D_x$ is the dimensionless particle diameter calculated as:

$$
D_x = \left[\frac{(s-1)\cdot g}{\nu^2}\right]^{1/3}\cdot D_{pq}
$$ (eq-d-dimless)

where $s$ is the ratio of sediment grain and water density (typically 2.68); $g$ is gravitational acceleration; and $\nu$ is the kinematic viscosity of water ($\approx$10$^{-6}$m$^{2}$ s$^{-1}$) {cite:p}`schwindt_hydro-morphological_2017`.

To use the {cite:p}`einstein1942`-{cite:t}`brown1949` formulae in Gaia use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 2
```

```{admonition} Consider adapting bedload_einst.f
The application thresholds as a function of $\tau_{x}$ stem from the Gaia Fortran file [bedload_einst.f](http://docs.opentelemac.org/doxydocs/v8p2r0/html/bedload__einst__gaia_8f.html). However, the original publications suggest using a threshold of $\tau_{x}$=0.182 (rather than 0.2) for switching the formula cases.
```





(gaia-engelund)=
### Engelund-Hansen (1967)

```{admonition} Recall the validity range for the Engelund-Hansen formulae (3 and 30)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

The {cite:t}`engelund_monograph_1967` formula takes into account the solid transport as a whole and thus considers the transport in suspension and the transport by scavenging. Starting from the current power approach of the original 1966 formula of {cite:t}`bagnold_approach_1966,bagnold_empirical_1980`, the formula describes in particular the solid transport in the dune regime due to low energies by balancing the energy useful to drive the particles up the dunes with the energy supplied by the fluid to the particles. Applying the theory of {cite:t}`bagnold_approach_1966,bagnold_empirical_1980`, the shear $$ is the sum of the shear transmitted between the grains by the fluid and the shear transmitted by moment changes caused by intergranular collisions. Consequently, grains are eroded as long as the fluid shear equals the critical shear.

dimensionless friction coefficient $f_{eh}$

$$
f_{eh} = \frac{2\cdot S}{Fr}
$$

$$
\Phi_b = \frac{0.1\cdot \tau_{*}}{f_{eh}}
$$ (eq-engelund)


```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 3 / 30
```



(gaia-rijn)=
### van Rijn (1984)

```{admonition} Recall the validity range for the van-Rijn formula (7)
:class: warning
Revise {numref}`Tab. %s <tab-gaia-bl-formulae>` to ensure that the application is in the applicable range of parameters corresponding to the conditions under which the formula has been developed.
```

In developing his formula, Leo van Rijn studied several formulations, among which are those of {cite:t}`bagnold_empirical_1980`, {cite:t}`einstein1942` or {cite:t}`ackers_sediment_1973`. The theory of {cite:t}`bagnold_empirical_1980`, according to which bedload is dominated by gravity while suspended transport is controlled by turbulence, was followed in the path of {cite:t}`van_rijn_sediment_1984` formulations. For the calculation of the bedload transport, in a manner identical to \cite{ackers73}, the important parameters retained are the dimensionless diameter as well as a solid transport parameter depending on the frictional velocities. To calibrate his near-bed (bedload) solid transport model, {cite:t}`van_rijn_sediment_1984` used data from experiments on flat-bottomed channels with different materials whose mean diameter was 1.8~[mm]. Then, {cite:t}`van_rijn_sediment_1984`conducted further comparative experiments to compare the results of the old model with experiments in channels for river flows and particles of 0.2 to 2~[mm] diameter. Concerning the suspended transport, {cite:t}`van_rijn_sediment_1984` established criteria for suspension also based on laboratory experiments by simplifying the calibration parameters empirically. Finally he performed a validation of the suspension transport using particles smaller than 0.5~[mm]. This was performed using several data sets and then comparing the results with those obtained from different formulas.
The formula of {cite:t}`van_rijn_sediment_1984` takes into account the total sediment transport, i.e. by scavenging and by suspension by calculating both parts separately.

$$
\Phi_b = 0.053\cdot \frac{T{2.1}}{D_{x}^{0.3}}
$$ (eq-rijn)

$$
T = \frac{{u}^2_* - {u}^2_{*, cr}}{{u}^2_{*, cr}}
$$



```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 7
```


(gaia-sl)=
## Suspended Load

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
