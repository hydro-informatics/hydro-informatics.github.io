(gaia-basics)=
# Basic Setup of Gaia

The following instructions refer to the setup of the above-created Gaia steering file (*gaia-morphodynamics.cas*), which needs some mandatory parameters and enables many more optional keywords settings. An overview of available keywords can be found in the {{ gaia_ref }} and the Gaia dictionary file `/telemac/v8p2/sources/gaia/gaia.dico`. Similar to the Telemac2d or Telemac3d hydrodynamics steering file, the Gaia steering file can be distinguished between keyword groups for general (file-related), physical (sediment transport), and numerical parameters. This section introduces general parameters embracing the setup of boundary condition files and basic definitions of sediment and riverbed characteristics. The implementation of {term}`Bedload` and/or {term}`Suspended load` is covered in separate sections.

(gaia-gen)=
## General Parameters

The general parameters defining mandatory input and output files resemble those of the hydrodynamic steering file. The input files can even be the same used in the hydrodynamics steering file. For instance, **define** the **[qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf)** from the {ref}`pre-processing <slf-prepro-tm>` **as geometry file**. In addition, add **boundaries-gaia.cli** as **BOUNDARY CONDITIONS FILE**, which will be explained in the section on {ref}`boundary conditions for Gaia <gaia-bc>`. The Gaia **RESULTS FILE** keyword should also differ from the RESULTS FILE keyword in the hydrodynamic steering file.

```fortran
/ gaia-morphodynamics.cas
/
/ COMPUTATION ENVIRONMENT
/
GEOMETRY FILE : qgismesh.slf
BOUNDARY CONDITIONS FILE : boundaries-gaia.cli
RESULTS FILE : rGaia-steady2d.slf
MASS-BALANCE : YES
```

Graphical output variables related to sediment transport can be defined with the **VARIABLES FOR GRAPHIC PRINTOUTS** keyword for {term}`Bedload` and/or {term}`Suspended load` and the following list-options:

* `B` for bottom elevation in (m a.s.l.)
* `E` for bottom evolution in (m)
* `F` for {term}`Froude number` (-)
* `M` for the magnitude (length) of the bi-directional (i.e., $x$ and $y$ directions) unit sediment transport $\boldsymbol{q_s}$ (read more in the definition of the {term}`Exner equation`) in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `MU` for the skin friction coefficient (as a function of {ref}`skin friction correction factors <c-friction>` described in the section on bedload)
* `N` for unit bedload transport in $x$-direction $\boldsymbol{q_b}\cdot\cos\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$) where  $\alpha$ is the angle between the longitudinal channel ($x$) axis and the solid transport vector $\boldsymbol{q_b}$.
* `P` for unit bedload transport in $y$-direction $\boldsymbol{q_b}\cdot\sin\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `QSBL` for the magnitude (length) of the bi-directional (i.e., $x$ and $y$ directions) unit **bedload (only)** transport $\boldsymbol{q_b}$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `R` for the non-erodible bottom (?)
* `S` for water surface elevation in (m a.s.l.)
* `TOB` for bed shear stress in (N$\cdot$m$^{-2}$)

