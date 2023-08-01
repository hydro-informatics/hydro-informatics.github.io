(tm-foc-bc)=
# Boundary Conditions

```{admonition} Requirements

This tutorial does not require running code, but we recommend to at least setting up a Telemac model, such as described in the {ref}`steady 2d tutorial <telemac2d-steady>`, which eases the understanding of concepts and terms.
```

The liquid boundary conditions are overdetermined when too many parameters are prescribed, which are at least numerically competing. For example, if discharge and water depth are prescribed but cannot be achieved with the defined roughness coefficients, Telemac will attempt to comply with the water depth. However, this water depth does often not correspond to the prescribed discharge and Telemac tries to compensate for the difference by varying the lengths (amounts) of the velocity vectors. In turn, the velocity vectors are constrained by the roughness coefficients. Thus, Telemac tries to vary water depths and velocity vectors to achieve a {term}`stage (H)-discharge (Q) relation <Stage-discharge relation>` prescribed at the boundary, which might be impossible with the defined roughness. A workaround would be to adjust roughness (friction) coefficients so that the defined boundary conditions and roughness coefficients are exactly in balance. However, the boundary conditions should be calibrated specifically for multiple terrain types (i.e., {ref}`roughness zones <tm-friction-zones>`) through model calibration using measured values and not imposed by issues at the model boundaries to achieve mass balance. So, what next?

To deal with the problem of overdetermined boundary conditions and mass imbalance, the next sections first provide tips on correctly placing liquid boundaries geometrically, then recall the setup of a boundary file, the types of boundaries (i.e., values), and how they might affect the mass balance.

```{admonition} Tips for modeling rivers
:class: important

The workflows and tips shown in this chapter primarily refer to the numerical modeling of rivers with Telemac. Similar conditions might apply to lake estuaries, but other environments, such as coastal regions, will require different considerations for defining boundary conditions.
```

(tm-foc-draw-bc)=
## Draw Liquid Boundaries

When drawing liquid boundaries, for example, in BlueKenue, a couple of geometric characteristics will help to improve the stability and mass balance of the later simulation: 

* Liquid boundaries should have at least 5-10 nodes.
* All liquid inflow boundaries should have a close-to equal number of nodes as the sum of liquid outflow boundaries.
* Liquid inflow (upstream) boundaries should only be defined at the lower riverbed, never on the riverbanks or floodplains (see {numref}`Fig. %s <draw-inflow>`).
* Draw the boundaries sufficiently far away from the region of interest: imposed or unrealistic water depths (or water surface elevations) related to the flowrates will otherwise strongly affect the region of interest. As a rule of thumb, in a 2d simulation, the upstream and downstream boundaries should be at least 800 to 1000 m distanced from the region of interest.

```{figure} ../../img/telemac/cross-section-sx.png
:alt: draw bluekenue liquid boundary conditions conlim upstream inflow
:name: draw-inflow

The red highlighted part of this qualitative cross section should be defined as the inflow (upstream) boundary condition. Mesh nodes at the riverbanks and on the floodplains should not be included.
```


(tm-foc-unpack-bc)=
## The Structure of Boundaries.Cli

The steady 2d, unsteady 2d, and tutorials showcase the different types of boundaries using prescribed discharge (`Q`) and/or water depth (`H`), which are implemented into a boundaries `.cli` file consisting of 13 space (tab) - separated colons:

````{admonition} Example of a hydrodynamics boundaries.cli file (first 3 rows)
:class: note
```
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000         138           1
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9836           2
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9838           3
...
```
````

The 13 space (tab) - separated colons correspond to 13 boundary variables, which are listed in {numref}`Table %s <tab-bc-overview>` for a hydrodynamic Telemac2d/3d (see [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)) and a Gaia boundary conditions file.


```{list-table} Meaning of columns in a Boundary.Cli file for Telemac2d/3d and Gaia.
:header-rows: 1
:name: tab-bc-overview

* - Column no.<br>
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
    <small>*flowrate* (*concentration*)</small>

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


The first three columns of a `.cli` file determine whether a boundary is solid or liquid, and if liquid, the type of liquid boundaries. These three columns (i.e. LIHBOR, LIUBOR, and LIVBOR) may take the following values:

* `0` to enforce a zero velocity boundary
* `2` to indicate a solid (wall) boundary with friction
* `4` to define a free liquid boundary type
* `5` to define a prescribed (i.e., determined) liquid boundary type
* `6` to prescribe a velocity (only for LIUBOR/LIVBOR)

Also, these values can be assigned to column 8 (LITBOR/LIEBOR) of the `.cli` file. Note that in a hydrodynamic simulation, the combination of columns 2 and 3 (LIUBOR and LIVBOR) is effectively a discharge boundary. All other columns are *Prescriptions* and *Node IDs*. The *Prescriptions* may be used to impose, for example, a flow velocity value (not recommended). The *Node IDs* were written by BlueKenue (or whatever mesh generator was used) and should not be modified. Thus, regarding the mass balance of water, the first three columns are important and they can get assigned the (common) value combinations listed in {numref}`Tab. %s <bc-defs-tm>` below. For the mass balance of tracers, column 8 can be defined analogously. Additionally, a `.cli` file for sediment transport can be similarly defined with the first three columns, as described in the {ref}`Gaia tutorial <gaia-bc>`.

```{list-table} Value combinations for the first three columns of a hydrodynamic boundaries.cli file affecting the mass balance of water.
:header-rows: 1
:name: bc-defs-tm

