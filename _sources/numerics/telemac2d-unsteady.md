(chpt-unsteady)=
# Unsteady 2d Simulation

```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials.




The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Get Started

The {ref}`steady 2d tutorial <telemac2d-steady>` hypothesizes that the discharge of a river is constant over time. However, the discharge of a river is never truly steady and varies slightly from second to second, even in flow-controlled rivers. Alas, the inherently unsteady flow regime of rivers cannot realistically be modeled in any numerical software. As a result, we must discretize time-dependent discharge (e.g., a flood hydrograph) in a numerical model as a series of steady discharges. {numref}`Figure %s <unsteady-hydrograph>` illustrates the discretization of a natural flood hydrograph into steps of steady flows, which will be used in this tutorial.

```{figure} ../img/telemac/unsteady-hydrograph.png
:alt: unsteady flow discharge quasi steady telemac telemac2d hydrodynamic
:name: unsteady-hydrograph

The discretization of a natural hydrograph into steps of steady flows (qualitative hydrograph for this tutorial).
```

This tutorial shows how such a quasi-unsteady discharge hydrograph can be created and implemented in a Telemac2d simulation. The tutorial builds on the steady simulation of a discharge of 35 m$^3$/s and requires the following data from the {ref}`pre-processing <slf-prepro-tm>` and {ref}`steady2d <telemac2d-steady>` tutorials, which can be downloaded by clicking on the filenames:

* The computational mesh in [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf).
* The boundary definitions in [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries.cli).
* The results of the steady 2d model run for 35 m$^3$/s in [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) (result of the {ref}`dry bonus run <tm2d-dry>`).

Consider saving the files in a new folder, such as `/unsteady2d-tutorial/`.

```{admonition} Unsteady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/).
```

(prepro-unsteady)=
## Adapt the Steering File

The integration of unsteady flows requires the adaptation of keywords and additional keywords (e.g., for linking liquid boundary files) in the steering (`*.cas`) file from the steady2d tutorial ([download steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the unsteady CAS file
To view the integration of the unsteady simulation keywords in the steering file, the `unsteady2d.cas` file can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/unsteady2d.cas)
```

With the upstream open (liquid) boundary type being `4 5 5` (prescribed Q) and the downstream open (liquid) boundary type being `5 5 5` (prescribed Q and H), a time-dependent flow hydrograph and a {term}`Stage-discharge relation` needs to be provided (recall the rationales behind the choice of boundary types from the {ref}`pre-processing tutorial <bk-liquid-bc>`).

To activate the use of a {term}`Stage-discharge relation` for an open (liquid) boundary with the `STAGE-DISCHARGE CURVES` keyword needs to be added to the steering file. This keyword accepts the following integers:

* `0` is the **default** that deactivates the usage of stage discharge.
* `1` applies prescribed elevations as function of calculated flow rate (discharge).
* `2` applies prescribed flow rates (discharge) as function of calculated elevation.

The `STAGE-DISCHARGE CURVES` keyword is a list that assigns one of the three integer (i.e., either `0`, `1`, or `2`) to the open (liquid) boundaries. In this tutorial `STAGE-DISCHARGE CURVES : 0;1` actives the use of a {term}`Stage-discharge relation` for the downstream boundary only where the **upstream open boundary number 1** is set to `0` and the **downstream open boundary number 1** is set to `0`. To recall how TELEMAC counts open boundaries read the comment box in the {ref}`steady2d tutorial <tm2d-bounds>`.

The form (curve) of the {term}`Stage-discharge relation` needs to be defined in a stage-discharge file ({term}`ASCII` text format). Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). This tutorial uses the following relation that is stored in a file called `ratingcurve.txt` ([download](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/ratingcurve.txt)):

```
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
```

To define {term}`Stage-discharge relation`s for multiple open boundaries (e.g., at river diversions or tributaries), add the curves to the same file. TELEMAC automatically recognizes where the curves apply by the number given in parentheses after the parameter name in the column header. For instance, in the above example for this tutorial, the column headers `Z(2)` and `Q(2)` tell TELEMAC to use these values for the second (i.e., downstream) open boundary. The column order is not important because TELEMAC reads the curve type (i.e., either $Q(Z)$ or $Z(Q)$) from the `STAGE-DISCHARGE CURVES` keyword.

````{admonition} Expand to view an example for multiple stage-discharge curve definitions
:class: note, dropdown
The following file block would prescribe {term}`Stage-discharge relation`s to the upstream and downstream boundary conditions in this tutorial. However, the file cannot be used here unless the upstream boundary type is changed to `5 5 5` (prescribed H and Q) in the `boundaries.cli` file (read more in the {ref}`pre-processing tutorial <bk-liquid-bc>`).
```
#
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
#
# Upstream Rating Curve
#
Q(1)  Z(1)
m3/s  m
35    371.33
50    371.45
101   371.86
1130  375.73
2560  379.08
```
````

To use a stage-discharge file, define the following keyword in the steering file:

```
/ steering.cas
STAGE-DISCHARGE CURVES : 1
STAGE-DISCHARGE CURVES FILE : YES
```