The parameters `M` and `QSBL` will result in the same output if no suspended load is simulated. To output multiple parameters, **set** the **VARIABLES FOR GRAPHIC PRINTOUTS** keyword for this tutorial as follows:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : B,E,M,MU,N,P,QSBL,TOB
```

(gaia-bc)=
## Boundary Conditions

The boundary conditions in Gaia work similarly to the hydrodynamics and can be derived from the hydrodynamics [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) file.

````{admonition} Recall the structure of the hydrodynamics boundaries.cli file
:class: tip, dropdown
The [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) file has 13 variables per line, which are separated with a `space` and this is how the file head looks like (for closed wall `2`-type boundaries):

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

A boundaries `*.cli` file is divided into 13 space (tab) - separated colons corresponding to 13 boundary type (variables) and value prescriptions. The cross-comparison {numref}`Table %s <tab-gaia-bc>` holds the 13 type/value prescription names of a hydrodynamic Telemac2d/3d (e.g., [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)) boundary conditions file up side by side with those of a Gaia boundary conditions file.

````{dropdown} View the cross-comparison Table of Boundary variables and types in Telemac2d/3d and Gaia
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
````

The boundary type variables (no. 1, 2, 3, and 8) listed in {numref}`Tab. %s <tab-gaia-bc>` can take the integer values `2` (closed wall), `4` (free Neumann-type boundary), `5` (Dirichlet-type prescribed boundary), or `6` (Dirichlet-type velocity). It is important for a Gaia simulation that the eighth entry (**LIEBOR**) is set to `4` or `5` for open-type boundaries, but **not to `2`**, which would correspond to a closed wall for tracers (suspended load).

To this end, create a sediment transport boundaries file (`*.cli`) for Gaia by **creating a copy of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)** and calling the copy **boundaries-gaia.cli**. In the context of Gaia, the hydrodynamic boundary types can be kept, though their flags are differently interpreted according to the list in {numref}`Tab. %s <tab-gaia-bc>`.

```{admonition} Why two boundary condition files?
Most examples of the TELEMAC installation (`/telemac/v8p2/examples/gaia/`) use a single boundary conditions file, which works fine because the numerical values are identical. However, the flags of a Gaia `*.cli` and a Telemac2d/3d `*.cli` file are not the same and for this reason, this eBook features good practice by using two (identical) boundary condition files. Thus, we could use a single `*.cli` file, but we do use `*.cli` two files to be prepared for more complex and physically correct simulations in the future. For instance, a more complex future simulation may require prescribing bedload fluxes in the `*.cli` file, where the extra Gaia boundary file is not just an option.
```

To verify the correct setup of the boundary conditions files, open **boundaries.cli** and **boundaries-gaia.cli**  with a {ref}`text editor <npp>` and check on the liquid boundary definitions. Both the **boundaries.cli** and the **boundaries-gaia.cli** files are similarly organized according to {numref}`Tab. %s <tab-gaia-bc>`.

* The first three entries of the upstream boundary are (according to {numref}`Tab. %s <tab-gaia-bc>`):
  * `4` for **LIHBOR** for water depth, which was set to `5` in the {ref}`dry-initialized steady2d simulation<tm2d-dry>`;
  * `5` for **LIQBOR** for (solid) discharge, and **LIVBOR** (flow velocity) corresponding to the hydrodynamics boundary file ({ref}`dry-initialized steady2d simulation<tm2d-dry>`).
  *  In summary, make sure to **prescribe Q only** (i.e., with `4 5 5`) at the upstream boundary.

```{admonition} Why not prescribe water depth (elevation) at the upstream boundary?
The riverbed elevation is expected to change in a morphodynamic simulation. Thus, with a movable bed, we are interested in how the water depth and the riverbed elevation change as a function of water runoff (e.g., important in the case of floods). Prescribing the water depth/elevation at the inflow boundary would fail to meet this objective.
```

* The first three entries of the downstream boundary are (according to {numref}`Tab. %s <tab-gaia-bc>`):
  * `5` for **LIHBOR** for prescribed water depth, in line with the {ref}`dry-initialized steady2d simulation<tm2d-dry>`;
  * `4` for **LIQBOR** for (solid) discharge, and **LIVBOR** (flow velocity).
  *  In summary, make sure to **prescribe Q only** (i.e., with `5 4 4`) at the downstream boundary.

```{admonition} Why not prescribe discharge at the downstream boundary?
The sediment outflow is mostly unknown and prescribing fluxes at the downstream boundary would force the model to deposit any sediment inflow in the model, too. Thus, the model must have the option to vary outflow as a function of eroded (or deposited) sediment, which may lead to different fluxes at the upstream and downstream boundaries.
```

* The following four entries (4-7 in {numref}`Tab. %s <tab-gaia-bc>`) are `0.000` (for the Q2BOR, UBOR, VBOR, and AUBOR values) and would prescribe (assign) float values directly in the boundary file (deactivated through the `0.000` setting).
* The eighth entry is the **LIEBOR** type, which must bet set to `4` or `5` for enabling solid discharge fluxes and may not be `2` (closed wall). To enable solid flux modeling with Gaia from any existing purely hydrodynamic Telemac2d/3d simulation `*.cli`, make the following modifications (already done in *boundaries.cli*/*boundaries-gaia.cli* for this tutorial):
  - the **upstream LIEBOR to `5`** (prescribed -equilibrium- flowrate), which also requires that EBOR is set to `0.0` (no change of bottom elevation), and
  - **downstream LIEBOR to `4`** (free).

The prescription of time-dependent solid flowrates with a liquid boundaries file can be achieved with `LIEBOR=5` and following the descriptions in the {ref}`unsteady (quasi-steady) tutorial <tm2d-liq-file>`.

The below boxes feature the setup of the **boundaries.cli** and **boundaries-gaia.cli** files for this tutorial according to the above descriptions.

````{tabbed} Upstream boundary
```
[go to line 7]
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000         144           7   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        9824           8   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        9831           9   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000          89          10   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        9817          11   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        9818          12   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000         109          13   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000       10011          14   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        9820          15   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000         105          16   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        7936          17   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000          93          18   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        7940          19   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000        7555          20   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000       11484          21   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000          73          22   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000       11481          23   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000          77          24   # upstream (144 - 32)
4 5 5  0.000 0.000 0.000 0.000  5  0.000 0.000 0.000          32          25   # upstream (144 - 32)
```
````

````{tabbed} Downstream boundary
```
[go to line 312]
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          34         312   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         113         313   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         765         314   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         116         315   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000       11242         316   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          81         317   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         769         318   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          85         319   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000          97         320   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        5293         321   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000         101         322   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000        5294         323   # downstream (34 - 5)
5 4 4  0.000 0.000 0.000 0.000  4  0.000 0.000 0.000           5         324   # downstream (34 - 5)
```
````

This section only explains the **geometric** assignment of boundary types in the `*.cli` files. In addition, (sediment) **fluxes** across these open boundaries are to be **defined in the (Gaia) steering file**. The prescription (and initialization) of sediment fluxes differs for bedload (discharge per boundary) and suspended load (concentration per sediment class fraction) and this is why the implementation of sediment flux prescriptions is defined in separate sections (i.e., {ref}`boundary prescriptions for bedload <gaia-bc-bl>` and {ref}`concentration prescriptions for suspended load <gaia-bc-sl>`).


## Riverbed Composition

(gaia-sed)=
### Sediment Classes

The essential physical parameters embrace sediment type, grain sizes, and definitions of
transport mechanisms that apply to the simulation. This tutorial deals with non-cohesive sediment only, which is defined through the keywords setting `TYPE OF SEDIMENT : NCO`.

```{admonition} Cohesive sediment transport
Gaia considers sediment with grain diameters of less than 60$\cdot$10$^{-6}$m to 100$\cdot$10$^{-6}$m being cohesive. To model such fine sediment, where capillary forces may have significant effects on erosion, adaptations in the boundary conditions file and types are required. In the cohesive sediment case, the **TYPE OF SEDIMENT** keyword is `CO`. Read more about modeling cohesive sediment in section 3.3.3 of the {{ gaia }}.
```

Gaia enables the differentiation between classes of sediment diameters with the **CLASSES SEDIMENT DIAMETERS** keyword (same keyword for both bedload and suspended load). This tutorial features the implementation of three sediment classes in the form of sand (0.0005 m), gravel (0.02 m), and cobble (0.1 m) and assigns a grain density (**CLASSES SEDIMENT DENSITY**) of 2680 kg m$^{-3}$ to the three classes. The grain sizes correspond to representative mean (average) diameters for every class. The **CLASSES INITIAL FRACTION** keyword is a list assigning a fraction (i.e., the share of the total sediment) to each of the three classes. Make sure that the **sum of all fractions is exactly 1.0**. Moreover, as *INITIAL* already suggests, the here defined fractions correspond to the initial state and Gaia will re-mix the sediment fractions as a function of erosion and deposition of sediment size classes.

```fortran
/ continued: gaia-morphodynamics.cas
/
/ PHYSICAL PARAMETERS FOR SEDIMENT
/
CLASSES TYPE OF SEDIMENT : NCO;NCO;NCO
CLASSES SEDIMENT DIAMETERS : 0.0005;0.02;0.1 / in m
CLASSES SEDIMENT DENSITY : 2680;2680;2680 / in kg per m3
CLASSES INITIAL FRACTION : 0.1;0.65;0.25 / must sum up to 1.0
```

The particle size classes can also be assigned specific {term}`Shields parameter` values (**CLASSES CRITICAL SHEAR STRESS**) or settling velocities (**CLASSES SETTLING VELOCITIES**), for example, to impose no-erosion or no-deposition conditions. Note that the SISYPHE keyword NUMBER OF SIZE-CLASSES OF BED MATERIAL is obsolete in Gaia.

Particular sediment transport formulae for simulating {term}`Bedload` or {term}`Suspended load` are related to the phenomena under consideration and their implementation in the Gaia steering file is explained in the next sections.

```{admonition} Zonal sediment size and fraction definitions
:class: tip
Sediment size classes can be declared for particular zones of a model, similar to friction zones (recall the friction zone box at the bottom of the {ref}`section on friction boundaries <tm2d-friction>`). Thus, a Selafin (`*.slf`) file containing riverbed characteristics can be declared with the geometry in the Gaia steering file. An example for zonal sediment definitions is provided with the Wilcock-Crowe model in the TELEMAC installation (e.g., `/telemac/v8p2/examples/gaia/wilcock_crowe-t2d/` -  have a look at **gai_ref_WC2003.slf** in {ref}`BlueKenue <bluekenue>`).
```

(gaia-active-lyr)=
### Active Layer

The {ref}`boundary conditions <gaia-bc>` of a model define sediment supply (inflow) and outflow rates, which may stem from gauging stations, measurements, or watershed soil loss models, such as the Revised Universal Soil Loss Equation (RUSLE) {cite:p}`renard1997`. Sediment that just passes through the model and merely settles from time to time before being mobilized again (by {cite:t}`einstein_bed-load_1950`s theory) is referred to as wash load or traveling bedload {cite:p}`piton_concept_2017`. However, sediment can also be recruited (eroded) from the riverbed or deposited on the riverbed within the model boundaries. To tell a morphodynamic model to what depths it can erode (e.g., because bedrock or concrete is present below), active layers can be defined. In addition, multiple active layers can be defined, for example, to implement sediment stratification in the riverbed with respect to grain sizes. Grain size stratification plays a role especially when the riverbed is armored, which means that the uppermost sediment layer is significantly coarser than deeper sediment layers {cite:p}`hirano1971`. **Above the active layer** of the riverbed **is the mixing layer**, which is in direct contact with the bulk water flow. {numref}`Figure %s <active-layers>` qualitatively illustrates this concept, where the uppermost layer corresponds to the mixing layer and the lower sublayers constitute the active layer of the riverbed.

```{figure} ../img/telemac/active-layers-web.jpg
:alt: active mixing layer riverbed hyporheic zone
:name: active-layers