* - **Type**
  - Number code
  - Typical application
* - Solid
  - `2 2 2`
  - Solid boundaries
* - Prescribed Q
  - `4 5 5`
  - {ref}`Upstream liquid <tm2d-bounds>`
* - Prescribed H
  - `5 4 4`
  - {ref}`Downstream liquid <tm2d-bounds>`
* - Prescribed H and Q
  - `5 5 5`
  - {ref}`Stream gauges <tm2d-bounds>` (rather avoid)
```

(tm-edit-bc)=
## Edit Boundary.Cli to Change Conditions

To view or edit the type of boundary conditions, open the `.cli` file with a text editor (read more about {ref}`text editors <npp>`). Typically, most of the rows will hold the value combination `2 2 2` in columns 1-3, that is, they are solid boundaries. The liquid boundary rows start with `4` or `5` as listed in {numref}`Tab. %s <bc-defs-tm>`. Every row in the `.cli` file represents a node of the mesh, and neighboring rows represent neighboring mesh nodes. For instance, the node described in row (line) 435 of a `.cli` file is geospatially located directly between the boundary nodes described in lines 434 and 436 of the `.cli` file. Since the definitions in the `.cli` file are purely geometric or geometric attributes, additional hydraulic attributes must be prescribed or linked in the steering (`.cas`) file. Thus, the Telemac steering file controls how much water is flowing through the liquid boundaries, and/or the water depth/surface elevation with the following keywords:

```fortran
/ Keywords in a .cas steering file
PRESCRIBED ELEVATIONS : 518.20 ; 0
PRESCRIBED FLOWRATES  : 0 ; 118.0
/ PRESCRIBED VELOCITIES : 1.0 ; 1.0 / not use simultaneously with PRESCRIBED FLOWRATES
/ PRESCRIBED DEPTH : 1.0 ; 1.0 / not use simultaneously with PRESCRIBED ELEVATIONS
```

Alternative usages of these keywords can be found in the {ref}`unsteady 2d <tm2d-liq-file>` and {ref}`Gaia <gaia-bc>` tutorials, or section 4.2 of the {{ tm2d }}. Note that every `PRESCRIBED ...` row separates values for each liquid boundary with a `;` sign. Notably, the first and second values apply to the first and second boundaries defined in the `.cli` file, counting from the top of the `.cli` file (see next paragraph). If one of these values is `0` (e.g., the second ELEVATION and the first FLOWRATE boundary), Telemac will treat it as a free (`4`) liquid boundary.

The order of boundaries can be found in the `.cli` file: the first node sequence where rows (lines) start with either `4` or `5` (or `6`) is the first liquid boundary. Because the mesh generator placed neighboring nodes in neighboring rows, the boundary lines are defined in neighboring rows, too. The below box features an example of a downstream boundary defined between nodes 7-12 (global IDs 144-9818). Further down in the `.cli` file, another liquid boundary (e.g., `4 5 5`) might be found to define upstream inflows. In this case, the downstream boundary is boundary 1 and the upstream boundary is boundary 2, and both are accordingly prescribed in the steering (`.cas`) file.

````{admonition} Example of a downstream 5 4 4 (prescribed H) boundary defined in a .cli file
:class: tip
:name: cli-example

```
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9828           6   # 
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000         144           7   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9824           8   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9831           9   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000          89          10   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9817          11   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9818          12   # downstream (144 - 9818)
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        7602          13   # 
```
````


## Boundaries & Convergence

The prescription of `5 4 4` (H only), `4 5 5` (Q only), or `5 5 5` (Q and H) boundary conditions in the {ref}`above example <cli-example>` may result in numerical instabilities of a dry-initialized simulation, or unbalanced inflows and outflows.

To verify mass conservation, refer to the next section on {ref}`quantitative convergence <tm-convergence>` analysis of fluxes across (or through) the liquid boundaries.

To troubleshoot mass convergence issues, have a look at our {ref}`workflow for mass conservation <tm-foc-mass-workflow>`.