Qualitative illustration of the active layer in the form of multiple sublayers of the riverbed. In this illustration, the uppermost layer corresponds to the mixing layer (Figure conceptually adapted from {cite:t}`du_boys_etudes_1879` and {cite:t}`church_what_2017`).
```

The active layer concept was initially introduced by {cite:t}`du_boys_etudes_1879` as a sequence of layers of the riverbed, which are moving at different speeds (the deeper the layer, the slower). {cite:t}`du_boys_etudes_1879` described that the thickness of every layer was equal to the diameter of representative grain size and that the active bed (i.e., the sum of all moving layers) can be up to 10 times the representative grain size (i.e., approximately 10 grain diameters) {cite:p}`frey2011,ravelet2013`. {cite:t}`hirano1971` picked up on this concept and characterized the active layer as an exchange layer with a thickness of multiple times the $D_{50}$, between an immobile sublayer and a fully mobile layer in the bulk flow along the riverbed. Several processes (e.g., hydraulic shear, grain collision, or sorting) dominate within the exchange layer and the thickness of the exchange layer has been defined differently by several authors. One reason for the different definitions of the active layer thickness is that it also depends on the proportion of fine sediment contents. The difference between coarse and fine sediment is that it might build up bedforms such as ripples or dunes. Thus, in the presence of fine sediments, such as sand (diameter smaller than 1-2 mm), only models accounting for bedforms in the active layer can reproduce bed aggradation or degradation and grain sorting effects {cite:p}`blom2008`. However, a model considering bedforms composed of fine sediments describes the active layer as a function of (0.5 times) the height of dunes (i.e., mega ripples) {cite:p}`kleinhans2005`, which contrasts with the definition of the active layer thickness as a multiple of a grain diameter (e.g., 3$\cdot D_{50}$). Thus, there are **two** competing parametric and **conceptual definitions of the active layer**, which is why {cite:t}`church_what_2017` propose the following terminology that is adapted in this eBook:

* The **active layer describes the immediately mobile riverbed** where **real-time**, **dynamic** particle displacement happens. Its thickness is a multiple of the characteristic grain diameter.
* The **disturbance layer encompasses sand wave progression** in the form of **scour and fill** on an **event scale**. Its thickness is 0.5 times the dune (or ripple) height.

Though Gaia accepts only an **ACTIVE LAYER THICKNESS** keyword, it may refer to the *active layer* as a multiple of the representative grain size, or when fine sediment is present ($\geq$ 20%), to the *disturbance layer* with a thickness of 0.5 times the dune height. When the riverbed is composed not of cobble and gravel and a small share of fine sediment (approximately between 1% and 20%), the active layer thickness should be generously assumed with a multiple (2-3 times) of the cobble size.

Moreover, the thickness of the active layer is a user-defined **target** value in Gaia. Thus, Gaia will iterate based on hydrodynamics and sediment characteristics toward the user-defined active layer thickness. In particular, Gaia erodes the user-defined {ref}`sediment size classes <gaia-sed>` from the active layer as a function of hydrodynamics computed with Telemac2d/3d. The eroded sediment is then transported in the form of {ref}`bedload <gaia-bl>` or {ref}`suspended load <gaia-sl>`. To this end, Gaia creates the active layer with the user-defined sediment classes at the surface of the riverbed at the beginning of a simulation. During the simulation, Gaia not only erodes the sediment but also redeposits it depending on hydrodynamics and sediment characteristics, and it modifies the user-defined initial values of sediment class fractions. Thus, Gaia changes the active layer during the simulation in space and in time and it uses the **ACTIVE LAYER THICKNESS** as target value (not as a forced constant).

The riverbed can be stratified into several sublayers (cf. {numref}`Fig. %s <active-layers>`) by defining the **NUMBER OF LAYERS FOR INITIAL STRATIFICATION** keyword (integer). Gaia then vertically divides the riverbed into the number of user-defined layers plus one, where the plus-one layer corresponds to the active layer. In addition, the thickness of the riverbed layers can be defined with the **LAYERS INITIAL THICKNESS** keyword. If the **ACTIVE LAYER THICKNESS** is larger than the riverbed's **LAYERS INITIAL THICKNESS**, Gaia will mix the stratified layers down to the **ACTIVE LAYER THICKNESS**. However, the active layer thickness is not a forced value in Gaia. Thus, if the active layer thickness is larger than the riverbed layer thickness, Gaia will not erode beyond the riverbed layer thickness.

```{admonition} What happens when Gaia has to deposit sediment?
Sediment deposition at a grid node corresponds to a mass flux into the active layer. Because Gaia is programmed to conserve the mass of the active layer, a portion corresponding to the volume of deposition is passed to the riverbed. Thus, Gaia changes the composition of the active layer and the riverbed layers below the active layer when sediment deposits.
```

In this tutorial, a sand, gravel, and cobble sediment mix is used with an **ACTIVE LAYER THICKNESS** of 3 $\cdot D_{90}$ (of cobble). The riverbed is initially stratified into three sublayers (plus the 0.3-m thick active layer) and the initial thickness of the riverbed layers is assumed with 1.5 m with the following keyword definitions in the Gaia steering file:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ ...
/ RIVERBED LAYERS
ACTIVE LAYER THICKNESS : 0.3 / multiple of D90 - default is 10000
NUMBER OF LAYERS FOR INITIAL STRATIFICATION : 3 / default is 1
LAYERS INITIAL THICKNESS : 1.5 / m - default is 100
```

Gaia derives mixed cohesive and non-cohesive sediment beds from the composition of the active layer. Non-cohesive sediment in the form of gravel and cobble is transported as bedload and sand is transported in suspension. Cohesive sediment is purely transported as suspended load. The {{ gaia }} provides more information on the transport of mixed (cohesive and non-cohesive) sediment in section 3.2.1. In addition, riverbed consolidation can be simulated by defining the **BED MODEL** keyword with `2` (cf. {{ gaia }}, section 3.3).

## Bedload vs. Suspended Load

Sediment transport modeling quickly becomes computationally expensive. Therefore, it is important to be clear about the primary type of sediment transport mode and to activate only the most important phenomenon (i.e., either {term}`Bedload` or {term}`Suspended load`). For this reason, answer the question ***What type of sediment transport phenomenon is predominant in the model?*** If you are not sure about the answer to this question, revise the section on {ref}`sediment transport modes <gaia-seditrans>`. In addition, here are some practice-oriented suggestions:

 * **Bedload only**: Modeling suspended load in a gravel-cobble bed river with a sand content (i.e., the sediment is mostly larger than 2 mm) of less than 5-10% is not purposeful and the definition `SUSPENSION FOR ALL SANDS : NO` should be used. In this case, the {ref}`section on bedload modeling <gaia-bl>` provides all necessary information and the suspended load section can be skipped.
* **Suspended load only**: Fine particle displacement in reservoirs, lakes, or coastal areas, primarily involves suspended load processes. If the sediment is generally finer than 1 mm, modeling bedload may not be necessary. In this case, skip the bedload modeling section and directly jump to the {ref}`section on suspended load modeling <gaia-sl>`.
* **Bedload and suspended load**: When the sediment mixture involves sand particles with diameters between 1-2 mm, and/or particles that may be both finer or coarser, mixed transport processes drive sediment transport. In this case, both sections on {ref}`bedload <gaia-bl>` and {ref}`suspended load <gaia-sl>` modeling should be accomplished.
* **Cohesive sediment**: When cohesive sediment is in the system (i.e., grain diameters of less than 0.06 mm), {ref}`suspended load <gaia-sl>` modeling must be activated.

This eBook features the implementation of combined bedload and suspended load modeling in a short river section with a gravel-cobble bed and a sand content of 10% (with the 0.5-mm class).
